variable "environment" { default = "dev" }
variable "aws_region" { default = "us-east-1" }
variable "instance_type" { default = "t3.micro" }
variable "app_replica_count" { default = 1 }
variable "vpc_cidr" { default = "10.10.0.0/16" }

