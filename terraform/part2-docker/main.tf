# Experiment 6 - Part 2: run the Streamlit ML app as a Docker container via Terraform.
# Prerequisite: the image student-pass-app:1.0 was built in Experiment 5
#   (docker build -t student-pass-app:1.0 .  from the project root)
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Windows Docker Desktop: if init/plan cannot reach Docker, use
#   provider "docker" { host = "npipe:////./pipe/docker_engine" }
provider "docker" {}

variable "host_port" {
  description = "Port on your machine where the app is published"
  type        = number
  default     = 8081
}

resource "docker_image" "app" {
  name         = "student-pass-app:1.0"
  keep_locally = true
}

resource "docker_container" "web" {
  name  = "terraform-student-app"
  image = docker_image.app.image_id

  ports {
    internal = 8501
    external = var.host_port
  }
}

output "website_url" {
  description = "URL for the Streamlit ML app"
  value       = "http://localhost:${var.host_port}"
}
