# 📒 Bitácora de ejecuciones

Qué se ejecutó, dónde y con qué resultado. Lo más reciente arriba.

| Fecha | Dónde | Qué se hizo | Resultado |
|---|---|---|---|
| 2026-11-20 | Notion | Tablero nuevo para el segundo recorrido 3D, con la misma estructura que los otros dos: orden aprobado, estado de la estación Revit, agentes y repos, pendientes y decisiones. Releído después de crearlo | ✅ |
| 2026-11-20 | Mac | Decisión del coordinador: orden de trabajo del segundo recorrido 3D aprobado (ver `docs/plan.md`) | ✅ Registrada |
| 2026-11-20 | Mac | Mapa de componentes en Excalidraw: estaciones, agentes, repositorio donde escribe cada uno, carpeta de entregas y pendientes. Privado, porque lleva nombres; revisado con un render | ✅ |
| 2026-11-20 | Estación Revit | Inventario de solo lectura por Orca, que ya responde: 3ds Max 2021.3.17, Corona 9 Hotfix 1 y Forest Pack Pro 6.3.1 instalados; RAM 2 × 16 GB a 4800 MT/s. Para hornear ahí falta el exportador glTF, `fopenexr`, Python, el MCP de 3ds Max y aclarar licencias. Ficha técnica actualizada. Terminal cerrada | ✅ |
| 2026-11-19 | Mac | Tablero visible desde otros equipos de Tailscale con `tailscale serve` por http, solo dentro de la red. Probado por la dirección de Tailscale: salud 200, tablero 200 y captura a ancho de celular. Falta la regla para que las PCs de las estaciones no lo vean | ✅ / ⚠️ regla pendiente |
| 2026-11-19 | Mac | Estaciones con el nombre de su arquitecto en el tablero instalado y en los avisos de Discord, a pedido del coordinador. Los nombres viven solo en `.env`; el repo sigue con roles y Prometheus no cambia, así que el historial sigue completo. Revisado con capturas: leyendas, colores, disco, red, tabla y fichas. 5 alertas sin error | ✅ |
| 2026-11-19 | Tablero | Sección 03 sin datos en la estación 3ds Max: no es falla. Desde el 18-nov a las 12:21 no tiene abierto ningún programa medido (3ds Max, bakes ni agente); su medidor funciona. Las secciones 03 y 04 ahora dicen qué falta abrir en vez de "No data". En la estación Revit hay un 3ds Max 2021 abierto: revisar para P6 | ✅ |
| 2026-11-19 | Mac | Horario de avisos a Discord igual al de la oficina: lunes a viernes de 9:00 a 18:00 y sábado de 9:00 a 13:00; domingo en silencio. La recolección de datos no se apaga. `instalar.sh` corrido otra vez: 5 medidores arriba y 5 alertas evaluando sin error | ✅ |
| 2026-11-19 | Tablero | Ficha técnica actualizada y dos paneles nuevos en vivo en 08: **RAM instalada** y **Módulos de RAM**, que se actualizan solos cuando se mueve la RAM. Revisado a 900 y 1200 px | ✅ |
| 2026-11-19 | Las dos estaciones | Después de mover la RAM, conexiones revisadas: 5 medidores arriba y datos al minuto. Estación Revit: **32 GB**, 2 × 16 GB G.Skill (salieron los ADATA). Estación 3ds Max: 64 GB, 2 × 32 GB Corsair, ahora a **3600 MT/s** (antes 4800) | ✅ |
| 2026-11-19 | Estación Revit | `ficha-tecnica.ps1` no se pudo correr: su Orca no respondió, aunque Tailscale y los medidores sí. Falta leer la velocidad de la RAM | ⚠️ Pendiente |
| 2026-11-17 | Estación 3ds Max | Reglas de orquestación instaladas por su agente con visto bueno de la arquitecta: respaldo del archivo de reglas, `ORQUESTACION.md` con huella verificada y cargado al inicio, una regla vieja anotada. Revisado desde la Mac: huella igual, respaldo presente, las dos líneas al inicio | ✅ |
| 2026-11-17 | Mac → estación 3ds Max | Pedido de instalar las reglas enviado por el canal y avisado con una línea en su chat. Su agente descargó el archivo, verificó la huella y espera el visto bueno de la arquitecta | ⏸️ Esperando visto bueno |
| 2026-11-17 | Repo | Reglas de orquestación para la estación 3ds Max (`docs/agentes/max/ORQUESTACION.md`): canal de Orca, carpeta compartida con huella, bakes uno a la vez y registro de horarios para medir | ✅ Publicadas; falta instalarlas |
| 2026-11-17 | Estación Revit | Licencias para P6: la estación Revit no tiene 3ds Max ni Corona; se pueden comprar. Antes de comprar hay que confirmar que se puede activar la versión 2021 que usa la cadena | ✅ Aclarado |
| 2026-11-17 | Mac | Decisión: las estaciones no se emparejan con el Orca de la Mac. Se sigue avisando con una línea en el chat de la estación | ✅ Registrada |
| 2026-11-17 | Mac → estación 3ds Max | Conexión revisada otra vez: Orca responde, sesión del agente conectada y libre, carpeta compartida y medidores en línea | ✅ |
| 2026-11-17 | Mac → estación 3ds Max | El Orca de la estación no responde (puerto 6768 sin respuesta), aunque la estación sigue en línea en Prometheus. El canal queda en pausa hasta abrir Orca | ⚠️ |
| 2026-11-14 | Mac | **P7**: el agente del recorrido 3D validó la v12 con el validador 0.4.0: aceptada, 0 errores | ✅ |
| 2026-11-14 | Mac ↔ estación 3ds Max | **P7**: la v12 llegó por el canal, sin WhatsApp: ZIP de 1.38 GB y su `.md`, copiados en 55 s, huellas iguales | ✅ |
| 2026-11-14 | Mac ↔ estación 3ds Max | Prueba del canal: pregunta con contexto respondida y archivos de prueba en las dos direcciones con huellas iguales; los archivos se borraron. El correo de Orca no se entregó solo: hizo falta avisar en el chat de la estación | ✅ Con aviso manual |
| 2026-11-14 | Mac | MCP propio `uondr-discord` (`observabilidad/mac/discord/`): herramienta `avisar` por webhook, registrado en Claude Code. Aviso de prueba recibido por Discord | ✅ Conectado |
| 2026-11-14 | Mac | Alertas de Grafana pasan de Gmail a Discord: punto de contacto `discord-uondr`, el de correo se borró. 5 reglas sanas | ✅ |
| 2026-11-14 | Repo | Guía de canales para el agente del recorrido 3D (`docs/agentes/recorrido-3d/CANALES.md`): correo de Orca al chat de la estación 3ds Max, carpeta compartida con huella SHA-256 y prueba del canal. Valores reales en `privado/` | ✅ Lista; prueba pendiente |
| 2026-11-14 | Mac | Revisado el canal sin tocar la estación 3ds Max: Orca de la estación acepta comandos de orquestación, credencial de la carpeta compartida en el llavero, agente del recorrido 3D corriendo dentro de Orca | ✅ |
| 2026-11-14 | Mac | Tablero legible en pantalla dividida: EN VIVO en dos filas con textos de tamaño fijo, estaciones siempre en el mismo orden, leyendas abajo, ficha técnica al final como **08**. Revisado con capturas a 900 y 1200 px | ✅ |
| 2026-11-14 | Estación Revit | RAM verificada de nuevo con `ficha-tecnica.ps1` y consulta directa: 4 × 16 GB (2 G.Skill + 2 ADATA) a 3600 MT/s, 61.6 GB visibles. Sin cambios desde el arranque del 2026-11-13 | ✅ Verificado |
| 2026-11-14 | Repo | `CLAUDE.md` con las convenciones y el método de trabajo del proyecto | ✅ |
| 2026-11-14 | Mac | Alertas de Grafana por Gmail: 5 reglas, silencio fuera de horario. Reglas validadas en Grafana; falta la contraseña de aplicación para enviar | 🟡 |
| 2026-11-14 | Mac | Sección **00 · FICHA TÉCNICA** en el tablero con el hardware de cada estación | ✅ |
| 2026-11-14 | Las dos estaciones | Inventario de hardware con `ficha-tecnica.ps1`, solo lectura. Estación Revit: 4 × 16 GB de dos kits distintos a 3600 MT/s. Estación 3ds Max: 2 × 32 GB a 4800 MT/s y dos discos externos USB | ✅ |
| 2026-11-14 | Estación Revit | PawnIO + OhmGraphite instalados con `instalar-temperatura.ps1`. El primer intento de permiso no se aceptó; el segundo sí. Procesador a 49.5 °C | ✅ |
| 2026-11-13 | Mac | Tablero v2: secciones numeradas sin emojis, temperatura del procesador, áreas apiladas sin línea, umbrales punteados, red con color por estación. Revisado con capturas | ✅ |
| 2026-11-13 | Mac | Vista de solo lectura sin contraseña en Grafana, limitada a la Mac | ✅ |
| 2026-11-13 | Estación 3ds Max | PawnIO 2.2.0 + OhmGraphite 0.38.0 con `instalar-temperatura.ps1`, verificados por SHA-256. Procesador a 51 °C en reposo | ✅ |
| 2026-11-13 | Estación Revit | Instalación de temperatura pendiente: la estación no respondía, apagada o suspendida | ⏸️ |
| 2026-11-13 | Estación 3ds Max | El disco E: con poco espacio no afecta los bakes: la arquitecta hornea en el disco con más espacio libre | ✅ Aclarado |
| 2026-11-13 | Mac | Tablero **UONDR · Estaciones** en Grafana: 24 paneles en 6 secciones, generado por código y cargado por provisioning. Las 18 consultas probadas contra datos reales | ✅ |
| 2026-11-13 | Mac | Estaciones renombradas en Prometheus a `Estación Revit` y `Estación 3ds Max` | ✅ |
| 2026-11-13 | Estación 3ds Max | Hallazgo del tablero: el disco E: de 1 TB tiene 9.4 GB libres | ⚠️ Por revisar |
| 2026-11-13 | Estación 3ds Max | windows_exporter 0.32.1 instalado con `instalar-exporter.ps1` descargado del repo y verificado por SHA-256, ejecutado con permiso de administrador | ✅ 1,824 métricas, puerto solo para Tailscale |
| 2026-11-13 | Estación Revit | windows_exporter 0.32.1 instalado de la misma forma | ✅ 2,021 métricas, puerto solo para Tailscale |
| 2026-11-13 | Mac | Prometheus 3.16.0 y Grafana 13.3.1 instalados con `observabilidad/mac/instalar.sh` | ✅ Las dos estaciones en estado `up` |
| 2026-11-13 | Mac | Repo trasladado a `uondr3` y publicado. Autoría de commits con la dirección anónima de GitHub | ✅ |
| 2026-11-13 | Mac | Scripts de observabilidad: `observabilidad/mac/instalar.sh` y `observabilidad/windows/instalar-exporter.ps1` | ✅ Listos, sin instalar |
| 2026-11-12 | Estación Revit | Agente nuevo de verificación: respondió de memoria las 4 reglas de `ORQUESTACION.md` | ✅ Las reglas cargan solas |
| 2026-11-12 | Estación Revit | `ORQUESTACION.md` instalado, cargado desde `CLAUDE.md`; 2 reglas viejas corregidas en el documento de traspaso. Respaldo previo | ✅ Sin commit, a criterio del arquitecto |
| 2026-11-12 | Estación Revit | **P4**: 2 agentes lanzados desde la Mac, cada uno fijado por `pid` a su Revit. 20 notas creadas y borradas por agente, sin guardar | ✅ 13:02–13:05 simultáneos, 0 errores |
| 2026-11-12 | Estación Revit | Revisión previa: 3 Revit separados, cada uno registrado en rvt-mcp, 39.5 GB de RAM libres | ✅ |
| 2026-11-12 | Estación Revit | Actualización de rvt-mcp 0.8.1 → 1.2.2: respaldo de 822 MB, huella SHA-256 verificada, instalación de prueba, instalación real, `.mcp.json` actualizado | ✅ |
| 2026-11-12 | Estación Revit | Antes de instalar: 5 copias viejas de rvt-mcp seguían vivas por sesiones de Orca en segundo plano. Se detuvieron; los chats no se tocaron | ⚠️ Resuelto |
| 2026-11-12 | Estación Revit | **P4**, primer intento: los agentes se detuvieron solos. Solo había un Revit abierto y rvt-mcp 0.8.1 no distingue dos Revit del mismo año | ⛔ Detenido a salvo |
| 2026-11-12 | Estación Revit | **P3** entre máquinas, repetido con la misma versión de Orca | ✅ Funciona lanzando en el proyecto existente |
| 2026-11-12 | Estación Revit | **P3** en un área de trabajo nueva: el agente arranca pero la tarea no llega | ⚠️ Fallo de Orca en Windows |
| 2026-11-12 | Estación 3ds Max | Proyecto principal agregado a su Orca como carpeta | ✅ |
| 2026-11-12 | Mac | **P2**: emparejamiento con las dos estaciones | ✅ |
| 2026-11-12 | Mac ↔ Estación 3ds Max | **P1**: copia del ZIP de la v11 por carpeta compartida sobre Tailscale | ✅ 1.3 GB en 39 s, huella idéntica |
| 2026-11-12 | Las tres | **P1**: Tailscale instalado, nombres fijos, caducidad de llave desactivada en las estaciones | ✅ Conexión directa 5–14 ms |
| 2026-11-11 | Mac | **P3** ensayado en local: el agente preguntó, recibió la respuesta y reportó | ✅ |
