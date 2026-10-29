output "deployment_enabled" {
  value       = var.enable_deployment
  description = "False in the delivered portfolio."
}

output "cluster_name" {
  value       = try(module.gke[0].cluster_name, null)
  description = "Name for a future gcloud get-credentials command."
}

output "cluster_location" {
  value = var.enable_deployment ? var.zone : null
}

output "registry_url" {
  value       = try(module.registry[0].url, null)
  description = "Optional future mirror destination; no images are copied automatically."
}
