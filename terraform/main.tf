terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
  backend "local" {}
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ── Data sources (pre-existing resources) ──────────────────────────

data "google_project" "this" {
  project_id = var.project_id
}

data "google_artifact_registry_repository" "docker" {
  location      = var.region
  repository_id = "health-checker"
}

# ── Cloud Run service ──────────────────────────────────────────────

resource "google_cloud_run_v2_service" "health_checker" {
  name     = "health-checker"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }
    containers {
      image = "${data.google_artifact_registry_repository.docker.location}-docker.pkg.dev/${var.project_id}/${data.google_artifact_registry_repository.docker.repository_id}/health-checker:latest"
      env {
        name  = "GCP_PROJECT"
        value = var.project_id
      }
      resources {
        limits = {
          cpu    = "1"
          memory = "256Mi"
        }
      }
    }
    timeout         = "300s"
    service_account = data.google_project.this.number == 0 ? "" : "${data.google_project.this.number}-compute@developer.gserviceaccount.com"
  }

  depends_on = [data.google_project.this]
}

# Allow unauthenticated access
resource "google_cloud_run_v2_service_iam_member" "public" {
  location = google_cloud_run_v2_service.health_checker.location
  project  = google_cloud_run_v2_service.health_checker.project
  name     = google_cloud_run_v2_service.health_checker.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ── Cloud Scheduler ────────────────────────────────────────────────

resource "google_cloud_scheduler_job" "health_check" {
  name             = "health-check-cron"
  region           = var.region
  schedule         = "*/5 * * * *"
  time_zone        = "Etc/UTC"
  attempt_deadline = "300s"

  http_target {
    http_method = "GET"
    uri         = "${google_cloud_run_v2_service.health_checker.uri}check-all"
    headers = {
      "User-Agent" = "Google-Cloud-Scheduler"
    }
  }
}

# ── IAM: compute SA can read/write Firestore ────────────────────────

resource "google_project_iam_member" "compute_firestore" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${data.google_project.this.number}-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "compute_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${data.google_project.this.number}-compute@developer.gserviceaccount.com"
}

# ── IAM: Cloud Build SA can push to Artifact Registry ──────────────

resource "google_project_iam_member" "cloudbuild_ar_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${data.google_project.this.number}@cloudbuild.gserviceaccount.com"
}
