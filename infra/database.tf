resource "aws_db_subnet_group" "db" {
  name       = var.project
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "db" {
  identifier     = var.project
  engine         = "postgres"
  engine_version = "17" # pgvector is available as an extension on RDS Postgres
  instance_class = var.db_instance_class

  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = "permissibility"
  username = "app"
  # RDS generates the password and keeps it in Secrets Manager: it never passes through Terraform or its state.
  manage_master_user_password = true

  db_subnet_group_name   = aws_db_subnet_group.db.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false

  # Demo settings: the data is rebuilt from the rules documents, so destroy must be quick and clean.
  backup_retention_period = 1
  skip_final_snapshot     = true
  deletion_protection     = false
  apply_immediately       = true
}
