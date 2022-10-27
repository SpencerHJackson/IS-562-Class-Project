/*
*
*      VPC, Subnet, Route Table, IGW, NAT, and Security Group creation
*
*/

# VPC Resource
resource "aws_vpc" "project1_vpc" {
  cidr_block                = "10.0.0.0/18"
  enable_dns_hostnames      = true

  tags = {
      Name = "Project 1 VPC"
  }
}
# Public Subnet Resource
resource "aws_subnet" "public" {
  vpc_id                    = aws_vpc.project1_vpc.id
  cidr_block                = "10.0.0.0/24"
  map_public_ip_on_launch   = true
  availability_zone         = data.aws_availability_zones.available.names[1]


  tags = {
      Name = "Public Subnet"
  }
}

data "aws_availability_zones" "available" {
  state                     = "available"
}

# Public Subnet Resource
resource "aws_subnet" "public2" {
  vpc_id                    = aws_vpc.project1_vpc.id
  cidr_block                = "10.0.1.0/24"
  availability_zone         = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch   = true

  tags = {
      Name = "Public2 Subnet"
  }
}

# 2nd Private Subnet Resource for DB instance (Aurora requires subnets in 2 AZs)
resource "aws_subnet" "private" {
  vpc_id                    = aws_vpc.project1_vpc.id
  cidr_block                = "10.0.2.0/24"
  availability_zone         = data.aws_availability_zones.available.names[1]

  tags = {
      Name = "Private Subnet 2"
  }
}

# Resource for Internet Gateway for Public Subnet
resource "aws_internet_gateway" "project1_igw" {
  vpc_id                    = aws_vpc.project1_vpc.id

  tags = {
      Name = "Main IGW"
  }
}
# Elastic IP for NAT Gateway for Private Subnet
resource "aws_eip" "project1_nat_eip" {
  vpc                       = true
  depends_on                = [aws_internet_gateway.project1_igw]

  tags = {
      Name = "NAT Gateway EIP"
  }
}

# NAT Gateway for VPC
resource "aws_nat_gateway" "project1_nat" {
  allocation_id             = aws_eip.project1_nat_eip.id
  subnet_id                 = aws_subnet.public.id

  tags = {
      Name = "Main NAT Gateway"
  }
}

# Route Table for Public Subnet
resource "aws_route_table" "public" {
  vpc_id                    = aws_vpc.project1_vpc.id

  route {
    cidr_block              = "0.0.0.0/0"
    gateway_id              = aws_internet_gateway.project1_igw.id
  }

  tags = {
      Name = "Public Route Table"
  }    
}

# Route Table for Private Subnet
resource "aws_route_table" "private" {
  vpc_id                    = aws_vpc.project1_vpc.id

  route {
    cidr_block              = "0.0.0.0/0"
    gateway_id              = aws_nat_gateway.project1_nat.id
  }

  tags = {
    Name = "Private Route Table"
  }
}

# Association between Public Subnet and Public Route Table
resource "aws_route_table_association" "public" {
  subnet_id                 = aws_subnet.public.id
  route_table_id            = aws_route_table.public.id
}

# Association between Public Subnet and Public Route Table
resource "aws_route_table_association" "public" {
  subnet_id                 = aws_subnet.public2.id
  route_table_id            = aws_route_table.public.id
}

# Association between Private Subnet and Private Route Table
resource "aws_route_table_association" "private" {
  subnet_id                 = aws_subnet.private.id
  route_table_id            = aws_route_table.private.id
}

# Compute Security Group
resource "aws_security_group" "ec2_sg" {
  name                      = "ec2_security_group"
  description               = "Security Group for EC2 webserver instance for SSH and HTTP/HTTPS traffic"
  vpc_id                    = aws_vpc.project1_vpc.id

  ingress {
    from_port               = 22
    to_port                 = 22
    protocol                = "tcp"
    cidr_blocks             = ["10.0.0.0/18", "0.0.0.0/0"]
  }
  
  ingress {
    from_port               = 8000
    to_port                 = 8000
    protocol                = "tcp"
    cidr_blocks             = ["0.0.0.0/0"]
  }

  ingress {
    from_port               = 443
    to_port                 = 443
    protocol                = "tcp"
    cidr_blocks             = ["0.0.0.0/0"]
  }

  egress {
    from_port               = 0
    to_port                 = 0
    protocol                = "-1"
    cidr_blocks             = ["0.0.0.0/0"]
  }

  tags = {
    Name = "EC2 Security Group"
    security_group = "ec2_sg"
  }
}

# RDS Security Group
resource "aws_security_group" "db_sg" {
  name                      = "db_security_group"
  description               = "DB security group for RDS and SSH traffic over ports 3306 and 22"
  vpc_id                    = aws_vpc.project1_vpc.id
  
  ingress {
    from_port               = 3306
    to_port                 = 3306
    protocol                = "tcp"
    cidr_blocks             = ["0.0.0.0/0"]
  }

  egress {
    from_port               = 0
    to_port                 = 0
    protocol                = "-1"
    cidr_blocks             = ["0.0.0.0/0"]
  }

  tags = {
    Name = "DB Security Group"
    security_group = "rds_sg"
  }
}
