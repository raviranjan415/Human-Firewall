# ==============================================================================
# Human Firewall — Security Groups & Firewall Rules (Zero Trust Segmentation)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Edge Load Balancer Security Group (Public Ingress)
# ------------------------------------------------------------------------------
resource "aws_security_group" "lb" {
  name        = "human-firewall-${var.environment}-lb-sg"
  description = "Ingress control for Nginx Edge Load Balancer"
  vpc_id      = aws_vpc.main.id

  # Inbound HTTP
  ingress {
    description = "Allow HTTP from world"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound HTTPS
  ingress {
    description = "Allow HTTPS from world"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound to Application Cluster
  egress {
    description = "Allow outbound to app replicas"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "human-firewall-${var.environment}-lb-sg"
    Role = "LoadBalancer"
  }
}

# ------------------------------------------------------------------------------
# 2. Application Cluster Security Group (Internal Flask Replicas)
# ------------------------------------------------------------------------------
resource "aws_security_group" "app" {
  name        = "human-firewall-${var.environment}-app-sg"
  description = "Ingress control for Flask application replicas"
  vpc_id      = aws_vpc.main.id

  # Traffic from Load Balancer only
  ingress {
    description     = "Allow traffic from load balancer on WSGI port"
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = [aws_security_group.lb.id]
  }

  # SSH Access for Ansible Automation
  ingress {
    description = "Allow SSH from authorized CIDR for Ansible automation"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidr
  }

  # Outbound to Database and Internet
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "human-firewall-${var.environment}-app-sg"
    Role = "Application"
  }
}

# ------------------------------------------------------------------------------
# 3. Data Tier Security Group (Zero Public Exposure)
# ------------------------------------------------------------------------------
resource "aws_security_group" "data" {
  name        = "human-firewall-${var.environment}-data-sg"
  description = "Strict ingress control for PostgreSQL and Redis"
  vpc_id      = aws_vpc.main.id

  # PostgreSQL Access (Port 5432 from App Replicas only)
  ingress {
    description     = "Allow PostgreSQL access strictly from app replicas"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # Redis Access (Port 6379 from App Replicas only)
  ingress {
    description     = "Allow Redis access strictly from app replicas"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # Outbound restricted
  egress {
    description = "Allow internal outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.vpc_cidr]
  }

  tags = {
    Name = "human-firewall-${var.environment}-data-sg"
    Role = "DataTier"
  }
}

