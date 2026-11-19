#!/usr/bin/env bash
# Instala Prometheus y Grafana en la Mac coordinadora con Homebrew.
# Uso:
#   cp .env.example .env   # nombres reales de las estaciones en Tailscale
#   ./instalar.sh
# Se puede repetir: respalda la configuración anterior antes de reemplazarla.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
[ -f "$DIR/.env" ] || { echo "Falta $DIR/.env. Copia .env.example y edítalo."; exit 1; }
# shellcheck disable=SC1091
source "$DIR/.env"
: "${OBS_TARGETS:?Define OBS_TARGETS en .env}"
OBS_RETENCION="${OBS_RETENCION:-90d}"
OBS_PUERTO_SENSORES="${OBS_PUERTO_SENSORES:-4445}"
OBS_VISTA_ANONIMA="${OBS_VISTA_ANONIMA:-no}"
OBS_DISCORD_WEBHOOK="${OBS_DISCORD_WEBHOOK:-}"
OBS_HORA_INICIO="${OBS_HORA_INICIO:-09:00}"
OBS_HORA_FIN="${OBS_HORA_FIN:-18:00}"
OBS_HORA_FIN_SABADO="${OBS_HORA_FIN_SABADO:-13:00}"
OBS_ZONA="${OBS_ZONA:-America/Merida}"

command -v brew >/dev/null || { echo "Se necesita Homebrew: https://brew.sh"; exit 1; }
PREFIX="$(brew --prefix)"
ETC="$PREFIX/etc"
VAR="$PREFIX/var"
SELLO="$(date +%Y%m%d-%H%M%S)"

echo "==> Instalando Prometheus y Grafana"
brew install prometheus grafana

respaldar() { [ -f "$1" ] && cp "$1" "$1.bak-$SELLO" && echo "    respaldo: $1.bak-$SELLO" || true; }

echo "==> Configurando Prometheus"
respaldar "$ETC/prometheus.yml"
respaldar "$ETC/prometheus.args"
{
  echo "# Generado por observabilidad/mac/instalar.sh"
  echo "global:"
  echo "  scrape_interval: 15s"
  echo "  evaluation_interval: 15s"
  echo ""
  echo "scrape_configs:"
  echo "  - job_name: prometheus"
  echo "    static_configs:"
  echo "      - targets: [\"127.0.0.1:9090\"]"
  echo ""
  echo "  - job_name: estaciones"
  echo "    scrape_timeout: 10s"
  echo "    static_configs:"
  IFS=',' read -ra ENTRADAS <<< "$OBS_TARGETS"
  for e in "${ENTRADAS[@]}"; do
    etiqueta="${e%%=*}"; destino="${e#*=}"
    echo "      - targets: [\"$destino\"]"
    echo "        labels:"
    echo "          estacion: \"$etiqueta\""
  done
  echo ""
  echo "  - job_name: sensores"
  echo "    scrape_timeout: 10s"
  echo "    metrics_path: /metrics/"
  echo "    static_configs:"
  for e in "${ENTRADAS[@]}"; do
    etiqueta="${e%%=*}"; destino="${e#*=}"
    echo "      - targets: [\"${destino%:*}:$OBS_PUERTO_SENSORES\"]"
    echo "        labels:"
    echo "          estacion: \"$etiqueta\""
  done
} > "$ETC/prometheus.yml"

cat > "$ETC/prometheus.args" <<EOF
--config.file $ETC/prometheus.yml
--web.listen-address=127.0.0.1:9090
--storage.tsdb.path $VAR/prometheus
--storage.tsdb.retention.time=$OBS_RETENCION
EOF
promtool check config "$ETC/prometheus.yml"

