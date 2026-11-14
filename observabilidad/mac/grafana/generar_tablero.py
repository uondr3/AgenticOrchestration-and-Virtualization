#!/usr/bin/env python3
"""Genera el tablero UONDR de Grafana (dashboards/uondr.json).

Uso:
    python3 generar_tablero.py            # escribe dashboards/uondr.json
    python3 generar_tablero.py --probar   # además ejecuta cada consulta en Prometheus local

El tablero se versiona en el repo y Grafana lo carga por provisioning.
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

DS = {"type": "prometheus", "uid": "prometheus-uondr"}

# Paleta validada (tema oscuro): el color sigue a la entidad, nunca al orden.
COLOR_ESTACION = {"Estación Revit": "#3987e5", "Estación 3ds Max": "#d95926"}
COLOR_PROGRAMA = {
    "Revit": "#3987e5",
    "3dsmax": "#d95926",
    "3dsmaxbatch": "#199e70",
    "claude": "#c98500",
    "rvt-mcp": "#d55181",
}
# Colores de estado: reservados para umbrales.
BUENO, AVISO, CRITICO = "#0ca30c", "#fab219", "#d03b3b"

NVIDIA = 'windows_gpu_info{name=~"NVIDIA.*"}'
EST = 'estacion=~"$estacion"'

Q = {
    "conexion": 'up{job="estaciones",%s}' % EST,
    "cpu": '1 - avg by (estacion) (rate(windows_cpu_time_seconds_total{mode="idle",%s}[$__rate_interval]))' % EST,
    "ram_pct": '1 - windows_memory_available_bytes{%s} / windows_memory_physical_total_bytes{%s}' % (EST, EST),
    "ram_usada": 'windows_memory_physical_total_bytes{%s} - windows_memory_available_bytes{%s}' % (EST, EST),
    "ram_total": 'windows_memory_physical_total_bytes{%s}' % EST,
    "revit_abiertos": 'count by (estacion) (windows_process_info{process="Revit",%s}) or (0 * group by (estacion) (up{job="estaciones",%s}))' % (EST, EST),
    "bakes": 'count by (estacion) (windows_process_info{process="3dsmaxbatch",%s}) or (0 * group by (estacion) (up{job="estaciones",%s}))' % (EST, EST),
    "cpu_temp": 'max by (estacion) (ohm_cpu_celsius{sensor="Core (Tctl/Tdie)",%s})' % EST,
    "gpu_temp": 'max by (estacion) (windows_gpu_temperature_celsius{%s} * on (instance, estacion, luid) group_left () %s)' % (EST, NVIDIA),
    "gpu_uso": 'max by (estacion) (sum by (estacion, instance, luid, engtype, eng) (rate(windows_gpu_engine_time_seconds_total{%s}[$__rate_interval])) * on (instance, estacion, luid) group_left () %s)' % (EST, NVIDIA),
    "gpu_vram": 'max by (estacion) (windows_gpu_adapter_memory_dedicated_bytes{%s} * on (instance, estacion, luid) group_left () %s)' % (EST, NVIDIA),
    "prog_ram": 'sum by (estacion, process) (windows_process_working_set_private_bytes{%s})' % EST,
    "prog_cpu": 'sum by (estacion, process) (rate(windows_process_cpu_time_seconds_total{%s}[$__rate_interval])) / on (estacion) group_left () count by (estacion) (windows_cpu_time_seconds_total{mode="idle",%s})' % (EST, EST),
    "prog_vram": 'sum by (estacion, process) ((windows_gpu_process_memory_dedicated_bytes{%s} * on (instance, estacion, luid) group_left () %s) * on (instance, estacion, process_id) group_left (process) windows_process_info{%s})' % (EST, NVIDIA, EST),
    "revit_ram": 'windows_process_working_set_private_bytes{process="Revit",estacion="Estación Revit"}',
    "revit_cpu": 'sum by (estacion, process_id) (rate(windows_process_cpu_time_seconds_total{process="Revit",estacion="Estación Revit"}[$__rate_interval])) / on (estacion) group_left () count by (estacion) (windows_cpu_time_seconds_total{mode="idle",estacion="Estación Revit"})',
    "disco": 'windows_logical_disk_free_bytes{volume=~"[A-Z]:",%s} / windows_logical_disk_size_bytes{volume=~"[A-Z]:",%s}' % (EST, EST),
    "red_rx": 'sum by (estacion) (rate(windows_net_bytes_received_total{%s}[$__rate_interval]))' % EST,
    "red_tx": 'sum by (estacion) (rate(windows_net_bytes_sent_total{%s}[$__rate_interval]))' % EST,
}

_id = 0


def nid():
    global _id
    _id += 1
    return _id


def target(expr, legend, ref="A", instant=False):
    t = {"datasource": DS, "expr": expr, "legendFormat": legend, "refId": ref, "range": not instant}
    if instant:
        t["instant"] = True
    return t


def colores(mapa):
    return [
        {"matcher": {"id": "byName", "options": k},
         "properties": [{"id": "color", "value": {"mode": "fixed", "fixedColor": v}}]}
        for k, v in mapa.items()
    ]


def umbrales(*pasos):
    s = [{"color": BUENO, "value": None}]
    for color, valor in pasos:
        s.append({"color": color, "value": valor})
    return {"mode": "absolute", "steps": s}


def fila(titulo, y, repetir=None):
    p = {"type": "row", "id": nid(), "title": titulo, "collapsed": False,
         "gridPos": {"h": 1, "w": 24, "x": 0, "y": y}, "panels": []}
    if repetir:
        p["repeat"] = repetir
    return p


def stat(titulo, expr, x, y, w, h=4, unidad="none", decimales=None, umbral=None,
         mapeos=None, descripcion=""):
    p = {
        "type": "stat", "id": nid(), "title": titulo, "description": descripcion, "datasource": DS,
        "gridPos": {"h": h, "w": w, "x": x, "y": y},
        "targets": [target(expr, "{{estacion}}", instant=True)],
        "options": {"reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
                    "colorMode": "background" if umbral or mapeos else "none",
                    "graphMode": "none", "justifyMode": "center", "textMode": "value_and_name",
                    "orientation": "vertical", "wideLayout": True},
        "fieldConfig": {"defaults": {"unit": unidad, "color": {"mode": "thresholds"},
                                     "thresholds": umbral or {"mode": "absolute", "steps": [{"color": "text", "value": None}]},
                                     "mappings": mapeos or []},
                        "overrides": []},
    }
    if decimales is not None:
        p["fieldConfig"]["defaults"]["decimals"] = decimales
    return p


def serie(titulo, objetivos, x, y, w, h=8, unidad="none", apilar=False, max_=None,
          sobreescribir=None, descripcion="", umbral=None, tope=None):
    d = {"unit": unidad, "color": {"mode": "palette-classic-by-name"},
         "custom": {"lineWidth": 0 if apilar else 2, "fillOpacity": 70 if apilar else 8, "showPoints": "never",
                    "stacking": {"mode": "normal" if apilar else "none", "group": "A"},
                    "spanNulls": 60000, "axisSoftMin": 0,
                    "thresholdsStyle": {"mode": "dashed" if umbral else "off"}}}
    if max_ is not None:
        d["max"] = max_
    if tope is not None:
        d["custom"]["axisSoftMax"] = tope
    if umbral:
        d["thresholds"] = umbral
    return {
        "type": "timeseries", "id": nid(), "title": titulo, "description": descripcion, "datasource": DS,
        "gridPos": {"h": h, "w": w, "x": x, "y": y},
        "targets": objetivos,
        "options": {"legend": {"displayMode": "table", "placement": "right", "calcs": ["lastNotNull", "max"]},
                    "tooltip": {"mode": "multi", "sort": "desc"}},
        "fieldConfig": {"defaults": d, "overrides": sobreescribir or []},
    }


def red_colores():
    o = []
    for est, color in COLOR_ESTACION.items():
        o.append({"matcher": {"id": "byName", "options": f"{est} · recibido"},
                  "properties": [{"id": "color", "value": {"mode": "fixed", "fixedColor": color}}]})
        o.append({"matcher": {"id": "byName", "options": f"{est} · enviado"},
                  "properties": [{"id": "color", "value": {"mode": "fixed", "fixedColor": color}},
                                 {"id": "custom.lineStyle", "value": {"fill": "dash", "dash": [6, 4]}}]})
    return o


# Ficha técnica de cada estación. Actualizar cuando cambie el hardware
# (se obtiene con observabilidad/windows/ficha-tecnica.ps1).
FICHA_FECHA = "2026-11-14"
FICHA = {
    "Estación Revit": [
        ("Procesador", "AMD Ryzen 9 9900X · 12 núcleos / 24 hilos"),
        ("Placa", "Gigabyte B850 AORUS ELITE WIFI7 ICE · BIOS F11"),
        ("RAM", "**64 GB** DDR5 · 4 × 16 GB · 4 de 4 ranuras · **3600 MT/s**"),
        ("Módulos", "2 × G.Skill F5-6000J3636F16G + 2 × ADATA AX5U5600C4616G"),
        ("Tarjeta de video", "NVIDIA GeForce RTX 5080 · AMD Radeon integrada"),
        ("Disco", "Kingston NV3 1 TB NVMe"),
        ("Sistema", "Windows 11 Pro · build 26200"),
        ("Nota", "Dos kits distintos: la RAM trabaja a 3600 MT/s, abajo de su nominal de 5600–6000"),
    ],
    "Estación 3ds Max": [
        ("Procesador", "AMD Ryzen 9 9950X · 16 núcleos / 32 hilos"),
        ("Placa", "ASUS ProArt B850-CREATOR WIFI NEO · BIOS 0239"),
        ("RAM", "**64 GB** DDR5 · 2 × 32 GB · 2 de 4 ranuras · **4800 MT/s**"),
        ("Módulos", "Corsair CMK64GX5M2D6000C40, kit de 2 × 32 GB"),
        ("Tarjeta de video", "NVIDIA GeForce RTX 5070 · AMD Radeon integrada"),
        ("Discos", "Kingston NV3 1 TB NVMe interno · ADATA HV620S 1 TB USB · Transcend StoreJet 1 TB USB"),
        ("Sistema", "Windows 11 Pro · build 26200"),
        ("Nota", "Kit de 6000 MT/s trabajando a 4800 MT/s: el perfil EXPO no está activo"),
    ],
}


def ficha(nombre, x, y):
    filas = "\n".join(f"| **{k}** | {v} |" for k, v in FICHA[nombre])
    contenido = f"| | |\n|---|---|\n{filas}\n\n<small>Actualizada el {FICHA_FECHA}</small>"
    return {"type": "text", "id": nid(), "title": nombre, "gridPos": {"h": 10, "w": 12, "x": x, "y": y},
            "options": {"mode": "markdown", "content": contenido}}


def construir():
    panels = []
    y = 0
    panels.append(fila("00 · FICHA TÉCNICA · Hardware de cada estación", y)); y += 1
    panels += [ficha("Estación Revit", 0, y), ficha("Estación 3ds Max", 12, y)]
    y += 10
    panels.append(fila("01 · EN VIVO · Estado actual de cada estación", y)); y += 1
    panels += [
        stat("Conexión", Q["conexion"], 0, y, 4,
             mapeos=[{"type": "value", "options": {"1": {"text": "En línea", "color": BUENO},
                                                   "0": {"text": "Sin datos", "color": CRITICO}}}],
             umbral=umbrales((BUENO, 1)), descripcion="Prometheus lee el medidor de la estación"),
        stat("Procesador", Q["cpu"], 4, y, 3, unidad="percentunit", decimales=0,
             umbral=umbrales((AVISO, 0.75), (CRITICO, 0.9))),
        stat("RAM usada", Q["ram_pct"], 7, y, 3, unidad="percentunit", decimales=0,
             umbral=umbrales((AVISO, 0.75), (CRITICO, 0.9))),
        stat("Revit abiertos", Q["revit_abiertos"], 10, y, 3, decimales=0,
             descripcion="Cada casa debe ir en su propio Revit"),
        stat("Bakes", Q["bakes"], 13, y, 3, decimales=0,
             descripcion="Procesos 3dsmaxbatch activos"),
        stat("Temp. procesador", Q["cpu_temp"], 16, y, 4, unidad="celsius", decimales=0,
             umbral=umbrales((AVISO, 80), (CRITICO, 90)),
             descripcion="Sensor Tctl/Tdie del Ryzen, leído por OhmGraphite"),
        stat("Temp. tarjeta NVIDIA", Q["gpu_temp"], 20, y, 4, unidad="celsius", decimales=0,
             umbral=umbrales((AVISO, 75), (CRITICO, 85))),
    ]
    y += 4

    panels.append(fila("02 · TENDENCIA · Procesador y memoria en el tiempo", y)); y += 1
    panels += [
        serie("Procesador", [target(Q["cpu"], "{{estacion}}")], 0, y, 12, unidad="percentunit", max_=1,
              sobreescribir=colores(COLOR_ESTACION)),
        serie("RAM usada", [target(Q["ram_usada"], "{{estacion}}")], 12, y, 12, unidad="bytes",
              sobreescribir=colores(COLOR_ESTACION),
              descripcion="Cada estación tiene 64 GB"),
    ]
    y += 8

    panels.append(fila("03 · POR PROGRAMA · $estacion", y, repetir="estacion")); y += 1
    panels += [
        serie("RAM por programa", [target(Q["prog_ram"], "{{process}}")], 0, y, 8, unidad="bytes",
              apilar=True, sobreescribir=colores(COLOR_PROGRAMA)),
        serie("Procesador por programa", [target(Q["prog_cpu"], "{{process}}")], 8, y, 8,
              unidad="percentunit", sobreescribir=colores(COLOR_PROGRAMA),
              descripcion="Porcentaje de toda la máquina"),
        serie("Memoria de video por programa", [target(Q["prog_vram"], "{{process}}")], 16, y, 8,
              unidad="bytes", apilar=True, sobreescribir=colores(COLOR_PROGRAMA),
              descripcion="Solo la tarjeta NVIDIA"),
    ]
    y += 8

    panels.append(fila("04 · REVIT POR INSTANCIA · Una línea por casa abierta", y)); y += 1
    panels += [
        serie("RAM de cada Revit", [target(Q["revit_ram"], "Revit pid {{process_id}}")], 0, y, 12,
              unidad="bytes", descripcion="Una línea por Revit abierto. Cada casa va en su propio Revit"),
        serie("Procesador de cada Revit", [target(Q["revit_cpu"], "Revit pid {{process_id}}")], 12, y, 12,
              unidad="percentunit", descripcion="Porcentaje de toda la máquina"),
    ]
    y += 8

    panels.append(fila("05 · TEMPERATURA · Procesador y tarjeta de video", y)); y += 1
    panels += [
        serie("Procesador", [target(Q["cpu_temp"], "{{estacion}}")], 0, y, 12, unidad="celsius",
              sobreescribir=colores(COLOR_ESTACION), umbral=umbrales((AVISO, 80), (CRITICO, 90)),
              descripcion="Sensor Tctl/Tdie del Ryzen. Aviso a 80 °C, crítico a 90 °C", tope=95),
        serie("Tarjeta NVIDIA", [target(Q["gpu_temp"], "{{estacion}}")], 12, y, 12, unidad="celsius",
              sobreescribir=colores(COLOR_ESTACION), umbral=umbrales((AVISO, 75), (CRITICO, 85)),
              descripcion="Aviso a 75 °C, crítico a 85 °C", tope=95),
    ]
    y += 8

    panels.append(fila("06 · TARJETA DE VIDEO · Uso y memoria de la NVIDIA", y)); y += 1
    panels += [
        serie("Uso", [target(Q["gpu_uso"], "{{estacion}}")], 0, y, 12, unidad="percentunit", max_=1,
              sobreescribir=colores(COLOR_ESTACION)),
        serie("Memoria de video usada", [target(Q["gpu_vram"], "{{estacion}}")], 12, y, 12, unidad="bytes",
              sobreescribir=colores(COLOR_ESTACION)),
    ]
    y += 8

    panels.append(fila("07 · DISCO Y RED · Espacio libre y tráfico", y)); y += 1
    disco = {
        "type": "bargauge", "id": nid(), "title": "Espacio libre por disco", "datasource": DS,
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": y},
        "targets": [target(Q["disco"], "{{estacion}} · {{volume}}", instant=True)],
        "options": {"orientation": "horizontal", "displayMode": "basic", "showUnfilled": True,
                    "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}},
        "fieldConfig": {"defaults": {"unit": "percentunit", "min": 0, "max": 1, "decimals": 0,
                                     "color": {"mode": "thresholds"},
                                     "thresholds": {"mode": "absolute", "steps": [
                                         {"color": CRITICO, "value": None}, {"color": AVISO, "value": 0.1},
                                         {"color": BUENO, "value": 0.2}]}},
                        "overrides": []},
    }
    panels += [
        disco,
        serie("Red", [target(Q["red_rx"], "{{estacion}} · recibido", "A"),
                      target(Q["red_tx"], "{{estacion}} · enviado", "B")], 12, y, 12, unidad="Bps",
              sobreescribir=red_colores()),
    ]

    return {
        "uid": "uondr-estaciones",
        "title": "UONDR · Estaciones",
        "description": "Recursos de las estaciones Revit y 3ds Max. Generado por generar_tablero.py",
        "tags": ["uondr", "estaciones"],
        "timezone": "browser",
        "refresh": "30s",
        "time": {"from": "now-6h", "to": "now"},
        "schemaVersion": 41,
        "version": 1,
        "editable": True,
        "graphTooltip": 1,
        "templating": {"list": [{
            "type": "query", "name": "estacion", "label": "Estación", "datasource": DS,
            "query": {"query": 'label_values(up{job="estaciones"}, estacion)', "refId": "estaciones"},
            "definition": 'label_values(up{job="estaciones"}, estacion)',
            "refresh": 1, "multi": True, "includeAll": True, "regex": "/^Estación .*/", "allValue": "Estación .*",
            "current": {"selected": True, "text": ["All"], "value": ["$__all"]},
            "sort": 1,
        }]},
        "panels": panels,
        "annotations": {"list": [{"builtIn": 1, "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                                  "enable": True, "hide": True, "iconColor": "rgba(0, 211, 255, 1)",
                                  "name": "Annotations & Alerts", "type": "dashboard"}]},
    }


def probar():
    errores = 0
    for nombre, expr in Q.items():
        e = (expr.replace('=~"$estacion"', '=~".*"').replace("$__rate_interval", "2m"))
        url = "http://127.0.0.1:9090/api/v1/query?" + urllib.parse.urlencode({"query": e})
        try:
            d = json.load(urllib.request.urlopen(url, timeout=10))
            res = d["data"]["result"]
            muestra = "; ".join(
                f'{r["metric"].get("estacion", r["metric"].get("process", r["metric"].get("process_id", "")))}'
                f'{" " + r["metric"].get("volume", "") if "volume" in r["metric"] else ""}'
                f'={float(r["value"][1]):.3g}' for r in res[:6])
            print(f"OK   {nombre:15} {len(res):3} series  {muestra}")
            if not res:
                errores += 1
        except Exception as ex:  # noqa: BLE001
            errores += 1
            print(f"FALLA {nombre:15} {ex}")
    return errores


if __name__ == "__main__":
    salida = Path(__file__).parent / "dashboards" / "uondr.json"
    salida.write_text(json.dumps(construir(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"escrito {salida}")
    if "--probar" in sys.argv:
        sys.exit(1 if probar() else 0)
