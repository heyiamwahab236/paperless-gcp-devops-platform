variable "project_id" { type = string }
variable "name" { type = string }
variable "region" { type = string }
variable "subnet_cidr" {
  type    = string
  default = "10.40.0.0/24"
}
variable "pod_cidr" {
  type    = string
  default = "10.44.0.0/16"
}
variable "service_cidr" {
  type    = string
  default = "10.48.0.0/20"
}
