output "url" {
  value = "http://${aws_instance.app.public_ip}"
}

output "region" {
  value = var.region
}

output "instance_id" {
  value = aws_instance.app.id
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "api_keys_secret_name" {
  value = aws_secretsmanager_secret.api_keys.name
}
