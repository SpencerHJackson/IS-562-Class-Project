/*
*
*      IAM Configuration for EC2 Instance
*
*/

# IAM Assume Role for EC2
resource "aws_iam_role" "ec2_instance_role" {
  name                      = "EC2InstanceRole-${random_id.id.hex}"
  description               = "IAM Role for access EC2"
  assume_role_policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }
  EOF

  tags = {
    Name = "EC2AssumeRole"
  }
}

# EC2 Instance Profile to be referenced by aws_instance resource
resource "aws_iam_instance_profile" "ec2_profile" {
  name                      = "ec2_profile_${random_id.id.hex}"
  role                      = aws_iam_role.ec2_instance_role.name
}

# Attach role policies for SSMManagedInstanceCore and S3ReadOnlyAccess to EC2 Instance
resource "aws_iam_role_policy_attachment" "role_policy_attachment" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
  ])

  role = aws_iam_role.ec2_instance_role.name
  policy_arn = each.value
}
