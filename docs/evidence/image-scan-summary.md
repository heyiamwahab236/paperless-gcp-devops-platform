# Image security scan — 29 October 2026

**Completed; vulnerability gate FAILED.** All three pinned images were scanned with Trivy 0.76.1 directly from public registries. Containers were not started. CycloneDX SBOMs were generated for each image. `scan_images.py` returned exit code 1 because HIGH/CRITICAL findings were present; this was not a scanner execution failure.

| Image | HIGH matches | CRITICAL matches | Unique advisory IDs | Matches listing a fixed version |
|---|---:|---:|---:|---:|
| paperless-ngx | 279 | 11 | 92 | 14 |
| postgres | 86 | 2 | 43 | 26 |
| valkey | 0 | 0 | 0 | 0 |

Counts are package/advisory matches at the selected severities. One advisory can appear against several packages. Unique IDs are distinct within each image, not necessarily distinct across images. Fixed-version metadata is advisory information, not proof that a tested upstream image containing that fix is available.

Download [full reports and SBOMs](security-reports.zip), or inspect the [machine-readable summary](security-summary.json). The ZIP also contains the Kubernetes, Terraform-module and committed-secret reports, plus SHA-256 hashes. These contain package/configuration metadata, not application documents or local credentials. Image digests are in the summary and repository lock.

## Triage decision

Access remains limited to localhost with synthetic documents while these findings are unresolved. Prioritize the CRITICAL matches, review upstream/vendor advisories and package reachability, then test patched upstream image digests when available. Update images through their upstream releases and re-run scans and runtime checks. Record the scope, reason, reviewer, and expiry date for any future exception.

The image workflow includes unfixed vulnerabilities and has no blanket suppressions. Its gate is expected to fail for these digests until the findings are resolved or explicitly triaged through a reviewed policy change. The separate configuration-validation workflow has different checks and can pass while the image gate fails.

## Interpretation limits

Trivy warned that third-party SBOM metadata can affect detection accuracy and that some severities come from other vendors. Findings need advisory review; they are not evidence of an exploit against this deployment. Zero HIGH/CRITICAL matches for an image is not proof of security, and lower severities were outside this report. Scanner databases, fixed-version metadata and upstream images evolve. SBOM generation is inventory generation, not an additional vulnerability scan.

Runtime startup, ingestion, persistence and restore remain unverified because the Docker engine was unavailable. These image scans do not close that gap. See [the full validation record](VALIDATION.md).
