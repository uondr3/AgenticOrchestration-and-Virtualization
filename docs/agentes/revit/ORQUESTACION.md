# Trabajo en paralelo: varias casas, varios Revit

> Plantilla pública. La copia instalada en la estación Revit se carga desde su `CLAUDE.md` con la línea `@ORQUESTACION.md`.

Vigente desde el 12 de noviembre de 2026. Estas reglas tienen prioridad sobre cualquier instrucción anterior que diga elegir Revit por año o abrir otra casa dentro del Revit actual.

## La regla base

- **Una casa = un Revit abierto.** Cada casa vive en su propio proceso de Revit, no como pestaña dentro de otro Revit.
- **Un chat = una casa = un Revit.** Cada Revit acepta un solo agente conectado a la vez.
- **El arquitecto nunca edita una casa mientras su agente trabaja en ella**, y un agente nunca toca la casa de otro chat.
- Dentro de un mismo Revit las órdenes siguen siendo una tras otra, nunca en paralelo.

## Antes de la primera orden a Revit en cada tarea

1. Ejecuta `revit_list_available_targets`. Cada Revit aparece con su `pid` y el título de su ventana.
2. Elige el Revit cuya ventana tiene **tu** casa. Si no sabes cuál es tu casa, pregúntale al arquitecto antes de seguir.
3. Fíjate a él con `revit_switch_target` usando `pid:<n>` y haz la confirmación que pida la herramienta. **Nunca uses el año (2027) ni `auto`** cuando haya más de un Revit abierto.
4. Confirma con una consulta de solo lectura que el documento activo es tu casa.

Antes de cada bloque grande de cambios vuelve a confirmar el título del documento.

## Si algo no cuadra, detente y avisa al arquitecto

| Señal | Qué significa | Qué hacer |
|---|---|---|
| `AMBIGUOUS_TARGET` | Hay varios Revit y no elegiste uno | Elige por `pid` según el paso 3 |
| `TARGET_BUSY` | Otro chat ya está conectado a ese Revit | No insistas. Avisa al arquitecto: quizá te equivocaste de Revit o dos chats tienen la misma casa |
| `TARGET_CHANGED` | Ese Revit se cerró o se reinició y cambió de pid | Vuelve a los pasos 1 a 4 |
| Tu casa no aparece en ninguna ventana | No está abierta en su propio Revit | Pide al arquitecto que la abra en un Revit nuevo. Nunca la abras dentro de un Revit que ya tiene otra casa |
| Diálogo modal en Revit | Revit espera una respuesta humana | Detente y avisa. No sigas mandando órdenes |

## Git con varios chats en la misma carpeta

- Confirma solo tus propios archivos, nombrándolos uno por uno: `git add <rutas>`. Nunca uses `git add -A`, `git add .` ni `git commit -a`.
- Antes de confirmar, revisa `git status` y que solo vayan tus archivos.
- Si aparece `index.lock`, espera unos segundos y reintenta. No lo borres.
- Guarda los scripts de cada casa en su propia carpeta, `scripts/<casa>`.
- Para añadir algo a `lessons.md`, vuelve a leerlo justo antes de editar y cambia solo tu línea. Otro chat pudo haberlo modificado.

## rvt-mcp 1.2.2

- Desde el 12 de noviembre de 2026 la estación usa rvt-mcp 1.2.2. Antes usaba la 0.8.1, que no distinguía dos Revit del mismo año.
- Sus datos están en `%LOCALAPPDATA%\Bimwright\rvt-mcp\`. La carpeta `%LOCALAPPDATA%\RvtMcp\` ya no existe.
- Los scripts de `send_code` siguen funcionando igual.
- El historial de cambios por modelo viene encendido. Si una respuesta trae `_changes`, es normal.
- Existe `revit_report_task_result` para dejar en Revit un reporte de la tarea sin modificar el modelo.

## Tareas que llegan desde la Mac coordinadora

El coordinador puede mandar tareas a esta PC con Orca. Un agente que recibe una tarea así:

- sigue estas mismas reglas y las de `CLAUDE.md`;
- pregunta con `orca orchestration ask` cuando necesita una decisión, y termina su turno hasta recibir la respuesta;
- al terminar reporta con el comando que indique su tarea.

## Medidas preventivas que no cambian

- Antes de una modificación grande, respalda el archivo de la casa.
- No guardes, cierres ni sincronices una casa que no es la tuya.
- Si algo falla dos veces seguidas, detente y reporta. No improvises.
