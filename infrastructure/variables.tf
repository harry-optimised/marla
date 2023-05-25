
variable "ec2_instance_type" {
  description = "Instance type for the EC2 instance"
  default     = "t2.medium"
}

variable "ec2_ami_id" {
  description = "AMI id for the EC2 instance"
  default     = "ami-0ffa2060fccd67983"
}

variable "rds_instance_class" {
  description = "DB instance class for RDS"
  default     = "db.t2.micro"
}

variable "db_username" {
  description = "Username for the RDS database"
}

variable "db_password" {
  description = "Password for the RDS database"
}


variable "subdomain" {
  default = "marla"
}

