# 📡 Canales del agente del recorrido 3D

Guía para el agente de la **Mac coordinadora** que trabaja el recorrido 3D web. El **coordinador** es la persona que dirige el proyecto desde la Mac. Reemplaza a WhatsApp para hablar con el agente de la **estación 3ds Max** y para mover archivos entre las dos máquinas.

> Los valores reales (nombre de la estación en Orca, sesión del agente, rutas) no se publican. Están en la Mac, en `privado/canales-recorrido-3d.md` de este repo.

## Qué cambia

| Antes | Ahora |
|---|---|
| El prompt viajaba por WhatsApp y la arquitecta lo pegaba en su chat | Mensaje de Orca directo al chat de su agente |
| Respuesta y ZIP por WhatsApp | Respuesta por Orca; archivos en la carpeta compartida |
| No había forma de comprobar el archivo | Huella SHA-256 en el mensaje, comparada al recibir |
| No se sabía si la estación estaba ocupada | Tablero de Grafana: bakes, procesador, RAM y temperatura |

## Piezas

| Pieza | Para qué |
|---|---|
| Tailscale | Red privada entre la Mac y las estaciones. Ya funciona; no se toca |
| Orca · correo entre agentes | Pedidos, preguntas y respuestas con el agente que ya tiene el contexto de la estación |
| Carpeta compartida `UONDR-entregas` | Archivos en las dos direcciones, por SMB sobre Tailscale. 1.3 GB en 39 s |
| Grafana · tablero UONDR · Estaciones | Ver si la estación está libre antes de pedir algo pesado |
| Orca · trabajadores | Solo con permiso del coordinador: agentes nuevos que trabajan solos en la estación |

## 1. Mandar un mensaje

1. **Encontrar la sesión del agente de la estación.** Su identificador cambia cuando la arquitecta reinicia su chat, así que se busca cada vez:

   ```bash
   orca terminal list --environment <estación 3ds Max> --json
   ```

   Es la fila con `"agentIdentity": "claude"`. Su `handle` empieza con `term_`. Si hay más de una, se pregunta al coordinador cuál usar.

2. **Enviar:**

   ```bash
   orca orchestration send --on <estación 3ds Max> --to <term_…> \
     --subject "Recorrido 3D · <tema corto>" \
     --body "<pedido completo>"
   ```

3. **Avisar que revise su bandeja.** Si el agente de la estación está ocupado o esperando, Orca retiene el correo y no se lo entrega. Primero se lee su pantalla, solo lectura, y luego se escribe una sola línea en su chat:

   ```bash
   orca terminal read --environment <estación 3ds Max> --terminal <term_…> --screen
   orca terminal send --environment <estación 3ds Max> --terminal <term_…> \
     --text "Revisa tus mensajes de Orca: <msg_id>" --enter
   ```

   Esa línea solo avisa; el pedido completo siempre va por correo.

4. **Esperar la respuesta.** Hoy la respuesta no despierta al agente de la Mac. Se vigila la bandeja propia sin consumirla, con `orca orchestration inbox`, y luego se lee con `orca orchestration check`.

5. **Contestar preguntas** del otro agente:

   ```bash
   orca orchestration reply --id <msg_id> --body "<respuesta>"
   ```

> [!IMPORTANT]
> Para mensajes siempre se usa `--on`. Con `--environment` el comando corre en la estación, pero no entrega correo.

### Lo aprendido en la primera prueba (2026-11-14)

| Detalle | Qué pasa |
|---|---|
| Entrega automática del correo | No funcionó en ninguna dirección: Orca lo retiene mientras el agente está ocupado o esperando |
| Aviso en el chat | Una línea con `orca terminal send` hace que el agente de la estación lea su bandeja |
| `--type` con `--on` | Solo se aceptan `status` y `handoff`. Con `question` se rechaza y no se envía nada; lo normal es omitir `--type` |
| Sentido contrario | La estación no está emparejada con la Mac, así que su agente no puede escribirle al de la Mac. Responde con `reply` y el de la Mac vigila su bandeja |
| Archivos | Prueba en las dos direcciones con huellas iguales. La v12, de 1.38 GB, llegó en 55 s con la huella correcta |

### Cómo escribir el mensaje

- Un pedido por mensaje, completo por sí mismo: qué se pide, para qué, con qué archivos, qué se entrega y dónde.
- El mensaje aparece en el chat de la arquitecta y ella lo lee. Se escribe como antes por WhatsApp, sin secretos.
- Se pide la respuesta con `orca orchestration reply` y la huella SHA-256 de cada archivo.
- Para instrucciones largas: un `.md` en la carpeta compartida, mencionado en el mensaje.

