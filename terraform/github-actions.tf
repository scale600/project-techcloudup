# ── GitHub Actions → GCP deployment (Workload Identity Federation) ──
#
# Provisions an OIDC-based Workload Identity pool + a dedicated deployer
# service account so `.github/workflows/deploy.yml` can build/push/deploy
# the health-checker to Cloud Run without any long-lived service-account key.
#
# After `terraform apply`, the deterministic resource names are:
#   WIF provider : projects/<number>/locations/global/workloadIdentityPools/github-actions/providers/github-actions
#   SA email     : github-actions@<project_id>.iam.gserviceaccount.com
# (These match the GitHub secrets GCP_WIF_PROVIDER / GCP_SA_EMAIL.)

resource "google_iam_workload_identity_pool" "github" {
  project                   = var.project_id
  workload_identity_pool_id = "github-actions"
  display_name              = "GitHub Actions"
  description               = "OIDC pool for GitHub Actions deploys"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-actions"
  display_name                       = "GitHub Actions OIDC"
  description                        = "Trusts GitHub Actions OIDC tokens for scale600/project-techcloudup"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  attribute_condition = "assertion.repository == 'scale600/project-techcloudup'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Dedicated deployer service account (no key needed — used via WIF).
resource "google_service_account" "github_actions" {
  account_id   = "github-actions"
  display_name = "GitHub Actions deployer"
  project      = var.project_id
}

# Allow GitHub Actions (only this repo) to impersonate the deployer SA.
resource "google_service_account_iam_member" "github_wif" {
  service_account_id = google_service_account.github_actions.name
  role               = "roles/iam.workloadIdentityUser"
  member = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/scale600/project-techcloudup"
}

# Deployer can update the Cloud Run service.
resource "google_project_iam_member" "github_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

# Deployer can push images to Artifact Registry.
resource "google_project_iam_member" "github_ar_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

# Deployer can act as the runtime (compute) service account when deploying.
resource "google_service_account_iam_member" "github_act_as_compute" {
  service_account_id = "${data.google_project.this.number}-compute@developer.gserviceaccount.com"
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.github_actions.email}"
}
