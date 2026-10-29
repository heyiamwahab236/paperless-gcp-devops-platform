variable "project_id" { type = string }
variable "name" { type = string }
variable "zone" { type = string }
variable "network_id" { type = string }
variable "subnet_id" { type = string }
variable "admin_cidr" {
  type = string
  validation {
    condition     = can(cidrnetmask(var.admin_cidr)) && endswith(var.admin_cidr, "/32")
    error_message = "A single operator IPv4 /32 is required."
  }
}
variable "deletion_protection" {
  type    = bool
  default = true
}
variable "machine_type" {
  type    = string
  default = "e2-standard-2"
}
variable "master_cidr" {
  type    = string
  default = "172.16.0.0/28"
}
