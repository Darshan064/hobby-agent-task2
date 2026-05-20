resource "aws_security_group" "flask_sg" {
  name = "flask-security-group"

  ingress {
    from_port   = 5000
    to_port     = 5000
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

resource "aws_instance" "flask_server" {
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t3.micro"

  security_groups = [aws_security_group.flask_sg.name]

  key_name = "flask-key"

  tags = {
    Name = "FlaskServer"
  }
}
