# ==============================================================================
# Human Firewall — Root Variables
# ==============================================================================

variable "aws_region" {
  description = "Target cloud region for Human Firewall infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Target deployment tier (dev, staging, production)"
  type        = string
  default     = "production"
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be one of: dev, staging, production."
  }
}

variable "owner" {
  description = "Resource administrator identifier"
  type        = string
  default     = "DevOps Architect"
}

# ------------------------------------------------------------------------------
# Network Topology Variables
# ------------------------------------------------------------------------------
variable "vpc_cidr" {
  description = "CIDR block for the dedicated Human Firewall VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public DMZ subnets (Ingress / Nginx)"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private application subnets (Replicas & Database)"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

# ------------------------------------------------------------------------------
# Compute & Replicas
# ------------------------------------------------------------------------------
variable "instance_type" {
  description = "Compute instance tier for Flask application replicas"
  type        = string
  default     = "t3.micro"
}

variable "deploy_in_public_subnets" {
  description = "Place instances in public subnets with direct internet access (Free Tier friendly, avoids $32/mo NAT Gateway)"
  type        = bool
  default     = true
}

variable "app_replica_count" {
  description = "Number of active Flask application replicas to provision"
  type        = number
  default     = 2
  validation {
    condition     = var.app_replica_count >= 1 && var.app_replica_count <= 10
    error_message = "Application replica count must be between 1 and 10."
  }
}

variable "ssh_public_key" {
  description = "SSH public key content for administrative Bastion / Ansible access"
  type        = string
  default     = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleDevOpsKeyHumanFirewall2026 devops@humanfirewall.local"
}

variable "allowed_ssh_cidr" {
  description = "Permitted CIDR range for administrative SSH management"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# ------------------------------------------------------------------------------
# Offline / Validation Switches
# ------------------------------------------------------------------------------
variable "skip_credentials_validation" {
  description = "Skip AWS credential verification for offline terraform validate/plan"
  type        = bool
  default     = true
}

variable "skip_metadata_api_check" {
  description = "Skip AWS metadata API check"
  type        = bool
  default     = true
}

variable "skip_requesting_account_id" {
  description = "Skip querying AWS account ID"
  type        = bool
  default     = true
}

