variable "project" {
  description = "Project Name"
  default     = "newsbot-392213"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "us-west1"
  type        = string
}

variable "deployment_name" {
  description = "The name of this particular deployment, will get added as a prefix to most resources."
  default     = "newsbot"
  type        = string
}

variable "mastodon_access_token" {
  type        = string
  description = "Access token for Mastodon"
  sensitive   = true
}

variable "mastodon_id" {
  type        = string
  description = "Mastodon username"
  default     = "110678067712784209" #i.e., '@username@mastodon.social' or '123456789123456789'
}
