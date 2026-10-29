resource "google_artifact_registry_repository" "this" {
  project       = var.project_id
  location      = var.region
  repository_id = var.name
  description   = "Optional upstream image mirror for the Paperless operations lab"
  format        = "DOCKER"
  labels        = { purpose = "portfolio", environment = "sandbox" }
  docker_config { immutable_tags = true }
}

resource "google_artifact_registry_repository_iam_member" "reader" {
  project    = var.project_id
  location   = var.region
  repository = google_artifact_registry_repository.this.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${var.node_service_email}"
}
