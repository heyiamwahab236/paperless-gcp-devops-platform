# Source review — 29 October 2026

The references below were used to check deployment compatibility. Tagged sources correspond to the pinned application release; moving documentation can change. Image manifest digests were retrieved directly from GHCR/Docker Hub and recorded in `images.lock.json`.

| Source | Used to verify |
|---|---|
| [Paperless-ngx v3.3.4 release](https://github.com/paperless-ngx/paperless-ngx/releases/tag/v3.3.4) | Selected upstream release and security maintenance context |
| [Tagged Compose example](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/docker/compose/docker-compose.postgres.yml) | PostgreSQL 18, Valkey 9, service topology and changed PostgreSQL volume root |
| [Tagged setup guide](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/docs/setup.md) | Docker secrets via `_FILE`, rootless support, UID/GID caveats |
| [Tagged configuration](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/docs/configuration.md) | Secret key required, worker limits, OCR mode `auto`, polling interval variable |
| [Tagged administration guide](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/docs/administration.md) | Export/import commands, restore expectations |
| [Tagged Dockerfile](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/Dockerfile) | Port, startup, health command, rootless preparation, GPL-3.0-only declaration |
| [Tagged API views](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/src/documents/views.py) | Original document download query parameter |
| [Admin command wrapper](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/docker/rootfs/usr/local/bin/createsuperuser) | Use the s6-aware wrapper so file-secret values are available and execution drops privileges |
| [Upstream license](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/LICENSE) | Preserved GPL license text |
| [PostgreSQL copyright](https://github.com/postgres/postgres/blob/REL_18_STABLE/COPYRIGHT) | Database license attribution |
| [Valkey copying notice](https://github.com/valkey-io/valkey/blob/9.0/COPYING) | Broker license attribution |
| [Microsoft WSL configuration](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) | WSL memory/CPU/swap settings and restart behavior |
| [GKE node service accounts](https://docs.cloud.google.com/kubernetes-engine/security/configure-node-service-accounts) | Custom node account and `roles/container.defaultNodeServiceAccount` |
| [Google provider cluster resource](https://github.com/hashicorp/terraform-provider-google/blob/main/website/docs/r/container_cluster.html.markdown) | Cluster networking and control-plane fields; then verified against downloaded provider schemas |
| [Terraform mock testing](https://developer.hashicorp.com/terraform/language/tests/mocking) | Credential-free resource simulation |

Provider schemas were validated using the installed, signed Google provider locked to version 7.46.2. Official release checksums were checked for downloaded Terraform, actionlint, kubeconform and Trivy tools. Action references were resolved to commit SHAs using the upstream GitHub API. Check the [validation record](evidence/VALIDATION.md) for actual executions; a reviewed source is not a runtime test.

## Compatibility notes specific to 3.3.4

The current OCR mode choices are `auto`, `redo`, `force`, and `off`; older examples with `skip` should not be copied into this configuration. The consume-folder polling variable is `PAPERLESS_CONSUMER_POLLING_INTERVAL`. Rootless containers must not combine `USERMAP_UID/GID` remapping or runtime OCR-language package installation. PostgreSQL 18's image volume root is `/var/lib/postgresql`, not the legacy `/var/lib/postgresql/data` mapping.
