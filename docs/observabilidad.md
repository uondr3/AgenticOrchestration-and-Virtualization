# 📈 Observabilidad

Historial de procesador, RAM, disco, red, tarjeta de video y consumo **por programa** de cada estación, para medir pruebas, decidir compras y entender qué pasó cuando algo falla.

## Componentes

```mermaid
flowchart LR
    subgraph REVIT["🏗️ Estación Revit"]
        WE1["windows_exporter :9182<br/>CPU · RAM · disco · red · GPU<br/>Revit · claude · rvt-mcp"]
    end
    subgraph MAX["🎨 Estación 3ds Max"]
        WE2["windows_exporter :9182<br/>CPU · RAM · disco · red · GPU<br/>3dsmax · 3dsmaxbatch · claude"]
    end
    subgraph MAC["💻 Mac coordinadora"]
        PROM["📊 Prometheus :9090<br/>recoge cada 15 s<br/>guarda 90 días"]
        GRAF["📈 Grafana :3000<br/>tableros y alertas"]
    end
    PROM -- "Tailscale" --> WE1
    PROM -- "Tailscale" --> WE2
    GRAF --> PROM
```

| Pieza | Dónde | Qué hace | Puerto |
|---|---|---|---|
| windows_exporter 0.32.1 | Cada estación, como servicio | Publica las métricas del sistema, de la tarjeta de video y de los programas elegidos | 9182 |
| Prometheus | Mac coordinadora | Pasa cada 15 s a recoger las métricas y guarda 90 días | 9090, solo local |
| Grafana | Mac coordinadora | Tableros, alertas y marcas de eventos | 3000, solo local |

La Mac se duerme fuera del horario de trabajo. Como el equipo trabaja en el mismo horario, los huecos de noche no importan.

## Qué se mide por programa

Solo los procesos que importan, para no llenar el historial de datos inútiles:

`Revit`, `3dsmax`, `3dsmaxbatch`, `claude`, `rvt-mcp`

Para cada uno: uso de procesador, memoria, lectura y escritura de disco, y memoria de video.

## Instalación

### 1. Estaciones Windows

En PowerShell **como administrador**:

```powershell
.\observabilidad\windows\instalar-exporter.ps1
```

- Descarga el MSI oficial y verifica su SHA-256.
- Lo instala como servicio con los colectores necesarios y el filtro de procesos.
- Abre el puerto 9182 **solo para direcciones de Tailscale** (`100.64.0.0/10`).
- No requiere cerrar Revit ni 3ds Max.

### 2. Mac coordinadora

```bash
cd observabilidad/mac
cp .env.example .env      # escribir los nombres reales de las estaciones en Tailscale
./instalar.sh
```

- Instala Prometheus y Grafana con Homebrew como servicios.
- Genera la configuración de Prometheus a partir de `.env`, con 90 días de historial.
- Conecta Grafana con Prometheus.
- Prometheus y Grafana escuchan solo en la Mac (`127.0.0.1`).

Grafana queda en <http://127.0.0.1:3000>. El primer inicio pide cambiar la contraseña `admin`.

## Seguridad

- Nada se expone a internet. Las métricas viajan solo por Tailscale.
- El puerto 9182 de cada estación acepta solo direcciones de Tailscale.
- Los nombres reales de las máquinas viven en `observabilidad/mac/.env`, que no se publica.

## Estado

| Pieza | Versión | Estado |
|---|---|---|
| Prometheus | 3.16.0 | ✅ En la Mac desde 2026-11-13 |
| Grafana | 13.3.1 | ✅ En la Mac desde 2026-11-13 |
| windows_exporter, estación Revit | 0.32.1 | ✅ |
| windows_exporter, estación 3ds Max | 0.32.1 | ✅ |
| OhmGraphite + PawnIO, estación 3ds Max | 0.38.0 + 2.2.0 | ✅ Temperatura del procesador |
| OhmGraphite + PawnIO, estación Revit | 0.38.0 + 2.2.0 | ✅ Temperatura del procesador |

### Temperatura del procesador

Windows no expone la temperatura de los Ryzen. La lee **OhmGraphite**, un servicio basado en LibreHardwareMonitor que publica los sensores en el puerto 4445, con ayuda de **PawnIO**, un controlador firmado que reemplaza al antiguo WinRing0. Se instala con:

```powershell
.\observabilidad\windows\instalar-temperatura.ps1    # como administrador
```

El sensor del tablero es `Core (Tctl/Tdie)`. Prometheus lo recoge en el trabajo `sensores`.

### Vista sin contraseña, solo en la Mac

Con `OBS_VISTA_ANONIMA="si"` en `observabilidad/mac/.env`, Grafana permite ver los tableros en modo lectura sin iniciar sesión. Como Grafana escucha solo en `127.0.0.1`, esto aplica únicamente dentro de la Mac. Sirve para que el agente coordinador tome capturas del tablero. Para quitarlo: `OBS_VISTA_ANONIMA="no"` y volver a correr `instalar.sh`.

Cada estación reporta dos tarjetas de video: la integrada del procesador y la NVIDIA. Para el tablero se filtra la NVIDIA.

