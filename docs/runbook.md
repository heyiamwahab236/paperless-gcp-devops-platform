# Operations runbook

All commands below are **Bash in WSL2**, from the repository root, unless stated otherwise. Prerequisites and memory setup are in [windows-wsl2.md](windows-wsl2.md). Use synthetic documents only. Run the two environments sequentially.

## 1. Start and verify Compose

```bash
python3 scripts/init_local.py
docker compose config --quiet
docker compose pull
docker compose up -d --wait --wait-timeout 900
docker compose exec webserver createsuperuser
docker compose ps
python3 scripts/smoke.py
docker stats --no-stream
```

Open `http://localhost:8000`. Admin creation is interactive; no password is written to command history. `init_local.py` never rotates existing secrets. Compose secrets are local files mounted into containers, not a managed secret store. PostgreSQL's initial password is applied only when its data directory is empty.

The app can take several minutes on first startup due to migrations and image unpacking. `up --wait` returning successfully confirms container health; the API smoke test separately confirms the processing path. Write down the document ID/marker from the smoke result. Capture the UI with the synthetic title, not personal documents.

### Restart/persistence exercise

```bash
docker compose restart
docker compose up -d --wait --wait-timeout 900
```

Log in again, search for the **same marker**, and download the original. A new smoke run alone cannot prove old data survived; it creates a new document each time. Record what you actually observed and retain the original marker in your evidence.

### Stop without deleting data

```bash
docker compose stop
```

`docker compose down` removes containers/network but retains named volumes. `docker compose down --volumes` deletes this Compose project's database, queue, index, and document volumes. Use the latter only for an intentionally disposable test after exporting anything needed. Do not rename the Compose project or volume names while expecting old data to reappear.

## 2. Run the same workload in Minikube

The Kubernetes environment starts empty and does not import Compose data automatically.

```bash
docker compose stop
minikube start --profile=paperless-lab --driver=docker --cpus=2 --memory=3072 --kubernetes-version=v1.35.0
python3 scripts/init_local.py
python3 scripts/kube_secret.py --context paperless-lab
helm lint helm/paperless --strict
helm upgrade --install demo helm/paperless --kube-context paperless-lab \
  --namespace paperless --wait --timeout 15m
kubectl --context paperless-lab -n paperless get pods,pvc,svc
kubectl --context paperless-lab -n paperless exec -it deployment/demo-paperless-app -- createsuperuser
kubectl --context paperless-lab -n paperless port-forward --address=127.0.0.1 service/demo-paperless-app 8000:8000
```

Keep the port-forward terminal open. In a second WSL terminal run `python3 scripts/smoke.py` from the repository root. Visit `http://localhost:8000`. Stop the port-forward with Ctrl+C when finished.

`kube_secret.py` explicitly addresses a context rather than trusting your current context. It writes only the namespace and a Secret called `paperless-secrets`; it never prints secret contents. The chart does not embed credential values in Helm's release record.

### Persistence and resources

```bash
kubectl --context paperless-lab -n paperless rollout restart deployment/demo-paperless-app
kubectl --context paperless-lab -n paperless rollout status deployment/demo-paperless-app --timeout=15m
kubectl --context paperless-lab -n paperless get pods,pvc
```

Restart the port-forward if it disconnected. Search for the same previous marker and verify its original again. For a resource snapshot you can use `docker stats --no-stream` to measure the Minikube container. If metrics are needed, explicitly enable `minikube addons enable metrics-server --profile=paperless-lab`, wait for it to be ready, then use `kubectl --context paperless-lab -n paperless top pods`. Metrics-server adds overhead; it is optional.

### Stop and cleanup

```bash
minikube stop --profile=paperless-lab
```

This preserves the profile. `helm uninstall demo --kube-context paperless-lab -n paperless` retains the three PVCs; reinstall using the same release name and credentials to reuse them. **Deleting the namespace, PVCs, or Minikube profile can delete the data.** Export off the node first. For an intentionally disposable lab, inspect `kubectl --context paperless-lab -n paperless get pvc` before deleting the dedicated `paperless` namespace or `minikube delete --profile=paperless-lab`. No cleanup command should target another profile or namespace.

## 3. Backup and restore drill (Compose)

This uses the upstream document exporter/importer. It is a logical application export, not point-in-time database recovery. Preserve `.secrets`, configuration and image locks separately in private storage; they are not public evidence. Exports contain originals and account information and must remain private.

1. Stop uploads and consumption, wait for pending tasks to finish, and make sure the test instance has no email ingestion or scheduled external writers. Do not export while records/files are changing. For production, arrange a proper maintenance/consistency procedure.
2. Run a dated export, then copy it outside the runtime directory:

```bash
stamp=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "runtime/export/$stamp"
docker compose exec -T webserver document_exporter "/usr/src/paperless/export/$stamp"
mkdir -p backups
cp -a "runtime/export/$stamp" "backups/$stamp"
find "backups/$stamp" -type f -print0 | sort -z | xargs -0 sha256sum > "backups/$stamp.sha256"
docker compose stop
```

