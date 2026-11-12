resource "aws_key_pair" "my_key" {
  key_name   = "monitor_key"
  public_key = file("${path.module}/monitor_key.pub")

}
resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}
resource "aws_security_group" "my_security_group" {
  name        = "monitor_sg"
  description = "This will add a TF generated security group"
  vpc_id      = aws_default_vpc.default.id



  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
    description = "SSH from my IP"
  }
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
    description = "API from my IP"
  }
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
    description = "Grafana from my IP"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All access open outbound"
  }
  tags = {
    Name = "monitor_sg"
  }
}

resource "aws_instance" "my_instance" {
  instance_type   = var.instance_type
  ami             = var.ami_id
  key_name        = aws_key_pair.my_key.key_name
  security_groups = [aws_security_group.my_security_group.name]
  root_block_device {
    volume_size = var.storage_size
    volume_type = "gp3"
    encrypted   = true
  }
  tags = {
    Name        = var.project_name
    Environment = var.env
  }
}
