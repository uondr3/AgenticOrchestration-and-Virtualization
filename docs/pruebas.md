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
| P7 📦 Entrega sin WhatsApp | ¿La entrega llega a la Mac y se valida sola? | Huella correcta y validador aceptado | ⬜ |

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
Se monta 3ds Max 2021, Corona 9 y Forest Pack con las mismas rutas en otra estación y se hornea la misma zona. Mientras corre se revisa qué licencia toma cada programa.

### P7 · Entrega sin WhatsApp
El agente deja el ZIP en la carpeta compartida; la Mac verifica la huella contra `entrega.json` y corre el validador.