Keep this shell's `stamp`, or set it to the actual export folder name later. The checksum manifest detects later file changes; it does not independently prove that the export is complete or restorable. Check the exporter exit code and expected documents. Keep an additional encrypted copy on a separate storage device if the data matters.

3. Restore into an isolated Compose **project** on another port. This preserves the original volumes. The project name and port below must not already be in use. The runtime export folder and credential files are shared read sources; do not put new files into `runtime/consume` during this drill.

```bash
PAPERLESS_PORT=8001 docker compose -p paperless-restore up -d --wait --wait-timeout 900
PAPERLESS_PORT=8001 docker compose -p paperless-restore exec -T webserver document_importer "/usr/src/paperless/export/$stamp"
```

Use a fresh database with the **same Paperless version** for the importer. Do not create an admin in the restore project before import; the export carries users. If an earlier restore attempt populated those volumes, choose another unused project name or deliberately reset only the disposable restore project after checking it. Visit `http://localhost:8001`, use the restored account, search for the original marker, compare document counts and tags, and download the original. Confirm its hash matches the pre-backup file. Log a measured elapsed time only after completing this exercise.

4. After verification, remove only the disposable restore project and restart the original:

```bash
PAPERLESS_PORT=8001 docker compose -p paperless-restore down --volumes
docker compose up -d --wait --wait-timeout 900
```

The restore command is destructive only to the named restore project's volumes. Keep the original and restore stacks sequential on an 8 GB machine. Never interpret a successful exporter command as a successful restore drill.

### Kubernetes export before node deletion

Quiesce ingestion and wait for pending tasks. Use `kubectl exec` to create `/storage/export` and run `document_exporter /storage/export` in `deployment/demo-paperless-app`. Find the current app pod with `kubectl --context paperless-lab -n paperless get pods -l app.kubernetes.io/component=app`. Copy `/storage/export` out with `kubectl --context paperless-lab -n paperless cp POD_NAME:/storage/export backups/kubernetes-export -c app`, replacing `POD_NAME` with that exact pod name. `kubectl cp` requires `tar` in the image. Verify the files locally before deleting anything. Restore to an empty same-version instance as documented upstream; a Kubernetes restore has not been proven merely by the Compose drill.

## 4. Upgrade and rollback

Read the [upstream release notes](https://github.com/paperless-ngx/paperless-ngx/releases), run a verified export/restore drill, and record current image digests. Resolve the intended image tags to their actual registry digests. Update `images.lock.json`, `compose.yaml`, `helm/paperless/values.yaml`, and the chart `appVersion` together. Run validation, image scans, and the appropriate runtime demo before changing persistent data. Dependabot updates tools/providers; image updates currently require a reviewed manual change.

Paperless migrations may make a previous image incompatible with an upgraded database. **Do not rely on `helm rollback` or an older image tag as a data rollback strategy.** Restore the pre-upgrade export into fresh same-version storage, verify it, then switch access. PostgreSQL major upgrades require upstream-supported export/import or `pg_upgrade` procedures; never attach a version-18 container directly to an older-major database volume.

## 5. Troubleshooting and observability

| Symptom | Inspect | Likely next step |
|---|---|---|
| Cannot connect to Docker | `docker version` | Start Docker Desktop, enable Ubuntu WSL integration; use Linux containers |
| Container unhealthy | `docker compose ps`; `docker compose logs --tail=100 webserver` | Check DB/broker health and migrations; allow first startup time |
| Permission denied on consume/export | `id -u`; `id -g`; `.env`; directory ownership | Run in WSL Linux storage; correct UID/GID, then recreate app |
| DB authentication fails after editing secrets | DB logs and whether pgdata already existed | File edits do not rotate database roles; restore original credential or perform coordinated SQL/app rotation |
| K8s Pending | `kubectl --context paperless-lab -n paperless get events --sort-by=.lastTimestamp` | Inspect insufficient resources or unbound PVC; ensure default storage provisioner exists |
| K8s CrashLoopBackOff | `kubectl --context paperless-lab -n paperless logs deployment/demo-paperless-app --tail=100` | Inspect startup errors, Secret references, permissions, dependency readiness |
| OOMKilled or exit 137 | Pod describe / container status; actual memory | Reduce document size/concurrency and stop the other environment before considering larger limits |
| UI works, documents absent | App worker logs and task status in UI | The web probe does not test the queue; use smoke and inspect ingestion errors |
| Browser cannot reach Minikube app | Port-forward terminal and service/pod selectors | Reopen port-forward after app restart; use localhost:8000 |
| Exported data missing after node deletion | Off-node backup location | Local PV retention cannot survive destroyed node storage |

Compose logs are bounded to two 5 MB files per service. The lab relies on logs, health/readiness and explicit resource snapshots. It does not include a metrics dashboard or configured alerts. Logs can expose document titles, user names and content: inspect privately, redact before publishing, and never upload raw `kubectl get secret -o yaml`, `docker inspect`, environment dumps, or Terraform state.