echo "==> Configurando Grafana"
INI="$ETC/grafana/grafana.ini"
PROV="$ETC/grafana/provisioning"
respaldar "$INI"
mkdir -p "$PROV/datasources" "$PROV/dashboards" "$PROV/alerting" "$PROV/plugins"
cp "$DIR/grafana/provisioning/datasources/prometheus.yml" "$PROV/datasources/prometheus.yml"
mkdir -p "$ETC/grafana/dashboards"
cp "$DIR"/grafana/dashboards/*.json "$ETC/grafana/dashboards/"
sed "s|__DASHBOARDS_DIR__|$ETC/grafana/dashboards|" "$DIR/grafana/provisioning/dashboards/uondr.yml" > "$PROV/dashboards/uondr.yml"
python3 -I - "$INI" "$PROV" "$OBS_VISTA_ANONIMA" <<'PY'
import re, sys
ini, prov = sys.argv[1], sys.argv[2]
s = open(ini, encoding="utf-8").read()
s, n = re.subn(r"(?m)^;?\s*provisioning\s*=.*$", f"provisioning = {prov}", s, count=1)
if n == 0:
    s = s.replace("[paths]", f"[paths]\nprovisioning = {prov}", 1)
# Vista anónima de solo lectura: Grafana escucha solo en 127.0.0.1, así que solo aplica dentro de la Mac
anon = "true" if sys.argv[3] == "si" else "false"
i = s.find("[auth.anonymous]")
if i >= 0:
    j = s.find("\n[", i + 1); j = len(s) if j < 0 else j
    sec = s[i:j]
    sec = re.sub(r"(?m)^;?\s*enabled\s*=.*$", f"enabled = {anon}", sec, count=1)
    sec = re.sub(r"(?m)^;?\s*org_role\s*=.*$", "org_role = Viewer", sec, count=1)
    s = s[:i] + sec + s[j:]
open(ini, "w", encoding="utf-8").write(s)
PY
grep -E "^(provisioning|http_addr) *=" "$INI" || true

echo "==> Alertas por Discord"
case "$OBS_DISCORD_WEBHOOK" in
  https://discord.com/api/webhooks/*|https://discordapp.com/api/webhooks/*)
  cp "$DIR/grafana/provisioning/alerting/reglas.yml" "$PROV/alerting/reglas.yml"
  rm -f "$PROV/alerting/correo.yml"
  # El webhook es un secreto: el archivo generado queda solo para el usuario.
  ( umask 077; cat > "$PROV/alerting/discord.yml" <<EOF2
# Generado por instalar.sh desde .env. No se publica.
apiVersion: 1
deleteContactPoints:
  - orgId: 1
    uid: correo-uondr
contactPoints:
  - orgId: 1
    name: discord-uondr
    receivers:
      - uid: discord-uondr
        type: discord
        settings:
          url: "$OBS_DISCORD_WEBHOOK"
          use_discord_username: false
muteTimes:
  - orgId: 1
    name: fuera-de-horario
    time_intervals:
      - weekdays: ["monday:friday"]
        times:
          - start_time: "00:00"
            end_time: "$OBS_HORA_INICIO"
          - start_time: "$OBS_HORA_FIN"
            end_time: "24:00"
        location: "$OBS_ZONA"
      - weekdays: ["saturday"]
        times:
          - start_time: "00:00"
            end_time: "$OBS_HORA_INICIO"
          - start_time: "$OBS_HORA_FIN_SABADO"
            end_time: "24:00"
        location: "$OBS_ZONA"
      - weekdays: ["sunday"]
        location: "$OBS_ZONA"
policies:
  - orgId: 1
    receiver: discord-uondr
    group_by: ["alertname", "estacion"]
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
    routes:
      - receiver: discord-uondr
        object_matchers: [["equipo", "=", "uondr"]]
        mute_time_intervals: ["fuera-de-horario"]
EOF2
  )
  echo "    alertas al canal de Discord, activas lun-vie $OBS_HORA_INICIO-$OBS_HORA_FIN y sáb $OBS_HORA_INICIO-$OBS_HORA_FIN_SABADO"
  ;;
  *)
  rm -f "$PROV/alerting/reglas.yml" "$PROV/alerting/correo.yml" "$PROV/alerting/discord.yml"
  echo "    sin OBS_DISCORD_WEBHOOK válido en .env: alertas desactivadas"
  ;;
esac

echo "==> Arrancando servicios"
brew services restart prometheus
brew services restart grafana
sleep 8

echo "==> Verificación"
curl -fsS http://127.0.0.1:9090/-/ready && echo
curl -fsS "http://127.0.0.1:9090/api/v1/targets?state=active" \
  | python3 -I -c 'import sys,json; [print("   ", t["labels"].get("estacion", t["labels"]["job"]), t["scrapeUrl"], t["health"], t.get("lastError","")) for t in json.load(sys.stdin)["data"]["activeTargets"]]'
curl -fsS http://127.0.0.1:3000/api/health && echo
echo "Grafana: http://127.0.0.1:3000 (el primer inicio pide cambiar la contraseña de admin)"
