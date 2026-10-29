# Architecture decisions

| Decision | Reason | Consequence / revisit trigger |
|---|---|---|
| Use upstream Paperless image unchanged | Follow upstream packaging and keep application upgrades separate from deployment configuration | Track upstream releases and dependency vulnerabilities |
| Pin multi-platform image digests | Tags can move; Compose and Helm need the same input | Refresh all three locations deliberately and rerun runtime/security checks |
| PostgreSQL 18 + Valkey 9 | Matches current upstream topology; Valkey is Redis-compatible | PostgreSQL 18 mounts `/var/lib/postgresql`; never reuse an older-major data directory directly |
| One task, one OCR thread, one web worker | Limit CPU and memory pressure on an 8 GB Windows host | Small synthetic workload; throughput has not been measured |
| Exclude Tika, Gotenberg and AI services | Avoid extra memory and image downloads | Office document conversion and AI features are outside this profile |
| Single replica and Recreate | App and DB are single-writer persistent workloads in this lab | Updates require downtime; no high availability |
| Deployment + named PVC instead of StatefulSet | One fixed replica, no peer discovery or ordered multi-node identity needed | Rethink workload split before horizontal scaling |
| File secrets locally; pre-existing Secret in Helm | Keep credentials out of Git and Helm release values | Kubernetes Secrets are not encryption; rotation requires DB password synchronization |
| Rootless Kubernetes / upstream root initialization in Compose | Kubernetes fsGroup prepares disks; Compose uses upstream startup ownership mapping | Compose initializes ownership as root before dropping application privileges |
| Health probes plus API smoke test | Distinguish serving a page from processing a document | Check queue behavior and persistence separately; smoke is not backup proof |
| Mock Terraform provider in CI | Exercise resource relationships without credentials or cloud costs | Cannot prove quotas, regional availability, IAM permissions or successful provisioning |
| Private zonal GKE with NAT blueprint | Use private worker nodes with outbound image access and one steady-state node | NAT, GKE, disks, logs and temporary upgrade capacity can all cost money if enabled |
| No GCP deployment workflow or OIDC provider | Local operation and mock validation require no cloud resources | Future delivery should use short-lived federation, scoped permissions and environment approval |
| Configuration audit reports findings; secret scan blocks | Keep configuration findings available for triage while blocking exposed credentials | Configuration validation and the image vulnerability gate run separate checks |

## What would change for production

Separate web and worker concerns using supported upstream deployment patterns; add tested managed PostgreSQL, backup schedules, recovery objectives, TLS, application authentication policy, network policies with an enforcing CNI, external secret lifecycle, disaster-recovery tests, capacity measurements, and monitoring with actionable alerts. These changes are outside the current implementation.
