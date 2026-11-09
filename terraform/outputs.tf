# ==============================================================================
# Human Firewall — Terraform Infrastructure Outputs
# Consumed directly by Ansible dynamic inventory generator
# ==============================================================================

output "vpc_id" {
  description = "Identifier of the created VPC"
  value       = aws_vpc.main.id
}

output "load_balancer_public_ip" {
  description = "Public IP address of the Edge Nginx Load Balancer"
  value       = aws_instance.load_balancer.public_ip
}

output "load_balancer_private_ip" {
  description = "Private IP address of the Edge Nginx Load Balancer"
  value       = aws_instance.load_balancer.private_ip
}

output "app_replica_private_ips" {
  description = "List of private IP addresses for Flask application replicas"
  value       = aws_instance.app_replicas[*].private_ip
}

output "database_private_ip" {
  description = "Private IP address of the PostgreSQL database host"
  value       = aws_instance.database.private_ip
}

output "app_url" {
  description = "Public URL of the Human Firewall application"
  value       = "http://${aws_instance.load_balancer.public_ip}"
}

output "app_replica_public_ips" {
  description = "List of public IP addresses for Flask application replicas"
  value       = aws_instance.app_replicas[*].public_ip
}

output "app_replica_count" {
  description = "Number of active provisioned application replicas"
  value       = length(aws_instance.app_replicas)
}

# ------------------------------------------------------------------------------
# Structured Machine-Readable Inventory for Ansible Orchestration
# ------------------------------------------------------------------------------
output "ansible_inventory" {
  description = "JSON-compatible inventory structure for Ansible integration"
  value = {
    loadbalancers = [
      {
        name       = aws_instance.load_balancer.tags["Name"]
        public_ip  = aws_instance.load_balancer.public_ip
        private_ip = aws_instance.load_balancer.private_ip
      }
    ]
    webservers = [
      for idx, inst in aws_instance.app_replicas : {
        name       = inst.tags["Name"]
        public_ip  = inst.public_ip
        private_ip = inst.private_ip
        replica_id = idx + 1
      }
    ]
    dbservers = [
      {
        name       = aws_instance.database.tags["Name"]
        public_ip  = aws_instance.database.public_ip
        private_ip = aws_instance.database.private_ip
      }
    ]
  }
}

