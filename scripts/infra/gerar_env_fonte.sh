#!/usr/bin/env bash
# Gera o arquivo `.env` do checkout do i-Educar a partir do `.env.example` oficial e das
# variaveis da instancia (config/instancia-*.env). Necessario porque o php-fpm do i-Educar
# le a configuracao do `.env` do checkout (as variaveis do container nao chegam ao FPM).
# Somente valores de laboratorio; nenhum segredo real e utilizado.
#
# Uso: scripts/infra/gerar_env_fonte.sh config/instancia-a.env
set -euo pipefail

ENV_FILE="${1:?uso: $0 config/instancia-X.env}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

SRC="$(cd "$IEDUCAR_SRC" && pwd)"
APP_KEY_VALUE="base64:$(head -c 32 /dev/urandom | base64)"

sed \
  -e "s|^DB_HOST=.*|DB_HOST=postgres|" \
  -e "s|^REDIS_HOST=.*|REDIS_HOST=redis|" \
  -e "s|^DB_DATABASE=.*|DB_DATABASE=${DB_DATABASE}|" \
  -e "s|^DB_USERNAME=.*|DB_USERNAME=${DB_USERNAME}|" \
  -e "s|^DB_PASSWORD=.*|DB_PASSWORD=${DB_PASSWORD}|" \
  -e "s|^REDIS_PREFIX=.*|REDIS_PREFIX=${REDIS_PREFIX}|" \
  -e "s|^APP_URL=.*|APP_URL=${APP_URL}|" \
  -e "s|^APP_KEY=.*|APP_KEY=${APP_KEY_VALUE}|" \
  "$SRC/.env.example" > "$SRC/.env"

echo "Gerado ${SRC}/.env para a instancia ${INSTANCE_NAME}"
