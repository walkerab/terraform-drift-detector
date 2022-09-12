terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "sg" {
  tags = {
    Name = "terraform-drift-test"
  }
}

output "sg_id" {
  value = aws_security_group.sg.id
}
