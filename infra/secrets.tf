# Created empty: the value is set with infra/set-api-keys.sh, so the keys never enter Terraform state.
resource "aws_secretsmanager_secret" "api_keys" {
  name                    = "${var.project}/api-keys"
  recovery_window_in_days = 0 # delete immediately on destroy, so the name can be reused
}
