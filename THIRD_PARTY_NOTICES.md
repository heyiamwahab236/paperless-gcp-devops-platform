# Attribution and licenses

This independent deployment and operations repository is not affiliated with the Paperless-ngx project. Its configuration, automation, tests, diagrams, and documentation are offered under the [MIT License](LICENSE). Upstream applications, container contents, trademarks, and third-party license texts retain their own terms.

| Dependency | Role | Upstream license / source |
|---|---|---|
| Paperless-ngx 3.3.4 | Unmodified document-management workload | GPL-3.0-only, explicitly declared in the [tagged Dockerfile](https://github.com/paperless-ngx/paperless-ngx/blob/v3.3.4/Dockerfile); [source](https://github.com/paperless-ngx/paperless-ngx/tree/v3.3.4), [license copy](LICENSES/GPL-3.0-only.txt) |
| PostgreSQL 18 image | Metadata database | PostgreSQL License; [COPYRIGHT](https://github.com/postgres/postgres/blob/REL_18_STABLE/COPYRIGHT), [license copy](LICENSES/PostgreSQL.txt) |
| Valkey 9 image | Redis-compatible queue broker | BSD 3-Clause for Valkey core; [COPYING](https://github.com/valkey-io/valkey/blob/9.0/COPYING), [license copy](LICENSES/Valkey-BSD-3-Clause.txt) |

Paperless-ngx is developed by its upstream maintainers and contributors. This repository uses their published container unchanged. The service topology and configuration keys follow the official documentation.

License texts in `LICENSES/` retain their upstream terms. A container also includes operating-system packages and libraries under additional licenses; the table is **not a complete container license inventory**. The image-security workflow emits CycloneDX SBOMs for inspection. Refer to the source and notices associated with each image digest.

This repository distributes configuration references, not container image archives. If you later redistribute modified upstream code or mirror/distribute images, review and satisfy the applicable license and corresponding-source obligations for that distribution. A project MIT file or attribution paragraph does not remove them.

Tools are downloaded separately. Terraform 1.13.5 has its own [Business Source License](https://github.com/hashicorp/terraform/blob/v1.13.5/LICENSE); the Google provider is [MPL-2.0](https://github.com/hashicorp/terraform-provider-google/blob/main/LICENSE). Docker Desktop has separate product terms. Helm, Kubernetes, Minikube, Trivy, actionlint, kubeconform and Actions retain their respective upstream licenses. Documentation links are in [sources](docs/sources.md).
