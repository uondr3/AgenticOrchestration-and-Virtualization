# 🧭 Plan general

## Problema de partida

- Los agentes de cada estación trabajan en Revit y 3ds Max, pero **la aplicación atiende una orden a la vez** y el arquitecto se queda esperando.
- Prompts, respuestas y entregas viajan **por WhatsApp**, con ZIP de hasta 1.3 GB.
- Un ciclo de bakes del recorrido 3D tarda **de 1 a 3 horas** y crecerá con casas más grandes.

## Decisiones tomadas

| Fecha | Decisión | Por qué |
|---|---|---|
| 2026-11-09 | No virtualizar las estaciones | GPU-P y passthrough no son viables en Windows 11 Pro con GeForce, y la licencia de Autodesk es por usuario |
| 2026-11-11 | Ambos agentes usan Claude Code | Confirmado por el equipo |
| 2026-11-11 | Un arquitecto y un agente nunca editan la misma casa a la vez | Autodesk desaconseja el mismo usuario en dos sesiones del mismo proyecto |
| 2026-11-11 | La tarjeta de video no acelera los bakes | Corona 9 renderiza solo con CPU |
| 2026-11-12 | Red: Tailscale | Direcciones fijas, cifrado y acceso desde fuera de la oficina |
| 2026-11-12 | Orquestación: Orca con servidores remotos | La Mac lanza agentes en las estaciones y recibe sus reportes |
| 2026-11-12 | Entregas por carpeta compartida de Windows sobre Tailscale | 1.3 GB en 39 s, con reanudación |
| 2026-11-12 | **Un agente por Revit, una casa por Revit** | Cada Revit acepta una sola conexión de agente |
| 2026-11-12 | rvt-mcp 1.2.2 en la estación Revit | Desde la 1.1.0 distingue varios Revit del mismo año |
| 2026-11-13 | Observabilidad: Prometheus + Grafana en la Mac coordinadora | El equipo trabaja en el mismo horario; historial central y tableros propios |
| 2026-11-13 | Repo público en `uondr3` | Documentación compartida y trazabilidad |
| 2026-11-14 | Notificaciones por Discord en lugar de Gmail: webhook a un canal, para Grafana y para el agente coordinador | Decisión del coordinador. El webhook solo puede publicar en su canal |
| 2026-11-17 | Cada entrega espera el visto bueno de la arquitecta antes de ir a `para-mac\`, aunque la Mac la pida | Decisión de la arquitecta, anotada en sus reglas |
| 2026-11-17 | Las estaciones no se emparejan con el Orca de la Mac. El agente de la Mac avisa con una línea en el chat de la estación y vigila su propia bandeja | Las PCs de los arquitectos no deben tener acceso al Orca de la Mac |
| 2026-11-20 | Segundo recorrido 3D, producido en la estación Revit con un agente nuevo de 3ds Max. Orden: termina la ronda en curso → el agente de la estación 3ds Max escribe sus lecciones → limpieza y una carpeta por proyecto en el repo de la cadena → se instala lo que falta en la estación Revit → nace el agente nuevo y lee las lecciones | Reorganizar a media ronda rompería la cadena, y el agente nuevo debe partir de lo ya aprendido |
| 2026-11-20 | Las dos estaciones serán máquinas de horneado. El repo de la cadena llevará tareas y lecciones por proyecto | Hornear zonas a la vez solo se gana en PCs distintas; dos proyectos no deben pisarse |
| 2026-11-14 | El recorrido 3D deja WhatsApp: correo de Orca al chat del agente de la estación 3ds Max y archivos por la carpeta compartida | Habla con el agente que ya tiene el contexto, la arquitecta lo ve en su chat y cada archivo se verifica por huella |

## Fases

| Fase | Contenido | Estado |
|---|---|---|
| 1. Diagnóstico | Flujo actual, MCPs, licencias, virtualización | ✅ |
| 2. Validación | Pruebas P1 a P7 ([pruebas.md](pruebas.md)) | 🟡 5 de 7: P5 a medias, falta P6 |
| 3. Documentación para agentes | Reglas en los proyectos de cada estación ([agentes/](agentes)) | ✅ Reglas en las dos estaciones · guía de canales del recorrido 3D |
| 4. Coordinación y piloto | Trabajo real con varias casas y entregas automáticas | 🟡 Estación Revit en uso |
| 5. Observabilidad | Prometheus + Grafana ([observabilidad.md](observabilidad.md)) | 🟡 Tablero y alertas por Discord listos, faltan los eventos de agentes |

## Medidas preventivas que siempre se mantienen

- Respaldo antes de cualquier cambio en una estación.
- Pruebas en copias o en áreas aparte, nunca sobre el trabajo abierto del arquitecto.
- Nunca se toca la instancia interactiva de 3ds Max; los procesos pesados van en `3dsmaxbatch`.
- Se avisa al arquitecto antes de arrancar algo pesado.
- Si algo falla dos veces seguidas, el agente se detiene y reporta.
- Al terminar una prueba se borra lo que creó.
