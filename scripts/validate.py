"""Run non-deploying validation. Requires Docker CLI/Compose, Helm and Terraform.

No Docker daemon or cloud credentials required. init downloads the locked provider.
"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]


def run(command, capture=None):
    print('+ ' + ' '.join(command), flush=True)
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=bool(capture))
    if capture:
        capture.write_text(result.stdout, encoding='utf-8')
    if result.returncode:
        if capture:
            print(result.stderr)
        raise SystemExit(result.returncode)


def main():
    os.chdir(ROOT)
    build = ROOT / 'build'
    build.mkdir(exist_ok=True)
    for executable in ('docker', 'helm', 'terraform'):
        if not shutil.which(executable):
            raise SystemExit(f'Missing prerequisite: {executable}')
    for path in ROOT.rglob('*.yaml'):
        if any(p in ('.terraform', 'build', '.venv', 'runtime') for p in path.parts) or 'templates' in path.parts:
            continue
        list(yaml.safe_load_all(path.read_text(encoding='utf-8')))
    for path in (ROOT / '.github').rglob('*.yml'):
        list(yaml.safe_load_all(path.read_text(encoding='utf-8')))
    run(['docker', 'compose', 'config', '--quiet'])
    run(['helm', 'lint', 'helm/paperless', '--strict'])
    for name, values in [('local', []), ('gke', ['-f', 'helm/values-gke.yaml'])]:
        manifest = build / f'{name}.yaml'
        run(['helm', 'template', 'demo', 'helm/paperless', '--namespace', 'paperless'] + values, manifest)
        run([sys.executable, 'scripts/check_manifests.py', str(manifest)])
        tool = shutil.which('kubeconform')
        if not tool:
            local = build / 'tools' / ('kubeconform.exe' if os.name == 'nt' else 'kubeconform')
            tool = str(local) if local.exists() else None
        if not tool:
            raise SystemExit('Install kubeconform using scripts/install_ci_tools.py kubeconform')
        run([tool, '-strict', '-summary', '-kubernetes-version', '1.35.0', str(manifest)])
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    run([sys.executable, 'scripts/check_docs.py'])
    run(['terraform', '-chdir=terraform', 'fmt', '-check', '-recursive'])
    run(['terraform', '-chdir=terraform', 'init', '-backend=false', '-input=false', '-lockfile=readonly'])
    run(['terraform', '-chdir=terraform', 'validate', '-no-color'])
    run(['terraform', '-chdir=terraform', 'test', '-no-color'])
    print('PASS: non-deploying validation. Runtime and cloud deployment are not proven by these checks.')


if __name__ == '__main__':
    main()
