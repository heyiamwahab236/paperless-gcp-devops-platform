mock_provider "google" {
  mock_resource "google_service_account" {
    defaults = { email = "paperless-node@portfolio-test-project.iam.gserviceaccount.com" }
  }
}
run "private_single_zone_nodes" {
  command = plan
  module { source = "./modules/gke" }
  variables {
    project_id = "portfolio-test-project"
    name       = "paperless-lab"
    zone       = "europe-west3-a"
    network_id = "projects/portfolio-test-project/global/networks/paperless-lab"
    subnet_id  = "projects/portfolio-test-project/regions/europe-west3/subnetworks/paperless-lab"
    admin_cidr = "203.0.113.10/32"
  }
  assert {
    condition     = google_container_cluster.this.private_cluster_config[0].enable_private_nodes && google_container_cluster.this.deletion_protection
    error_message = "Private nodes and deletion protection are required."
  }
  assert {
    condition     = google_container_node_pool.this.node_count == 1 && google_container_node_pool.this.location == "europe-west3-a"
    error_message = "Use exactly one zonal node, not one node per region zone."
  }
  assert {
    condition     = google_project_iam_member.node.role == "roles/container.defaultNodeServiceAccount" && google_container_node_pool.this.node_config[0].workload_metadata_config[0].mode == "GKE_METADATA"
    error_message = "Use the scoped node role and Workload Identity metadata."
  }
}
