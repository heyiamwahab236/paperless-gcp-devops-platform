# Verification record — 29 October 2026

The checks below ran locally on Windows. Terraform used a mock provider; no Google Cloud resources or service-account keys were created.

## Completed checks

| Check | Observed result |
|---|---|
| Official image references | All three tags resolved from their public registries to the immutable digests in `images.lock.json` |
| `docker compose config --quiet` | Passed; no daemon needed |
| Helm strict lint | Passed; informational recommendation for a chart icon only |
| Helm render: local and GKE overlay | Passed; 9 Kubernetes resources per configuration |
| kubeconform, strict Kubernetes 1.35.0 schemas | 9 valid, 0 invalid, 0 errors, 0 skipped for each configuration |
| Custom manifest policies | Passed for local and GKE renders |
| Python unit/regression tests | 9 passed |
| Terraform formatting + provider validation | Passed with the locked Google provider |
| Terraform mock tests | 5 passed; simulated resources only |
| Actionlint | All three workflow files passed, embedded shell checking disabled |
| Bash parser | 14 workflow command blocks passed syntax-only parsing; commands not executed |
| Trivy committed-secret scan | No findings in the repository working tree at scan time; not a Git-history scan |
| Trivy Terraform module audit, synthetic inputs | 3 module results; 0 HIGH/CRITICAL findings in this scan |
| Trivy rendered Kubernetes audit | 1 HIGH finding: `KSV-0014`, app root filesystem writable |
| Trivy image scans + SBOM generation | Completed for all three locked images; vulnerability gate failed, as documented in the image summary |

The known Kubernetes finding is retained in the report, not suppressed. Upstream s6 startup uses writable container paths; the lab app remains non-root with dropped capabilities and no privilege escalation. A constrained writable-mount design and runtime test would be required before making its root filesystem read-only. See [security limits](../../SECURITY.md).

The module audit uses `terraform/audit.tfvars.example` with documentation-only inputs. The default root configuration disables cloud resources, so scanning only that root could miss module coverage. The workflow instead audits all three independent modules and checks report coverage.

## Tool versions used locally

| Tool | Version |
|---|---|
| Python | 3.14 (CI uses 3.12) |
| PyYAML | 6.0.3 |
| Docker Compose | 5.1.1 |
| Helm | 4.2.4 (CI uses 3.19.0) |
| Terraform | 1.13.5 |
| Google provider | 7.46.2, official checksums locked for Windows/Linux AMD64 |
| kubeconform | 0.7.0 |
| actionlint | 1.7.7 |
| Trivy | 0.76.1 |

The validation-tool downloads were checked against official release checksums. Terraform reported a HashiCorp-signed provider. Local output is preserved in [validation-log.txt](validation-log.txt); environment-specific absolute paths were replaced with neutral labels. Hosted CI validation is still pending.

## Runtime checks not completed

Docker and WSL2 were installed, but the Linux Docker engine was unavailable. A Docker Desktop startup attempt did not expose a usable engine. The attempted Compose runtime test failed before container creation with a missing `dockerDesktopLinuxEngine` endpoint. No application containers, database volumes, smoke result, UI screenshot or resource benchmark were produced.

Consequently:

- Compose application startup and document ingestion: **NOT VERIFIED**.
- Minikube deployment and pod persistence: **NOT RUN**.
- Export/restore exercise: **NOT RUN**.
- GitHub-hosted validation: **BLOCKED BEFORE EXECUTION** in the [first run](https://github.com/heyiamwahab236/paperless-gcp-devops-platform/actions/runs/40931333478); no validation steps ran.
- Live Google Cloud plan/apply: **INTENTIONALLY NOT RUN**.
- Performance on an 8 GB laptop: **NOT MEASURED**. The memory settings are design budgets; this validation host had more RAM.

Pending runtime checks can be executed through the manual `Runtime demo` workflow or the [runbook](../runbook.md). Image-security results are recorded separately in [image-scan-summary.md](image-scan-summary.md).
