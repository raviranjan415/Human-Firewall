# ==============================================================================
# Human Firewall — Terraform Root Configuration
# INT333 DevOps Advanced Configuration Management
# ==============================================================================

# Local values for standardized naming & tagging
locals {
  name_prefix = "human-firewall-${var.environment}"

  common_tags = {
    Project     = "Human Firewall"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Course      = "INT333"
  }
}

