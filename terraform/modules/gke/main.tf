resource "google_service_account" "node" {
  project      = var.project_id
  account_id   = "${var.name}-node"
  display_name = "Paperless lab GKE nodes"
}

resource "google_project_iam_member" "node" {
  project = var.project_id
  role    = "roles/container.defaultNodeServiceAccount"
  member  = "serviceAccount:${google_service_account.node.email}"
}

resource "google_container_cluster" "this" {
  project                  = var.project_id
  name                     = var.name
  location                 = var.zone
  network                  = var.network_id
  subnetwork               = var.subnet_id
  initial_node_count       = 1
  remove_default_node_pool = true
  deletion_protection      = var.deletion_protection
  networking_mode          = "VPC_NATIVE"
  enable_shielded_nodes    = true
  datapath_provider        = "ADVANCED_DATAPATH"
  resource_labels          = { purpose = "portfolio", environment = "sandbox" }
  release_channel { channel = "REGULAR" }
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = var.master_cidr
  }
  master_authorized_networks_config {
    gcp_public_cidrs_access_enabled = false
    cidr_blocks {
      cidr_block   = var.admin_cidr
      display_name = "operator"
    }
  }
  workload_identity_config { workload_pool = "${var.project_id}.svc.id.goog" }
  master_auth {
    client_certificate_config { issue_client_certificate = false }
  }
  logging_config { enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"] }
  monitoring_config { enable_components = ["SYSTEM_COMPONENTS"] }
  addons_config {
    gce_persistent_disk_csi_driver_config { enabled = true }
  }
  # Also secure the temporary pool that GKE creates before removing it.
  node_config {
    service_account = google_service_account.node.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]
    machine_type    = var.machine_type
    disk_size_gb    = 30
    disk_type       = "pd-standard"
    image_type      = "COS_CONTAINERD"
    metadata        = { disable-legacy-endpoints = "true" }
    workload_metadata_config { mode = "GKE_METADATA" }
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
  }
  depends_on = [google_project_iam_member.node]
}

resource "google_container_node_pool" "this" {
  project    = var.project_id
  name       = "${var.name}-pool"
  location   = var.zone
  cluster    = google_container_cluster.this.name
  node_count = 1
  management {
    auto_repair  = true
    auto_upgrade = true
  }
  # A spare node can briefly be billed during a managed upgrade.
  upgrade_settings {
    max_surge       = 1
    max_unavailable = 0
  }
  node_config {
    machine_type    = var.machine_type
    disk_size_gb    = 30
    disk_type       = "pd-standard"
    image_type      = "COS_CONTAINERD"
    service_account = google_service_account.node.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]
    metadata        = { disable-legacy-endpoints = "true" }
    workload_metadata_config { mode = "GKE_METADATA" }
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
  }
}
