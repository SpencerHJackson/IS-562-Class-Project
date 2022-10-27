
/*
*
*      EC2 Web Server Configuration
*
*/

# EC2 Instance with code to install CodeDeploy agent and Apache and download webfiles from S3 bucket
resource "aws_instance" "project1_ec2_webserver" {
    ami                             = var.ami
    subnet_id                       = aws_subnet.public.id
    instance_type                   = var.instance_type
    vpc_security_group_ids          = [aws_security_group.ec2_sg.id]
    iam_instance_profile            = aws_iam_instance_profile.ec2_profile.name
    associate_public_ip_address     = true
    key_name                        = var.ec2_keypair
    user_data = <<-EOF
      #!/bin/bash
      echo "Update dependencies and install CodeDeploy Agent"
      yum -y update
      yum install -y ruby
      yum install -y aws-cli
      yum install -y httpd
      yum install -y mysql
      yum install -y python-mysqldb
      yum install -y python3-pip
      python3 -m pip install --upgrade pip
      pip install django==3.2
      service httpd start
      systemctl enable httpd
      cd /home/ec2-user
      wget https://aws-codedeploy-us-east-2.s3.us-east-2.amazonaws.com/latest/install
      chmod +x ./install
      ./install auto
      EOF

    tags = {
      Name                      = "Project1-web-server"
      Project1WebsiteServer     = "Project1WebsiteServer"
    }
}