variable "enable_deployment" {
  description = "Explicit opt-in to billable resources. Keep false for this portfolio."
  type        = bool
  default     = false
}

variable "project_id" {
  description = "Existing Google Cloud project; never created or billed by validation."
  type        = string
  default     = "paperless-blueprint-demo"
}

variable "name" {
  description = "Prefix for this independently deployable sandbox."
  type        = string
  default     = "paperless-lab"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,19}$", var.name))
    error_message = "Use 3-20 lowercase letters, numbers or hyphens, starting with a letter."
  }
}

variable "region" {
  type        = string
  description = "GCP region, configurable to meet location requirements."
  default     = "europe-west3"
}

variable "zone" {
  type        = string
  description = "One zone inside region; avoids accidental regional node multiplication."
  default     = "europe-west3-a"
}

variable "admin_cidr" {
  type        = string
  description = "Future operator's public IPv4 /32 for the control plane. Empty while disabled."
  default     = ""
  validation {
    condition     = var.admin_cidr == "" || (can(cidrnetmask(var.admin_cidr)) && endswith(var.admin_cidr, "/32"))
    error_message = "Use a single IPv4 /32, never 0.0.0.0/0."
  }
}

variable "deletion_protection" {
  type        = bool
  description = "Protect GKE from accidental deletion; must be disabled deliberately before teardown."
  default     = true
}
