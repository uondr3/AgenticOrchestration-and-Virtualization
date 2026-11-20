# Convenciones del proyecto

Orquestación de agentes de IA entre las estaciones de arquitectura de UONDR: una Mac coordinadora, una estación Revit y una estación 3ds Max, unidas por Tailscale y Orca, con observabilidad en Prometheus y Grafana.

## Cómo trabajamos

- Respuestas en español, fáciles de entender, con tablas y poco texto. Primero la respuesta, después el detalle.
- Lo que se decide, se ejecuta o se logra **siempre queda registrado** en el repo y en Notion. Ver "Al cerrar cada avance".
- Antes de afirmar que algo funciona, se verifica: comando, consulta, captura o huella SHA-256.
- Si algo falla dos veces seguidas, se detiene y se reporta. No se improvisa.

## Este repo es público

Todo lo que se sube lo puede leer cualquiera, y queda guardado aunque después se borre.

**Nunca se publica:** nombres de personas, usuarios de Windows, direcciones IP, nombres de máquina (`DESKTOP-*`, nombres reales en Tailscale), enlaces de emparejamiento de Orca, correos, contraseñas, nombres de proyectos o casas de clientes.

- En los documentos se usan roles: **estación Revit**, **estación 3ds Max**, **Mac coordinadora**.
- En lo privado (chat con el coordinador, Discord, Notion y el tablero instalado en la Mac) cada estación se nombra como su arquitecto, para reconocerla rápido. Los nombres están en `OBS_NOMBRE_REVIT` y `OBS_NOMBRE_MAX` de `observabilidad/mac/.env`.
- Los datos reales viven en archivos que git ignora: `.env`, `observabilidad/mac/.env` y `privado/`.
- Antes de cada push se revisa lo que va a subir:

  ```bash
  git diff --cached --name-only | xargs grep -n -i -E "100\.[0-9]+\.[0-9]+\.[0-9]+|192\.168\.|DESKTOP-|C:\\\\Users\\\\[A-Za-z]|@[a-z0-9-]+\.(com|mx)|orca://pair" | grep -v "100.64.0.0/10"
  ```

  Si aparece algo, se corrige antes de subir.

## Commits

- Autor: la dirección anónima de GitHub de `uondr3`, configurada solo en este repo. No cambiarla.
- Los commits terminan con la línea `Co-Authored-By` del agente que los hizo.
- El push usa la cuenta `uondr3` a través de `gh`, ya configurado en este repo.
- Mensajes cortos en español con prefijo: `docs:`, `obs:`, `fix:`.
- El repo anterior en la otra cuenta se deja como está. No se borra.

## Dónde va cada cosa

| Archivo | Qué guarda |
|---|---|
| `README.md` | Resumen, diagrama y tabla de estado de las pruebas |
| `docs/plan.md` | Decisiones con fecha, fases y medidas preventivas |
| `docs/pruebas.md` | Pruebas P1 a P7: criterio, cómo se hizo y resultado |
| `docs/observabilidad.md` | Componentes, instalación, operación diaria, tablero y alertas |
| `docs/agentes/` | Reglas y guías de los agentes: proyectos de cada estación y agente del recorrido 3D |
| `observabilidad/` | Scripts y configuración de Prometheus, Grafana y las estaciones |
| `tracking/ejecuciones.md` | Bitácora: todo lo que se ejecutó. Lo más reciente arriba |
| `tracking/hitos.md` | Hitos con fecha y estado |

Formato de la bitácora: `| Fecha | Dónde | Qué se hizo | Resultado |`, con resultado ✅, ⚠️, ⛔ o ⏸️.

## Al cerrar cada avance

1. Agregar una fila arriba en `tracking/ejecuciones.md`.
2. Si es un hito, marcarlo en `tracking/hitos.md`.
3. Actualizar el estado en `README.md` y el documento de `docs/` que corresponda.
4. Revisar datos sensibles, hacer commit y push.
5. Actualizar Notion, en **UONDR / 3D WALKTROUGHT**:
   - **Orquestación de agentes · Tablero**: fases, pruebas, máquinas, pendientes, decisiones.
   - **Observabilidad · Tablero**: avance, componentes, hitos, seguridad, accesos.
   - **Tablero del segundo recorrido 3D** (lleva el nombre del proyecto): orden de trabajo, estación Revit, agentes y repos, pendientes, decisiones.

   Notion lleva tablas y emojis, con poco texto. Se edita con cambios puntuales, sin reescribir la página.
