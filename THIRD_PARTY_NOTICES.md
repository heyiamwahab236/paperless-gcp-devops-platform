# Attribution and licenses

This is an independent deployment and operations portfolio, not an official Paperless-ngx distribution or endorsement. The original configuration, automation, tests, diagrams and documentation in this repository are offered under the [MIT License](LICENSE). That license does not relicense upstream applications, their container contents, trademarks or third-party license texts.

| Dependency | Role | Upstream license / source |
|---|---|---|
| Paperless-ngx 3.3.4 | Unmodified document-management workload | GPL-3.0-only, explicitly declared in the [tagged Dockerfile](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/Dockerfile); [source](https://github.com/paperless-ngx/paperless-ngx/tree/v3.3.4), [license copy](LICENSES/GPL-3.0-only.txt) |
| PostgreSQL 18 image | Metadata database | PostgreSQL License; [COPYRIGHT](https://github.com/postgres/postgres/blob/REL_18_STABLE/COPYRIGHT), [license copy](LICENSES/PostgreSQL.txt) |
| Valkey 9 image | Redis-compatible queue broker | BSD 3-Clause for Valkey core; [COPYING](https://github.com/valkey-io/valkey/blob/9.0/COPYING), [license copy](LICENSES/Valkey-BSD-3-Clause.txt) |

Paperless-ngx's maintainers and contributors created the web interface, OCR integration, document processing, API and application behavior. This repository consumes the published container; it does not vendor or modify that application source. The service topology and configuration keys were checked against the official documentation. Repository files were authored as the operations layer for this portfolio rather than presenting upstream application code as original work.

License texts in `LICENSES/` retain their upstream terms. A container also includes operating-system packages and libraries under additional licenses; the table is **not a complete container license inventory**. The image-security workflow emits CycloneDX SBOMs for inspection. Refer to the source and notices associated with each image digest.

This repository distributes configuration references, not container image archives. If you later redistribute modified upstream code or mirror/distribute images, review and satisfy the applicable license and corresponding-source obligations for that distribution. A project MIT file or attribution paragraph does not remove them.

Tools are not bundled in the deliverable. Terraform 1.13.5 has its own [Business Source License](https://github.com/hashicorp/terraform/blob/v1.13.5/LICENSE); the Google provider is [MPL-2.0](https://github.com/hashicorp/terraform-provider-google/blob/main/LICENSE). Docker Desktop has separate product terms. Helm, Kubernetes, Minikube, Trivy, actionlint, kubeconform and Actions retain their respective upstream licenses. Documentation links are in [sources](docs/sources.md).