## 2. Mover archivos

Desde la Mac:

```bash
open "smb://<estación 3ds Max>/UONDR-entregas"   # usa la contraseña guardada en el llavero
ls /Volumes/UONDR-entregas
```

| Subcarpeta | Dirección | Ejemplo |
|---|---|---|
| `para-estacion/` | Mac → estación 3ds Max | Paquetes e instrucciones para la arquitecta |
| `para-mac/` | Estación 3ds Max → Mac | Entregas `<casa>-vNN.zip` con su `.md` |

Si las subcarpetas no existen, el agente de la Mac las crea.

### Protocolo

| Paso | Quién | Qué |
|---|---|---|
| 1 | Quien envía | Copia el archivo y calcula su huella: `shasum -a 256` en la Mac, `Get-FileHash -Algorithm SHA256` en Windows |
| 2 | Quien envía | Pone nombre, tamaño y huella en el mensaje de Orca |
| 3 | Quien recibe | Copia a su disco (`rsync --partial --progress` en la Mac), recalcula la huella y compara |
| 4 | Quien recibe | Responde con el resultado. Si no coincide, se copia otra vez |

Si algo falla dos veces seguidas, se detiene y se avisa al coordinador.

Los archivos de prueba se borran al terminar. Las entregas reales se quedan en la carpeta hasta que el coordinador diga otra cosa.

## 3. Reglas de la estación 3ds Max

| Regla | Por qué |
|---|---|
| Nunca pedir que se toque el 3ds Max que la arquitecta tiene abierto | Es su trabajo en curso |
| Procesos pesados en `3dsmaxbatch`, uno a la vez si guardan EXR | Evita choques de archivos y de RAM |
| Antes de pedir un bake o algo pesado, revisar el tablero y avisar en el mensaje | La arquitecta sigue trabajando en la misma máquina |
| La arquitecta tiene la última palabra en su chat | El canal no reemplaza su criterio |
| Nunca mandar contraseñas, enlaces de emparejamiento ni el contenido de un `.env` | El mensaje queda en su chat |
| No lanzar trabajadores de Orca en la estación sin permiso del coordinador | Un trabajador es otro agente con acceso a sus archivos |

## 4. Ver si la estación está libre

Tablero en la Mac, en modo solo lectura: <http://127.0.0.1:3000/d/uondr-estaciones>. En **01 · EN VIVO** se miran Bakes, Procesador, RAM usada y Temp. procesador.

Por consulta, cuántos bakes corren ahora:

```bash
curl -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=count by (estacion) (windows_process_info{process="3dsmaxbatch"})'
```

Sin resultado significa cero bakes.

## 5. Dónde guarda el agente su documentación

- En una carpeta propia dentro de su repo, que el agente elige y donde no trabajan otros agentes.
- No edita `CLAUDE.md`, `AGENTS.md` ni archivos de otros sin permiso del coordinador.
- Los valores reales de máquinas y sesiones van solo en un archivo que git ignora.
- Si hace commit, agrega solo sus archivos y por ruta, nunca `git add -A`.

## 6. Prueba del canal

**Antes:** el coordinador avisa a la arquitecta, y ella escribe en su chat algo como:

> Vas a recibir mensajes del coordinador por Orca. Puedes responderlos con `orca orchestration reply` y usar la carpeta `C:\UONDR-entregas`.

| Paso | Quién | Qué | Criterio |
|---|---|---|---|
| 1 | Agente de la Mac | Deja `para-estacion/prueba-canal-<fecha>.txt` y calcula su huella | — |
| 2 | Agente de la Mac | Manda un mensaje con tres pedidos: **a)** una pregunta que solo responde quien tiene el contexto, como la última versión entregada y dónde se generan los ZIP; **b)** verificar la huella del archivo de prueba; **c)** crear `para-mac/prueba-canal-<fecha>.txt` y responder con su huella | El mensaje aparece en el chat de la estación |
| 3 | Agente de la estación | Responde con `orca orchestration reply` | La respuesta llega a la Mac sin WhatsApp |
| 4 | Agente de la Mac | Copia el archivo de `para-mac/` y compara la huella | Huellas iguales en las dos direcciones |
| 5 | Agente de la Mac | Borra los dos archivos de prueba | Carpeta limpia |

Reporte al coordinador: hora de envío, hora de respuesta, las dos huellas y cualquier error tal cual salió.
