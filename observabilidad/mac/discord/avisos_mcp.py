#!/usr/bin/env python3
"""Servidor MCP mínimo para los avisos de UONDR en Discord.

Publica en un solo canal de Discord por medio de un webhook: no lee mensajes ni
tiene permisos sobre el servidor. La URL del webhook llega en la variable de
entorno OBS_DISCORD_WEBHOOK, que carga avisos-mcp.sh desde observabilidad/mac/.env.
La URL es un secreto: nunca se imprime ni se devuelve.

Habla MCP por stdio (JSON-RPC 2.0, un mensaje por línea). Solo usa la biblioteca
estándar de Python 3.9.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.request

VERSIONES = ["2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25"]
COLORES = {"info": 0x3987E5, "ok": 0x0CA30C, "aviso": 0xFAB219, "critico": 0xD03B3B}
PREFIJOS = ("https://discord.com/api/webhooks/", "https://discordapp.com/api/webhooks/")

HERRAMIENTA = {
    "name": "avisar",
    "description": (
        "Envía un aviso al canal de Discord de UONDR, donde lo lee el coordinador. "
        "Úsalo cuando algo termina, falla o necesita su decisión. Texto corto en español. "
        "Nunca incluyas contraseñas, enlaces de emparejamiento ni valores de un .env."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "texto": {"type": "string", "maxLength": 3500,
                      "description": "Cuerpo del aviso. Admite el Markdown de Discord."},
            "titulo": {"type": "string", "maxLength": 200, "description": "Título corto."},
            "nivel": {"type": "string", "enum": list(COLORES), "default": "info",
                      "description": "info, ok, aviso o critico. Define el color."},
        },
        "required": ["texto"],
    },
}


def enviar(texto, titulo=None, nivel="info"):
    url = os.environ.get("OBS_DISCORD_WEBHOOK", "")
    if not url.startswith(PREFIJOS):
        raise RuntimeError("Falta OBS_DISCORD_WEBHOOK en observabilidad/mac/.env")
    tarjeta = {
        "description": texto[:3500],
        "color": COLORES.get(nivel, COLORES["info"]),
        "footer": {"text": "Mac coordinadora"},
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    if titulo:
        tarjeta["title"] = titulo[:200]
    cuerpo = json.dumps({
        "username": "Agente UONDR",
        "allowed_mentions": {"parse": []},
        "embeds": [tarjeta],
    }).encode("utf-8")
    pedido = urllib.request.Request(
        url + "?wait=true", data=cuerpo, method="POST",
        headers={"Content-Type": "application/json",
                 "User-Agent": "DiscordBot (https://github.com/uondr3/AgenticOrchestration-and-Virtualization, 1.0)"})
    try:
        with urllib.request.urlopen(pedido, timeout=15) as r:
            return json.load(r).get("id", "?")
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"Discord respondió {e.code}: {detalle}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Sin conexión con Discord: {e.reason}") from None


def llamar(params):
    if params.get("name") != "avisar":
        return {"content": [{"type": "text", "text": "Herramienta desconocida"}], "isError": True}
    a = params.get("arguments") or {}
    texto = str(a.get("texto", "")).strip()
    if not texto:
        return {"content": [{"type": "text", "text": "El texto está vacío"}], "isError": True}
    try:
        mensaje = enviar(texto, a.get("titulo"), a.get("nivel", "info"))
    except Exception as e:  # el error vuelve al agente, sin la URL
        return {"content": [{"type": "text", "text": f"No se envió: {e}"}], "isError": True}
    return {"content": [{"type": "text", "text": f"Aviso enviado a Discord (mensaje {mensaje})."}]}


def responder(id_, resultado=None, error=None):
    m = {"jsonrpc": "2.0", "id": id_}
    if error is not None:
        m["error"] = error
    else:
        m["result"] = resultado
    sys.stdout.write(json.dumps(m, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main():
    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue
        try:
            msg = json.loads(linea)
        except json.JSONDecodeError:
            responder(None, error={"code": -32700, "message": "JSON inválido"})
            continue
        if "id" not in msg:  # notificaciones: no llevan respuesta
            continue
        metodo, id_ = msg.get("method"), msg["id"]
        params = msg.get("params") or {}
        if metodo == "initialize":
            pedida = params.get("protocolVersion")
            responder(id_, {
                "protocolVersion": pedida if pedida in VERSIONES else "2025-06-18",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "uondr-discord", "version": "1.0.0"},
            })
        elif metodo == "ping":
            responder(id_, {})
        elif metodo == "tools/list":
            responder(id_, {"tools": [HERRAMIENTA]})
        elif metodo == "tools/call":
            responder(id_, llamar(params))
        else:
            responder(id_, error={"code": -32601, "message": f"Método no soportado: {metodo}"})


if __name__ == "__main__":
    main()
