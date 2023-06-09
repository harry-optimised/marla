resource "aws_instance" "ec2_instance" {
  ami           = var.ec2_ami_id
  instance_type = var.ec2_instance_type
  key_name      = aws_key_pair.my_key.key_name
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = {
    Name = "Chatbot_API_EC2_Instance"
  }
}

resource "aws_security_group" "ec2_sg" {
  name        = "ec2_sg"
  description = "Security group for the EC2 instance"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "rds_instance" {
  engine               = "mysql"
  identifier           = "marla"
  allocated_storage    =  10
  engine_version       = "5.7"
  instance_class       = var.rds_instance_class
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.mysql5.7"
  vpc_security_group_ids = ["${aws_security_group.rds_sg.id}"]
  skip_final_snapshot  = true
  publicly_accessible =  true
}

resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Security group for the RDS instance"

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "my_key" {
  key_name   = "my_key_pair"
  public_key = file("~/.ssh/marla_instance_1.pub")
}

resource "aws_eip" "eip" {
  instance = aws_instance.ec2_instance.id
  domain      = "vpc"
}


data "aws_route53_zone" "existing" {
  name = "harrysprojects.com"
}

resource "aws_route53_record" "my_a_record" {
  zone_id = data.aws_route53_zone.existing.zone_id
  name    = var.subdomain
  type    = "A"
  ttl     = "300"
  records = [aws_eip.eip.public_ip]
}
