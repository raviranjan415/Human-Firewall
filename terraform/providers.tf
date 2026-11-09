# ==============================================================================
# Human Firewall — Cloud Provider Configuration
# ==============================================================================

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Human Firewall"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Course      = "INT333 DevOps Configuration Management"
      Owner       = var.owner
    }
  }

  # Allows validation and planning without active cloud credentials when using mocks/dry-run
  skip_credentials_validation = var.skip_credentials_validation
  skip_metadata_api_check     = var.skip_metadata_api_check
  skip_requesting_account_id  = var.skip_requesting_account_id
}

