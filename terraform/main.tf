# Default configuration has no managed cloud resources. CI uses a mock provider.
resource "terraform_data" "guard" {
  count = var.enable_deployment ? 1 : 0
  lifecycle {
    precondition {
      condition     = var.project_id != "paperless-blueprint-demo" && var.admin_cidr != ""
      error_message = "An actual project and operator IPv4 /32 are required for deployment."
    }
    precondition {
      condition     = startswith(var.zone, "${var.region}-")
      error_message = "zone must belong to region."
    }
  }
}

resource "google_project_service" "apis" {
  for_each = var.enable_deployment ? toset([
    "compute.googleapis.com", "container.googleapis.com", "iam.googleapis.com",
    "artifactregistry.googleapis.com", "logging.googleapis.com", "monitoring.googleapis.com"
  ]) : toset([])
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
  depends_on         = [terraform_data.guard]
}

module "network" {
  count      = var.enable_deployment ? 1 : 0
  source     = "./modules/network"
  project_id = var.project_id
  name       = var.name
  region     = var.region
  depends_on = [google_project_service.apis]
}

module "gke" {
  count               = var.enable_deployment ? 1 : 0
  source              = "./modules/gke"
  project_id          = var.project_id
  name                = var.name
  zone                = var.zone
  network_id          = module.network[0].network_id
  subnet_id           = module.network[0].subnet_id
  admin_cidr          = var.admin_cidr
  deletion_protection = var.deletion_protection
  depends_on          = [module.network]
}

module "registry" {
  count              = var.enable_deployment ? 1 : 0
  source             = "./modules/registry"
  project_id         = var.project_id
  name               = var.name
  region             = var.region
  node_service_email = module.gke[0].node_service_email
  depends_on         = [google_project_service.apis]
}
