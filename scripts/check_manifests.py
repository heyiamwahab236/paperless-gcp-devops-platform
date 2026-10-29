"""Portfolio policy checks on real Helm output, complementary to kubeconform."""
import argparse
from pathlib import Path
import yaml


def check(documents):
    objects = [obj for obj in documents if obj]
    errors = []
    claims = {obj['metadata']['name'] for obj in objects if obj['kind'] == 'PersistentVolumeClaim'}
    deployments = [obj for obj in objects if obj['kind'] == 'Deployment']
    if len(deployments) != 3:
        errors.append('Exactly three workload Deployments are expected')
    for obj in objects:
        kind, name = obj['kind'], obj['metadata']['name']
        if kind == 'Secret':
            errors.append(f'{name}: chart must reference an external Secret')
        if kind == 'Service' and obj['spec'].get('type', 'ClusterIP') != 'ClusterIP':
            errors.append(f'{name}: public service is forbidden')
        if kind == 'PersistentVolumeClaim' and obj['metadata'].get('annotations', {}).get('helm.sh/resource-policy') != 'keep':
            errors.append(f'{name}: PVC retention required')
        if kind != 'Deployment':
            continue
        spec = obj['spec']
        pod = spec['template']['spec']
        if spec.get('replicas') != 1 or spec.get('strategy', {}).get('type') != 'Recreate':
            errors.append(f'{name}: single writer with Recreate required')
        if pod.get('automountServiceAccountToken', True):
            errors.append(f'{name}: unnecessary Kubernetes token')
        if not pod.get('securityContext', {}).get('runAsNonRoot'):
            errors.append(f'{name}: non-root process required')
        for volume in pod.get('volumes', []):
            claim = volume.get('persistentVolumeClaim', {}).get('claimName')
            if claim and claim not in claims:
                errors.append(f'{name}: unresolved PVC {claim}')
        for container in pod['containers']:
            if '@sha256:' not in container['image']:
                errors.append(f'{name}: immutable image digest required')
            security = container.get('securityContext', {})
            if security.get('allowPrivilegeEscalation', True) or 'ALL' not in security.get('capabilities', {}).get('drop', []):
                errors.append(f'{name}: privilege escalation/capabilities not restricted')
            for key in ('startupProbe', 'readinessProbe', 'livenessProbe'):
                if key not in container:
                    errors.append(f'{name}: missing {key}')
            for field in ('requests', 'limits'):
                if not all(k in container.get('resources', {}).get(field, {}) for k in ('cpu', 'memory')):
                    errors.append(f'{name}: missing {field}')
            for env in container.get('env', []):
                if env['name'] in ('PAPERLESS_SECRET_KEY', 'PAPERLESS_DBPASS', 'POSTGRES_PASSWORD') and 'secretKeyRef' not in env.get('valueFrom', {}):
                    errors.append(f'{name}: secret must come from secretKeyRef')
    # Verify each Service selects exactly one Deployment and targets an existing named port.
    for service in (o for o in objects if o['kind'] == 'Service'):
        selector = service['spec']['selector']
        matches = [d for d in deployments if all(d['spec']['template']['metadata']['labels'].get(k) == v for k, v in selector.items())]
        if len(matches) != 1:
            errors.append(f'{service["metadata"]["name"]}: selector must match one workload')
        else:
            ports = {p['name'] for c in matches[0]['spec']['template']['spec']['containers'] for p in c.get('ports', [])}
            if any(p['targetPort'] not in ports for p in service['spec']['ports']):
                errors.append('Unresolved service target port')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    failures = check(yaml.safe_load_all(args.manifest.read_text(encoding='utf-8')))
    if failures:
        raise SystemExit('\n'.join(failures))
    print('PASS: workload, storage, secrets, resource, service, and security policies')
