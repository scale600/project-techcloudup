output "dashboard_url" {
  description = "Public dashboard URL"
  value       = google_cloud_run_v2_service.health_checker.uri
}

output "scheduler_job_name" {
  description = "Cloud Scheduler job full name"
  value       = google_cloud_scheduler_job.health_check.name
}

output "project_number" {
  description = "GCP project number for SA references"
  value       = data.google_project.this.number
}
