variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "project-8ea04b35-82af-4a8d-845"
}

variable "region" {
  description = "GCP region for Cloud Run, Artifact Registry, and Scheduler"
  type        = string
  default     = "us-central1"
}
