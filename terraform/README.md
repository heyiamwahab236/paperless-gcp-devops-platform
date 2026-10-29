# Google Cloud deployment blueprint

**Status: configuration validated and tested with a mock provider; not deployed to Google Cloud.** With the default `enable_deployment = false`, local validation and mock tests require no project, billing account, service-account key, or GCP credentials.

## Module contracts

| Module | Inputs | Outputs / behavior |
|---|---|---|
| `modules/network` | project ID, name, region; optional subnet/pod/service CIDRs | Custom VPC, subnet with secondary ranges, Private Google Access, Cloud Router/NAT; exports network/subnet IDs |
| `modules/gke` | project ID, name, zone, network/subnet IDs, operator /32; optional machine type/master CIDR/deletion protection | One zonal private-node cluster/pool, Workload Identity, custom node account, PD CSI; exports name/node email |
| `modules/registry` | project ID, name, region, node email | Docker repository with immutable tags and scoped reader grant; exports registry URL |

The GKE module expects subnet secondary ranges named `pods` and `services`, as produced by the network module. Custom CIDRs must not overlap one another, the master `/28`, VPN routes or existing networks. Region/zone, quotas, org policy, Kubernetes availability, and IAM consistency require live verification before any future provisioning.

## Safe validation path

From repository root:

```bash
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform init -backend=false -input=false -lockfile=readonly
terraform -chdir=terraform validate
terraform -chdir=terraform test
```

`init` downloads the provider; it does not provision GCP. `validate` checks schemas. The test files declare a mock Google provider and include simulated plans/applies, default-off checks, input rejection, node/IAM/network checks, and composed outputs. Neither a real `plan` nor `apply` is included in CI. A real plan can require credentials/API access even with refresh disabled.

The root lock file includes hashes for Linux and Windows AMD64. When changing providers, use a reviewed upgrade and regenerate locks with `terraform providers lock -platform=linux_amd64 -platform=windows_amd64`, then rerun the tests.

## Optional cloud deployment

The following procedure provisions billable infrastructure and has not been executed. It is optional; local operation and validation do not depend on it.

1. Select an existing dedicated sandbox project with billing, quotas, a budget alert, and an authorized human identity. A budget alert is not a spending cap. Use Application Default Credentials from a short-lived human login or a scoped federated identity; do not create/download a service-account JSON key for Actions.
2. Review APIs and IAM permissions for the deploying identity. It needs permission to enable the listed project services, manage this VPC/NAT, create GKE resources, create the node service account and role grants, and manage the registry and its IAM. Org-policy restrictions may require additional review; do not default to granting project Owner. The runtime node role is separate from deployer permissions.
3. Configure an approved encrypted remote-state backend with locking and access control. This repository intentionally has no pre-created state bucket or bucket name. State, plan files, and `terraform.tfvars` are ignored. Do not commit credentials or state. The backend is a separate bootstrap prerequisite, not created implicitly here.
4. Copy `terraform.tfvars.example` to the ignored `terraform.tfvars`, enter the actual project, region/zone and current public operator IPv4 `/32`, and explicitly set `enable_deployment = true`. Review all CIDRs and existing resources. Reinitialize the chosen backend, then run a real `terraform plan -out=reviewed.tfplan` **from the terraform directory**. Inspect every resource and cost category before any separately authorized `terraform apply reviewed.tfplan`.
5. Obtain cluster credentials with `gcloud container clusters get-credentials CLUSTER_NAME --zone ZONE --project PROJECT_ID`, replacing the three values. Install the GKE auth plugin if required. Confirm the exact kubectl context and authorized network. Private nodes use NAT for public image downloads; no public app service is created.
6. Generate local secrets privately and use `python3 scripts/kube_secret.py --context ACTUAL_GKE_CONTEXT`. Deploy the chart with `helm upgrade --install demo helm/paperless --kube-context ACTUAL_GKE_CONTEXT -n paperless -f helm/values-gke.yaml --wait --timeout 15m`. The chart's `standard-rwo` disks, local-only URL and port-forward access are intended for a restricted sandbox. Create an admin and repeat smoke/persistence/restore exercises. No managed database, TLS ingress or internet-facing demo is supplied.
7. The registry is optional mirror infrastructure. It is empty; upstream image pulls work through NAT without it. Publishing a mirror is a separate process with source/license and provenance review. Workload Identity is enabled at cluster/node level, but the app gets no IAM binding or cloud permissions.

This blueprint targets a restricted sandbox. Google-managed API behavior, quotas, policy, network reachability, and IAM propagation require live verification and cannot be validated by mocks.

## Cost and teardown design

If enabled, expect charges for the GKE control plane as applicable, node VM and boot disk, app/DB/broker disks, NAT gateway and outbound traffic, logging/monitoring use, and any registry storage. Managed upgrades can briefly add a surge node. No prices or free-tier assumptions are encoded.

For an actual future teardown: export data off-cluster, uninstall the chart, inspect retained PVCs, and delete only the disposable PVCs after verifying backups. Then set `deletion_protection = false`, review and apply that specific change, and run a reviewed Terraform destroy against the same backend/state. Deletion protection cannot be bypassed merely by passing a value to `destroy`; it must first be updated in GKE. A deletion-protected cluster may leave partial resources if the teardown is rushed.

Inspect Compute disks, addresses, routers/NAT, Artifact Registry contents, snapshots, logging/storage and the billing dashboard afterward. Kubernetes-created disks are outside Terraform's state and may survive according to their reclaim policy. The project and APIs are intentionally retained (`disable_on_destroy = false`). Remote state/bootstrap storage is also separately managed. Deleting a cluster alone does not prove that billing has stopped.

References: [GKE node identity](https://docs.cloud.google.com/kubernetes-engine/security/configure-node-service-accounts), [Google Terraform provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs), [Terraform mock testing](https://developer.hashicorp.com/terraform/language/tests/mocking).
