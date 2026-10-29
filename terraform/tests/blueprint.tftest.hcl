# Terraform >=1.7 mock provider: no credentials, API calls, or cloud resources.
mock_provider "google" {
  mock_resource "google_service_account" {
    defaults = { email = "paperless-node@portfolio-test-project.iam.gserviceaccount.com" }
  }
}

run "disabled_by_default" {
  command = plan
  assert {
    condition     = output.deployment_enabled == false && length(module.gke) == 0 && length(module.network) == 0 && length(module.registry) == 0 && length(google_project_service.apis) == 0
    error_message = "Default configuration must not create cloud resources."
  }
}

run "reject_public_control_plane" {
  command = plan
  variables { admin_cidr = "0.0.0.0/0" }
  expect_failures = [var.admin_cidr]
}

run "require_deployment_inputs" {
  command = plan
  variables {
    enable_deployment = true
    admin_cidr        = "203.0.113.10/32"
  }
  expect_failures = [terraform_data.guard]
}

run "enabled_blueprint_mock" {
  command = apply
  variables {
    enable_deployment = true
    project_id        = "portfolio-test-project"
    admin_cidr        = "203.0.113.10/32"
  }
  assert {
    condition     = output.cluster_name == "paperless-lab" && output.registry_url == "europe-west3-docker.pkg.dev/portfolio-test-project/paperless-lab"
    error_message = "Module outputs must compose into the expected cluster and registry."
  }
}