6. Avisar por Discord con la herramienta `avisar` del MCP `uondr-discord`: avance cerrado, falla o decisión pendiente. Si la sesión no tiene el MCP, se usa `observabilidad/mac/discord/avisos-mcp.sh`.

## Trabajo en las estaciones

Los arquitectos aprobaron cambios en sus proyectos, **siempre con medidas preventivas**:

- Respaldo antes de cualquier cambio.
- Pruebas en copias o en áreas aparte, nunca sobre el trabajo abierto del arquitecto.
- Nunca se toca la instancia interactiva de 3ds Max. Los procesos pesados van en `3dsmaxbatch`, uno a la vez si guardan EXR.
- Una casa por Revit, un agente por Revit. Un arquitecto y un agente nunca editan la misma casa.
- Se avisa al arquitecto antes de algo pesado o de una ventana de permiso de Windows.
- Al terminar se borra lo que creó la prueba y se cierran las terminales abiertas.

Forma de operar desde la Mac:

- **Comandos:** terminal de PowerShell abierta con `orca terminal create --environment <estación>`. Se cierra al terminar con `orca terminal close`.
- **Scripts:** se publican primero en el repo, se descargan en la estación desde `raw.githubusercontent.com` y se verifica su SHA-256 antes de correrlos.
- **Permiso de administrador:** `Start-Process powershell -Verb RunAs`. El arquitecto acepta la ventana de Windows, y el resultado se escribe en `C:\ProgramData\UONDR-obs\*.log`.
- **Tareas para agentes:** `orca orchestration worker-start --on <estación> --worktree <identidad del proyecto existente>`. En áreas de trabajo nuevas la tarea no llega en Windows.
- **Agentes con `--keep-open`:** mantienen ocupado su Revit. Se liberan con `orca orchestration worker-release`.
- **Emparejamiento en un solo sentido:** la Mac entra al Orca de las estaciones. Las PCs de los arquitectos no se emparejan con el Orca de la Mac.
- **Correo a un agente de una estación:** `orca orchestration send --on <estación> --to <term_…>`. Después se lee su pantalla y se escribe una sola línea en su chat para que revise su bandeja. La respuesta no despierta a quien envió, así que se vigila su bandeja con `orca orchestration inbox`.
- **Archivos de texto con acentos:** los `.ps1` se guardan con BOM UTF-8 para PowerShell 5.1.

## Observabilidad

- El tablero **UONDR · Estaciones** es código: `observabilidad/mac/grafana/generar_tablero.py`. Se edita ahí, nunca a mano en Grafana.

  ```bash
  python3 observabilidad/mac/grafana/generar_tablero.py --probar --instalar   # prueba cada consulta e instala con los nombres del .env
  ```

- Tablero sin emojis. Las secciones van numeradas y en mayúsculas: `01 · EN VIVO · ...`.
- Colores fijos: azul para la estación Revit, naranja para la estación 3ds Max. Verde, amarillo y rojo solo para umbrales.
- Debe leerse en pantalla dividida. Para revisarlo se toman capturas con Chrome sin ventana a 900 y 1200 px de ancho, sobre la vista de solo lectura local:

  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --virtual-time-budget=20000 \
    --window-size=1600,1200 --screenshot=captura.png "http://127.0.0.1:3000/d/uondr-estaciones?orgId=1&kiosk"
  ```

- La ficha técnica del tablero se actualiza cuando cambia el hardware, con `observabilidad/windows/ficha-tecnica.ps1`.
- Configuración local en `observabilidad/mac/.env`. Después de cambiarla se vuelve a correr `observabilidad/mac/instalar.sh`.

## Secretos

- Nunca se muestran ni se copian al chat ni a los documentos: el `.env`, los enlaces de emparejamiento, la URL del webhook de Discord ni la contraseña de Grafana.
- Un secreto que el usuario tiene que dar se pide con una ventana de la Mac con texto oculto (`osascript ... with hidden answer`) y se escribe directo al archivo privado, sin pasar por el chat.
- Para leer un valor del `.env` se usa sin imprimirlo.
