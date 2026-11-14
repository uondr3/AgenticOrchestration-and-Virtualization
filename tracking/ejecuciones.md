# 📒 Bitácora de ejecuciones

Qué se ejecutó, dónde y con qué resultado. Lo más reciente arriba.

| Fecha | Dónde | Qué se hizo | Resultado |
|---|---|---|---|
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
