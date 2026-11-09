variable "environment" { default = "production" }
variable "aws_region" { default = "us-east-1" }
variable "instance_type" { default = "t3.medium" }
variable "app_replica_count" { default = 3 }
variable "vpc_cidr" { default = "10.0.0.0/16" }