## Operación diaria en la Mac

| Qué | Comando |
|---|---|
| Ver si los servicios corren | `brew services list` |
| Reiniciar | `brew services restart prometheus` · `brew services restart grafana` |
| Estado de las estaciones | <http://127.0.0.1:9090/targets> |
| Tableros | <http://127.0.0.1:3000> |
| Configuración | `/opt/homebrew/etc/prometheus.yml` · `/opt/homebrew/etc/grafana/grafana.ini` |
| Historial | `/opt/homebrew/var/prometheus` |

## Operación en las estaciones

| Qué | Comando en PowerShell |
|---|---|
| Ver si el medidor corre | `Get-Service windows_exporter` |
| Reiniciarlo | `Restart-Service windows_exporter`, como administrador |
| Ver sus datos | <http://127.0.0.1:9182/metrics> |
| Desinstalar | Panel de control → Programas → windows_exporter |

## Tablero UONDR · Estaciones

En Grafana: carpeta **UONDR** → **UONDR · Estaciones**, o directo en <http://127.0.0.1:3000/d/uondr-estaciones>.

| Sección | Qué muestra |
|---|---|
| 01 · EN VIVO | Conexión, procesador, RAM, Revit abiertos, bakes, temperatura del procesador y de la NVIDIA, por estación |
| 02 · TENDENCIA | Procesador y RAM de las dos estaciones en el tiempo |
| 03 · POR PROGRAMA | RAM, procesador y memoria de video de Revit, 3dsmax, 3dsmaxbatch, claude y rvt-mcp. Una fila por estación |
| 04 · REVIT POR INSTANCIA | RAM y procesador de cada Revit abierto, identificado por su `pid` |
| 05 · TEMPERATURA | Procesador y tarjeta NVIDIA, con líneas punteadas de aviso y crítico |
| 06 · TARJETA DE VIDEO | Uso y memoria de la NVIDIA |
| 07 · DISCO Y RED | Espacio libre por disco y tráfico de red |

Los títulos de sección van numerados y en mayúsculas, sin emojis. Las áreas apiladas se dibujan sin línea para que cada color corresponda a su programa.

Colores: azul para la estación Revit y para Revit, naranja para la estación 3ds Max y para 3dsmax. Verde, amarillo y rojo solo marcan umbrales: procesador y RAM al 75 % y 90 %, temperatura de la tarjeta a 75 °C y 85 °C, temperatura del procesador a 80 °C y 90 °C, disco con menos de 20 % y 10 % libre.

El tablero es código: se genera con `observabilidad/mac/grafana/generar_tablero.py`. Para cambiarlo se edita ese archivo y se corre:

```bash
python3 observabilidad/mac/grafana/generar_tablero.py --probar   # genera y prueba cada consulta
cp observabilidad/mac/grafana/dashboards/uondr.json /opt/homebrew/etc/grafana/dashboards/
```

Grafana lo recarga solo en 30 segundos. Los cambios hechos a mano en Grafana se pierden al regenerarlo.

## Alertas por correo

Grafana envía las alertas por **Gmail**, con SMTP de `smtp.gmail.com:587` y una **contraseña de aplicación** de Google.

| Alerta | Condición | Severidad |
|---|---|---|
| Estación desconectada | Prometheus no lee la estación durante 5 min | crítico |
| RAM arriba de 90 % | Durante 10 min | aviso |
| Procesador arriba de 90 °C | Durante 2 min | crítico |
| Tarjeta NVIDIA arriba de 85 °C | Durante 2 min | crítico |
| Disco del sistema con menos de 10 % libre | Disco C:, durante 15 min | aviso |

- Fuera del horario de trabajo y en fin de semana las alertas se silencian.
- Se agrupan por alerta y estación, y una alerta activa se repite cada 4 horas.
- Las alertas salen de la Mac: si está dormida, no se evalúan.

Para activarlas, en `observabilidad/mac/.env`:

```bash
OBS_SMTP_USUARIO="cuenta que envía"
OBS_SMTP_CLAVE="contraseña de aplicación"   # https://myaccount.google.com/apppasswords
OBS_ALERTA_CORREO="quién recibe"            # vacío = la misma cuenta
OBS_HORA_INICIO="09:00"
OBS_HORA_FIN="19:00"
```

y volver a correr `observabilidad/mac/instalar.sh`. Las reglas están en `observabilidad/mac/grafana/provisioning/alerting/reglas.yml`. El destinatario y el horario se generan desde `.env` y no se publican. Para probar el envío: Grafana → Alerting → Contact points → `correo-uondr` → Test.

## Ficha técnica

La sección **00 · FICHA TÉCNICA** del tablero muestra el hardware de cada estación. Se obtiene con `observabilidad/windows/ficha-tecnica.ps1`, que solo lee, y se escribe en `FICHA` dentro de `generar_tablero.py`. Hay que actualizarla cuando cambie el hardware.

## Siguientes pasos

| Paso | Qué |
|---|---|
| Eventos de agentes | Los agentes marcan en Grafana el inicio y fin de cada bake o entrega |
