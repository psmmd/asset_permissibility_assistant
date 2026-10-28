#!/usr/bin/env bash
# Copy the API keys from the local .env into Secrets Manager, without printing them.
# The value is passed on stdin, so it never appears in the process list or in shell history.
set -euo pipefail
cd "$(dirname "$0")"

get() { grep -E "^$1=" ../.env | cut -d= -f2-; }
anthropic=$(get ANTHROPIC_API_KEY)
openai=$(get OPENAI_API_KEY)
[[ -n "$anthropic" && -n "$openai" ]] || { echo "Both keys must be set in .env" >&2; exit 1; }

jq -n --arg a "$anthropic" --arg o "$openai" '{ANTHROPIC_API_KEY: $a, OPENAI_API_KEY: $o}' |
  aws secretsmanager put-secret-value \
    --region "$(terraform output -raw region)" \
    --secret-id "$(terraform output -raw api_keys_secret_name)" \
    --secret-string file:///dev/stdin >/dev/null
echo "API keys stored in Secrets Manager."
