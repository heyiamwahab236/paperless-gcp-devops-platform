# Architecture decisions

| Decision | Reason | Consequence / revisit trigger |
|---|---|---|
| Use upstream Paperless image unchanged | Portfolio focuses on deployment engineering; avoids invented application authorship | Upstream release and dependency vulnerabilities remain upstream dependencies |
| Pin multi-platform image digests | Tags can move; Compose and Helm need the same input | Refresh all three locations deliberately and rerun runtime/security checks |
| PostgreSQL 18 + Valkey 9 | Matches current upstream topology; Valkey is Redis-compatible | PostgreSQL 18 mounts `/var/lib/postgresql`; never reuse an older-major data directory directly |
| One task, one OCR thread, one web worker | Limit CPU and memory pressure on an 8 GB Windows host | Small synthetic workload; no throughput claim until measured |
| Exclude Tika, Gotenberg and AI services | Avoid extra memory and image downloads | Office document conversion and AI features are outside this profile |
| Single replica and Recreate | App and DB are single-writer persistent workloads in this lab | Deliberate maintenance downtime; no zero-downtime or HA claim |
| Deployment + named PVC instead of StatefulSet | One fixed replica, no peer discovery or ordered multi-node identity needed | Rethink workload split before horizontal scaling |
| File secrets locally; pre-existing Secret in Helm | Keep credentials out of Git and Helm release values | Kubernetes Secrets are not encryption; rotation requires DB password synchronization |
| Rootless Kubernetes / upstream root initialization in Compose | Kubernetes fsGroup prepares disks; Compose uses upstream startup ownership mapping | Compose startup exception is documented; do not claim every container starts non-root |
| Health probes plus API smoke test | Distinguish serving a page from processing a document | Check queue behavior and persistence separately; smoke is not backup proof |
| Mock Terraform provider in CI | Exercise resource relationships without credentials or cloud costs | Cannot prove quotas, regional availability, IAM permissions or successful provisioning |
| Private zonal GKE with NAT blueprint | Show explicit network/identity design with only one steady-state node | NAT, GKE, disks, logs and temporary upgrade capacity can all cost money if enabled |
| No GCP deployment workflow or OIDC provider | No cloud deployment is needed for this portfolio | Future delivery should use short-lived federation, scoped permissions and environment approval |
| Configuration audit reports findings; secret scan blocks | Keep local lab compromises visible and actionable | A green validation workflow is not a zero-findings security certification |

## What would change for production

Separate web and worker concerns using supported upstream deployment patterns; add tested managed PostgreSQL, backup schedules, recovery objectives, TLS, application authentication policy, network policies with an enforcing CNI, external secret lifecycle, disaster-recovery tests, capacity measurements, and monitoring with actionable alerts. These are design extensions, not implemented accomplishments.
