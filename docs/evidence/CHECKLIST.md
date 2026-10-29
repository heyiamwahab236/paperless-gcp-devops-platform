# Evidence checklist

Evidence is a record of completed work, not a list of implied accomplishments. Keep failures and limitations visible. Do not fill a checkbox until its linked artifact exists and you have reviewed it. The baseline verification record is [VALIDATION.md](VALIDATION.md).

## Delivered static evidence

- [x] Original Compose and Helm configuration with clear upstream attribution.
- [x] Immutable image references checked against the public registries.
- [x] Compose configuration validation.
- [x] Helm lint, render, Kubernetes schema and custom policy checks.
- [x] Python regression tests for credential handling and deployment policies.
- [x] Terraform formatting, provider validation and mocked tests.
- [x] GitHub Actions workflow syntax validation.
- [x] Current-version Kubernetes/Terraform configuration audit; findings documented.
- [x] Local image vulnerability scans and SBOMs for all three digests; findings retained, gate failed.
- [x] No Google Cloud resources provisioned.

The checkboxes above summarize the delivery's dated validation record; they are not GitHub run history. See the record for tool versions and exact limits.

## Complete on the laptop or the manual hosted demo

- [ ] Compose: all three services healthy; retain sanitized `docker compose ps` output.
- [ ] Compose: API smoke result with document ID, marker and original checksum check.
- [ ] Compose: one screenshot showing the synthetic document in the real app.
- [ ] Compose: same document still present after restarting the stack.
- [ ] Minikube: ready pods, bound PVCs and ClusterIP services with namespace/context visible.
- [ ] Minikube: API smoke result through the loopback port-forward.
- [ ] Minikube: same document survives app-pod replacement.
- [ ] Backup/restore: export, restore into empty same-version storage, verify old marker/counts/hash.
- [ ] Resource snapshot: record actual host RAM, WSL/Minikube allocation and workload limits.
- [ ] Optional OCR exercise: ingest a tiny scanned page and verify extracted text manually.

An API test using a born-digital PDF proves extraction, not OCR accuracy. Measurements on a larger machine do not prove the 8 GB profile's performance.

## GitHub proof after publication

- [ ] Publish the repository with attribution and license files intact.
- [ ] Link a completed green `Validate` run for the current commit.
- [ ] Run `Runtime demo` once for `compose` and once for `minikube`; retain real artifacts.
- [ ] Run `Image security`; record the date, image digests, findings and remediation decisions.
- [ ] Retain configuration-audit findings and explain lab exceptions.
- [ ] Add branch protection/rules requiring validation if appropriate to your GitHub plan.
- [ ] Replace the publishing guide's example owner with the actual owner wherever you add badges/links.

GitHub workflow artifacts expire. Before expiry, save reviewed, sanitized copies into this directory with the run URL and commit SHA. Screenshots of a green icon without a run link or commit are weak evidence.

## Evidence record template

```text
Date (UTC):
Git commit:
Environment and host RAM:
Image digests:
Command / workflow run URL:
Expected behavior:
Observed behavior:
Result: PASS / FAIL / NOT RUN
Sanitized artifact path:
Known limitation:
```

Recommended filenames: `compose-smoke.json`, `minikube-smoke.json`, `synthetic-document.png`, `restart-persistence.md`, `restore-drill.md`, `resource-snapshot.md`, `image-scan-summary.md`. These are suggestions, not files claimed to exist.

## Before committing evidence

Inspect every file manually. Remove credentials, tokens, secret YAML, environment dumps, state files, real document contents, private hostnames and personal account identifiers. Do not rely on automatic redaction alone. Keep raw backups/logs privately. Never fabricate screenshot content, uptime, users, performance gains, deployment counts or restore times.
