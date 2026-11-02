# Experiment 6 - Part 1: provider-neutral Terraform (creates nothing billable)
terraform {
  required_version = ">= 1.5.0"
}

variable "environment" {
  description = "Name of the environment being described"
  type        = string
  default     = "student-lab"
}

variable "app_name" {
  description = "Name of the ML application"
  type        = string
  default     = "student-pass-predictor"
}

locals {
  common_tags = {
    Environment = var.environment
    Application = var.app_name
    ManagedBy   = "Terraform"
    Purpose     = "MLOps-Lab"
  }
}

output "environment_name" {
  description = "Environment label for this lab"
  value       = var.environment
}

output "common_tags" {
  description = "Example metadata to apply to resources"
  value       = local.common_tags
}
