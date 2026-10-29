# Security model and reporting

Use synthetic documents and localhost access. This is a single-user operations lab, not a hardened service for confidential records or untrusted internet traffic.

## Implemented controls

- Digest-pinned upstream images; shared image-lock consistency test.
- No committed credentials, private documents, `.tfstate`, plans, or runtime exports.
- Local file secrets and Kubernetes `secretKeyRef`; no plaintext password in Helm values.
- Loopback-only Compose publishing and explicit loopback Kubernetes port-forwarding.
- Non-root Kubernetes workloads, RuntimeDefault seccomp, dropped capabilities, no privilege escalation, no mounted Kubernetes API token.
- Resource limits, bounded Compose logs, startup/readiness/liveness probes.
- Read-only repository permissions in Actions, SHA-pinned action dependencies, no `pull_request_target`, no cloud deployment job or cloud secrets.
- GKE blueprint with private nodes, a single operator `/32`, scoped node IAM, Workload Identity metadata and protected deletion.

## Visible limitations

Compose follows upstream root startup so ownership can be set before application processes drop privileges. The Helm app has a writable root filesystem for upstream s6 startup; DB/broker roots are read-only with explicit writable mounts. No container is privileged and no Docker socket is mounted into application containers.

Valkey has no password within the dedicated local stack/namespace and is never published to the host. PostgreSQL traffic and broker traffic are not TLS-protected in this lab. The chart has no NetworkPolicy; Kubernetes network isolation requires additional policies and a CNI that enforces them. Do not put untrusted workloads in this namespace/cluster.

Kubernetes Secrets are base64 encoding, not encryption. Access to the cluster/node or Docker host may reveal credentials and documents. Keep `.secrets` in protected local storage. Changes to a database-password file do not update an existing PostgreSQL role. Coordinate database role rotation, app credentials and restart; do not regenerate random files against an initialized database.

The cloud blueprint uses Google-managed disk encryption, not customer-managed keys or application-layer Secret encryption. It does not configure organization policy, external secret management, backup schedules or SLO alerts. The public control-plane endpoint is IP-restricted, not fully private. These are explicit sandbox tradeoffs, not silently waived production controls.

## What each security check means

| Check | Behavior |
|---|---|
| Trivy committed-secret scan | Blocks validation on a finding; never upload secrets as evidence |
| Deployment policy tests | Block regressions such as public services, multiple writers, plaintext secret env, or unpinned workload images |
| Trivy Kubernetes + Terraform module audit | Report-only HIGH/CRITICAL findings; coverage checked; retain reports and triage before exposure |
| Image security workflow | Manual/weekly; scans each locked image sequentially, emits SBOMs, fails on any HIGH/CRITICAL vulnerability or scanner error |

The image job does not use `--ignore-unfixed`, blanket ignore files or `continue-on-error`. A red result is expected when upstream/base-image packages have unresolved advisories. Report the affected image/digest, CVE, fix availability, mitigation, and chosen next step. Do not imply a green validation job means no vulnerabilities; it runs different checks. Scanner databases and findings change over time.

The installer verifies archives against official release checksums. This protects against download corruption; it does not independently verify release ownership or signatures. Review tool updates and preserve action SHA pins.

## Reporting

Do not paste a secret or private document into a public issue. For an upstream Paperless vulnerability, follow [its security policy](https://github.com/paperless-ngx/paperless-ngx/security/policy). For this repository, use GitHub private vulnerability reporting when the owner enables it. If a credential was committed, revoke/rotate it first, inspect history and access, and remove it from current files and history using a reviewed remediation procedure; deleting the file in a later commit is insufficient.
