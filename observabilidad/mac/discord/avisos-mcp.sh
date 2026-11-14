#!/bin/sh
# Arranca el servidor MCP de avisos de UONDR en Discord.
# Toma solo OBS_DISCORD_WEBHOOK de observabilidad/mac/.env, sin imprimirlo.
DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$DIR/../.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "avisos-mcp: falta $ENV_FILE" >&2
  exit 1
fi
OBS_DISCORD_WEBHOOK="$(. "$ENV_FILE" >/dev/null 2>&1; printf '%s' "${OBS_DISCORD_WEBHOOK:-}")"
export OBS_DISCORD_WEBHOOK
exec /usr/bin/python3 -I "$DIR/avisos_mcp.py"
