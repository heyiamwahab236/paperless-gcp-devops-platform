# Validation checklist

Track static checks, runtime tests, and recovery exercises here. Completed checks are documented in the dated [validation record](VALIDATION.md); runtime checks remain pending.

## Static validation

- [x] Original Compose and Helm configuration with clear upstream attribution.
- [x] Immutable image references checked against the public registries.
- [x] Compose configuration validation.
- [x] Helm lint, render, Kubernetes schema and custom policy checks.
- [x] Python regression tests for credential handling and deployment policies.
- [x] Terraform formatting, provider validation and mocked tests.
- [x] GitHub Actions workflow syntax validation.
- [x] Current-version Kubernetes/Terraform configuration audit; findings documented.
- [x] Local image vulnerability scans and SBOMs for all three digests; findings retained, gate failed.

These results were collected locally. See the validation record for tool versions and scan findings.

## Runtime and recovery

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

## GitHub Actions

- [ ] Complete `Validate` for the current commit and record its run URL.
- [ ] Run `Runtime demo` once for `compose` and once for `minikube`; retain real artifacts.
- [ ] Run `Image security`; record the date, image digests, findings and remediation decisions.
- [ ] Retain configuration-audit findings and explain lab exceptions.

GitHub workflow artifacts expire. Save reviewed, sanitized results into this directory with the run URL and commit SHA when a longer retention period is needed.

## Test record template

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

Use descriptive filenames such as `compose-smoke.json`, `minikube-smoke.json`, `restart-persistence.md`, `restore-drill.md`, and `resource-snapshot.md` for new test results.

## Handling test artifacts

Review artifacts before committing. Remove credentials, tokens, secret YAML, environment dumps, state files, real document contents, private hostnames, and personal account identifiers. Keep raw backups and logs in private storage.
