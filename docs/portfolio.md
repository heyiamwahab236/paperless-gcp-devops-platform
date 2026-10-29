# Presenting the project honestly

## Two-minute walkthrough

1. **Problem:** demonstrate repeatable deployment and operations of a real multi-service application, without keeping paid cloud infrastructure running.
2. **Boundary:** Paperless-ngx is upstream open-source software. The original work is the infrastructure, safeguards, validation, tests and operational documentation.
3. **Implementation:** show the digest lock, Compose resource limits, Helm single-writer/PVC design, and one policy test that rejects an unsafe change.
4. **Cloud design:** show the three Terraform modules, default-off deployment switch and mocked tests. Explain what mocks cannot prove.
5. **Evidence:** open a real Actions run and completed local/runtime screenshots. If a runtime check is still pending, say so plainly.

Do not give an interviewer a public URL that implies the GCP service is running. The repository and its evidence are the portfolio deliverable.

## Resume wording supported by the delivered files

**Paperless Deployment & Operations Lab — DevOps Portfolio**

*Docker Compose, Kubernetes, Helm, Terraform, Google Cloud architecture, GitHub Actions, Python*

- Built deployment and operations tooling around upstream Paperless-ngx, including resource-limited Docker Compose and a Helm chart with persistent storage, health probes and external credential references.
- Designed reusable Terraform modules for Google Cloud networking, private-node GKE and Artifact Registry; validated the configuration with credential-free mock tests without provisioning cloud resources.
- Implemented GitHub Actions workflows for configuration validation, deployment-policy tests, secret scanning and container vulnerability/SBOM reporting; documented reproducible setup and recovery procedures.

Use these after reviewing and understanding the implementation. The phrase “implemented workflows” means the definitions exist; add “verified in GitHub Actions” only after the linked runs actually complete. Do not call this application development, production cloud deployment, professional employment, or a zero-downtime platform.

## Stronger bullets available only after completing the evidence

- **After both runtime demos pass:** “Deployed the upstream application locally with Docker Compose and Minikube/Helm; verified document ingestion, text search, original-file integrity and persistence across restarts.”
- **After a restore drill passes:** “Tested a logical export/restore procedure in an isolated same-version environment and verified restored document counts and original-file hashes.”
- **After recording measurements:** “Configured a two-CPU lab with a 2 GiB combined application memory limit and recorded observed utilization under a documented synthetic workload.” State the real host RAM and measured values separately; do not turn a configured limit into a measured saving.

No current evidence supports “deployed to GCP,” “served thousands of users,” “reduced costs by X%,” “achieved 99.9% uptime,” “production hardened,” or “built Paperless-ngx.” Do not use those claims.

## Interview questions to be ready for

| Question | Explain using the repository |
|---|---|
| Why Recreate rather than rolling updates? | One app writer, bundled worker processes and RWO storage; planned downtime is explicit |
| What does a successful health check miss? | Queue execution, text extraction, search and recovery; the API smoke test covers part of that gap |
| How are secrets kept out of Git? | Exclusive local generation, ignore rules, references in manifests, secret scanning and manual review |
| Why is GKE not running? | The portfolio demonstrates a reviewed blueprint plus local evidence, avoiding ongoing infrastructure charges |
| What can mocked Terraform tests prove? | Expressions, module wiring, defaults and selected security properties; not IAM, quota or provisioning success |
| What would production need? | The documented gaps: isolation, TLS, secret lifecycle, backups, recovery tests, capacity/availability design and alerts |
| What happens if the DB password file changes? | The initialized database keeps its old role password; rotate both sides in a coordinated operation |
| What does an image vulnerability scan prove? | Findings for one image digest and database date; it is not a permanent security certification |

Make at least one deliberate improvement yourself, describe the reason in a real commit, and rerun its relevant checks. Preserve authentic history rather than manufacturing months of activity.
