resource "aws_instance" "replicas" {
  count                  = var.replica_count
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_ids[count.index % length(var.subnet_ids)]
  vpc_security_group_ids = var.security_group_ids
  key_name               = var.key_name

  tags = {
    Name        = "hf-${var.environment}-module-replica-${count.index + 1}"
    Environment = var.environment
  }
}

