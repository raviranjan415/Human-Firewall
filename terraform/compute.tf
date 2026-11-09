# ==============================================================================
# Human Firewall — Compute Instances (Load Balancer, Replicas, Database)
# ==============================================================================

# SSH Key Pair for Ansible & Administration
resource "aws_key_pair" "deployer" {
  key_name   = "human-firewall-${var.environment}-key"
  public_key = var.ssh_public_key

  tags = {
    Name = "human-firewall-${var.environment}-keypair"
  }
}

# Base Ubuntu Server 22.04 LTS AMI Data Source
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# ------------------------------------------------------------------------------
# 1. Edge Nginx Load Balancer (Public DMZ)
# ------------------------------------------------------------------------------
resource "aws_instance" "load_balancer" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.small"
  subnet_id                   = aws_subnet.public[0].id
  vpc_security_group_ids      = [aws_security_group.lb.id]
  key_name                    = aws_key_pair.deployer.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name = "human-firewall-${var.environment}-lb"
    Role = "loadbalancer"
  }
}

# ------------------------------------------------------------------------------
# 2. Flask Application Replicas
# ------------------------------------------------------------------------------
resource "aws_instance" "app_replicas" {
  count                       = var.app_replica_count
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = var.deploy_in_public_subnets ? aws_subnet.public[count.index % length(aws_subnet.public)].id : aws_subnet.private[count.index % length(aws_subnet.private)].id
  vpc_security_group_ids      = [aws_security_group.app.id]
  key_name                    = aws_key_pair.deployer.key_name
  associate_public_ip_address = var.deploy_in_public_subnets

  root_block_device {
    volume_size           = 15
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name    = "human-firewall-${var.environment}-replica-${count.index + 1}"
    Role    = "app_replica"
    Replica = tostring(count.index + 1)
  }
}

# ------------------------------------------------------------------------------
# 3. Dedicated Database Host (PostgreSQL & Redis)
# ------------------------------------------------------------------------------
resource "aws_instance" "database" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = var.deploy_in_public_subnets ? aws_subnet.public[0].id : aws_subnet.private[0].id
  vpc_security_group_ids      = [aws_security_group.data.id]
  key_name                    = aws_key_pair.deployer.key_name
  associate_public_ip_address = var.deploy_in_public_subnets

  root_block_device {
    volume_size           = 15
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name = "human-firewall-${var.environment}-db"
    Role = "database"
  }
}

