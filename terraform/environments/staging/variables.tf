variable "environment" { default = "staging" }
variable "aws_region" { default = "us-east-1" }
variable "instance_type" { default = "t3.small" }
variable "app_replica_count" { default = 2 }
variable "vpc_cidr" { default = "10.20.0.0/16" }

