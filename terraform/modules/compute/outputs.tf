output "replica_ids" {
  value = aws_instance.replicas[*].id
}

output "replica_private_ips" {
  value = aws_instance.replicas[*].private_ip
}

