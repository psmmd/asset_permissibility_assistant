data "aws_ami" "al2023_arm" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-kernel-*-arm64"]
  }
}

resource "aws_instance" "app" {
  ami                         = data.aws_ami.al2023_arm.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.app.id]
  iam_instance_profile        = aws_iam_instance_profile.app.name
  associate_public_ip_address = true

  # IMDSv2 only, with a hop limit of 1: the host can read the role's credentials, but containers cannot.
  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  root_block_device {
    volume_size = 16
    volume_type = "gp3"
    encrypted   = true
  }

  user_data = templatefile("${path.module}/user_data.sh.tftpl", {
    region              = var.region
    image               = "${aws_ecr_repository.app.repository_url}:latest"
    registry            = split("/", aws_ecr_repository.app.repository_url)[0]
    api_keys_secret_arn = aws_secretsmanager_secret.api_keys.arn
    db_secret_arn       = aws_db_instance.db.master_user_secret[0].secret_arn
    db_host             = aws_db_instance.db.address
    db_name             = aws_db_instance.db.db_name
  })
  user_data_replace_on_change = true

  tags = {
    Name = var.project
  }

  lifecycle {
    ignore_changes = [ami] # a newer AMI should not replace a running server
  }
}
