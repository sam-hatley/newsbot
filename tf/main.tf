terraform {
  required_version = ">= 1.3.7"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}

// Uploading files to google storage
resource "random_id" "default" {
  byte_length = 8
}

resource "google_storage_bucket" "default" {
  name                        = "${random_id.default.hex}-gcf-source" # Every bucket name must be globally unique
  location                    = var.region
  uniform_bucket_level_access = true
}

data "archive_file" "default" {
  type        = "zip"
  output_path = "/tmp/function-source.zip"
  source_dir  = "../src/"
}

resource "google_storage_bucket_object" "object" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.default.name
  source = data.archive_file.default.output_path # Add path to the zipped function source code
}


// Create Cloud Function
resource "google_cloudfunctions2_function" "default" {
  name        = "${var.project_name}-function"
  location    = var.region
  description = "a new function"

  build_config {
    runtime     = "python311"
    entry_point = "main"
    environment_variables = {
      MASTODON_TOKEN = var.mastodon_access_token
      MASTODON_ID    = var.mastodon_id
    }
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "64M"
    timeout_seconds    = 60
  }
}

output "function_uri" {
  value = google_cloudfunctions2_function.default.service_config[0].uri
}


// Schedule function
resource "google_cloud_scheduler_job" "job" {
  name             = "test-job"
  description      = "test http job"
  schedule         = "*/8 * * * *"
  time_zone        = "America/New_York"
  attempt_deadline = "320s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.default.service_config[0].uri
    body        = base64encode("{\"foo\":\"bar\"}")
  }
}
