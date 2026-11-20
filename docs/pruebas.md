# 🧪 Pruebas de validación

Cada prueba responde una pregunta de sí o no. Los resultados se registran en [../tracking/ejecuciones.md](../tracking/ejecuciones.md).

| Prueba | Pregunta | Criterio para pasar | Estado |
|---|---|---|---|
| P1 🌐 Red | ¿Las tres máquinas se ven y llega un ZIP de 1.3 GB? | Conexión directa y misma huella SHA-256 | ✅ 2026-11-12 |
| P2 🔗 Orca entre máquinas | ¿La Mac entra al Orca de cada estación? | `orca host name` y `orca repo list` responden para cada estación | ✅ 2026-11-12 |
| P3 💬 Ida y vuelta | ¿Un agente en la Mac y otro en una estación se preguntan y responden solos? | La tarea llega, la pregunta llega, el reporte final se acepta | ✅ 2026-11-12 |
| P4 🏠 Dos Revit | ¿Dos agentes editan dos casas a la vez sin estorbarse ni estorbar al arquitecto? | 0 órdenes en la casa equivocada, 0 errores | ✅ 2026-11-12 |
| P5 🔥 Bake trabajando | ¿La arquitecta sigue en 3ds Max mientras corre un bake? | Max fluido y el bake se alarga poco | ⬜ |
| P6 🖥️ Bake en otra PC | ¿La cadena de bakes corre en otra estación y qué licencias pide? | Lightmap equivalente y sin bloqueo de licencia | ⬜ |
| P7 📦 Entrega sin WhatsApp | ¿La entrega llega a la Mac y se valida sola? | Huella correcta y validador aceptado | ✅ 2026-11-14 |

## Cómo se hizo cada una

### P1 · Red
Tailscale en las tres máquinas, una sola cuenta, nombres de máquina fijos y caducidad de llave desactivada en las estaciones. Una carpeta compartida de Windows en la estación 3ds Max, montada en la Mac con `smb://<estación>`.

### P2 · Orca entre máquinas
En cada estación: Settings → Remote Orca Servers → *Compartir este equipo*, con la dirección de Tailscale. En la Mac: `orca environment add --name <estación> --pairing-code "<enlace>"`. El enlace funciona como contraseña y no se publica.

### P3 · Ida y vuelta
```bash
orca orchestration worker-start --spec-file tarea.txt --on <estación> \
  --worktree <identidad del proyecto existente> --agent claude --keep-open
```
- Lanzado dentro del **proyecto existente**, la tarea llega sola. En un área de trabajo nueva no llega: es un fallo de Orca en Windows.
- El agente pregunta con `orca orchestration ask`, el coordinador contesta con `orca orchestration reply`.
- Un agente lanzado con `--keep-open` mantiene ocupada la conexión a su Revit hasta `orca orchestration worker-release`.

### P4 · Dos Revit
- Requisito: rvt-mcp 1.1.0 o más nuevo. Con la 0.8.1 dos Revit 2027 se pisaban el registro.
- Tres Revit separados: uno para el arquitecto y uno por cada agente.
- Cada agente se fija a su Revit por `pid`, confirma el nombre de la casa antes de cada bloque, crea una vista con 20 notas y la borra sin guardar.
- Resultado: los dos agentes trabajaron a la vez, de 13:02 a 13:05, con 0 errores. Cada nota tardó unos 20 ms dentro de Revit, y los tres Revit juntos usaron unos 5.5 GB de RAM.

### P5 · Bake trabajando
El agente hornea la zona más corta tres veces: normal, con prioridad baja, y con prioridad baja dejando núcleos libres en Corona. Se mide la duración, la RAM máxima y la fluidez de Max.

### P6 · Bake en otra PC
Inventario del 2026-11-20, solo lectura: la estación Revit **ya tiene** 3ds Max 2021.3.17 (la misma versión de la cadena), Corona 9 Hotfix 1 y Forest Pack Pro 6.3.1. Falta el resto de la cadena: exportador glTF de Khronos, `fopenexr`, Python con su entorno, el MCP de 3ds Max y una carpeta de entregas. Falta también saber qué licencia toma cada programa al hornear en las dos estaciones a la vez. Antes de comprar: confirmar que la licencia permite activar 3ds Max 2021, la versión de la cadena, y qué licencia de Corona usa `3dsmaxbatch`.
Se monta 3ds Max 2021, Corona 9 y Forest Pack con las mismas rutas en otra estación y se hornea la misma zona. Mientras corre se revisa qué licencia toma cada programa.

### P7 · Entrega sin WhatsApp
El agente de la Mac le escribe al chat del agente de la estación 3ds Max con `orca orchestration send --on <estación> --to <term_…>`, y la respuesta vuelve con `orca orchestration reply`. Los archivos viajan por la carpeta compartida, en `para-estacion/` y `para-mac/`, con su huella SHA-256 en el mensaje.

Primero se prueba el canal con archivos pequeños y una pregunta que solo contesta el agente con contexto. Después va la primera entrega real. Guía y pasos: [agentes/recorrido-3d/CANALES.md](agentes/recorrido-3d/CANALES.md).

**Resultado, 2026-11-14:** la v12, un ZIP de 1.38 GB con su `.md`, llegó por la carpeta compartida en 55 s con la huella correcta, y el validador 0.4.0 la aceptó con 0 errores. Falta un detalle: el correo de Orca no despierta solo a ninguno de los dos agentes. Hoy se avisa con una línea en el chat de la estación y el agente de la Mac vigila su bandeja.
