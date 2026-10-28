#!/usr/bin/env bash
# Build the image for ARM64, push it to ECR and restart the app on the server.
set -euo pipefail
cd "$(dirname "$0")"

region=$(terraform output -raw region)
repo=$(terraform output -raw ecr_repository_url)
instance=$(terraform output -raw instance_id)
tag=$(git rev-parse --short HEAD)

aws ecr get-login-password --region "$region" | docker login --username AWS --password-stdin "${repo%%/*}"
docker build --platform linux/arm64 -t "$repo:$tag" -t "$repo:latest" ..
docker push "$repo:$tag"
docker push "$repo:latest"

# The service pulls :latest and re-ingests the rules on every restart.
aws ssm send-command --region "$region" --instance-ids "$instance" \
  --document-name AWS-RunShellScript --parameters 'commands=["systemctl restart app"]' \
  --query Command.CommandId --output text >/dev/null
echo "Deployed $tag. The app restarts in about a minute: $(terraform output -raw url)"
