variable "region" {
  type    = string
  default = "eu-west-1"
}

variable "project" {
  description = "Name prefix for all resources."
  type        = string
  default     = "asset-permissibility"
}

variable "alert_email" {
  description = "Receives AWS Budgets alerts."
  type        = string
}

variable "monthly_budget_usd" {
  description = "Budget alert threshold for the whole account."
  type        = number
  default     = 20
}

variable "instance_type" {
  description = "ARM (Graviton) instance; the image is built for linux/arm64."
  type        = string
  default     = "t4g.small"
}

variable "db_instance_class" {
  type    = string
  default = "db.t4g.micro"
}
