locals {
  data_lake_bucket = "d_lake"
}

variable "project" {
  description = "Your GCP Project ID"
  type = string
  default = "gold-totem-359211"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations/"
  type = string
  default = "europe-central2"
}

variable "zone" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations/"
  type = string
  default = "europe-central2-a"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  type = string
  default = "STANDARD"
}

variable "vm_image" {
  description = "Base image for your Virtual Machine."
  type = string
  default = "ubuntu-os-cloud/ubuntu-2004-lts"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "police_data"
}

variable "dbt_stg_dataset" {
  description = "BigQuery Dataset for storing dbt staging models"
  type = string
  default = "police_staging"
}

variable "dbt_core_dataset" {
  description = "BigQuery Dataset for storing dbt production models"
  type = string
  default = "police_production"
}