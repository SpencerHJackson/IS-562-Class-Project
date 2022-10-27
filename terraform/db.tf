/*
*
*      DB Server Configuration
*
*/

# AWS DB Instance for MySQL DB
resource "aws_db_instance" "rds_instance" {
    allocated_storage       = 20
    instance_class          = var.db_instance_class
    engine                  = "mysql"
    engine_version          = "5.7"
    identifier              = "rds-terraform"
    db_name                 = var.db_name
    username                = var.db_username
    password                = var.db_password
    skip_final_snapshot     = true
    db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
    publicly_accessible     = true
    vpc_security_group_ids  = [aws_security_group.db_sg.id]
    multi_az                = false
    

    tags = {
        Name = "rds-db-server"
    }
}

# AWS DB Subnet Resource
resource "aws_db_subnet_group" "rds_subnet_group" {
    name                    = "main"
    description             = "Subnet for the DB Instance"
    subnet_ids              = [aws_subnet.public.id, aws_subnet.public2.id]

    tags = {
        Name = "db-subnets"
    }
}