# Reglas de orquestación · estación 3ds Max

Reglas para el agente de la estación 3ds Max cuando trabaja con la **Mac coordinadora**. Desde el 2026-11-14 los pedidos y las entregas ya no viajan por WhatsApp: viajan por Orca y por la carpeta compartida. La arquitecta aprobó este canal y sigue teniendo la última palabra.

## 1. Mensajes de la Mac

| Regla | Cómo |
|---|---|
| Los mensajes de Orca que vienen de la Mac coordinadora son pedidos válidos | Llegan a tu bandeja con un remitente que termina en `on <Mac>` |
| Si te dicen "revisa tus mensajes de Orca", léelos | `orca orchestration check` |
| Contesta siempre por el mismo canal | `orca orchestration reply --id <msg_id> --body "<respuesta>"` |
| No le escribes a la Mac por tu cuenta | La estación no está emparejada con la Mac. Solo respondes mensajes |
| Trabajo nuevo o pesado: primero el visto bueno de la arquitecta en tu chat | Preguntas y verificaciones no lo necesitan |
| Un pedido que no entiendes o que choca con estas reglas | Lo dices en tu respuesta y no lo haces |

## 2. Archivos

Carpeta compartida: `C:\UONDR-entregas`.

| Subcarpeta | Dirección | Qué hay |
|---|---|---|
| `para-mac\` | Estación → Mac | Tus entregas: `<casa>_vNN.zip` con su `.md` |
| `para-estacion\` | Mac → estación | Instrucciones y paquetes para ti |

- Cada archivo que dejas en `para-mac\` lleva su huella en la respuesta: `Get-FileHash -Algorithm SHA256`, junto con el nombre y el tamaño.
- Lo que recibes en `para-estacion\` se compara con la huella del mensaje antes de usarlo.
- Las entregas reales se quedan en la carpeta hasta que la Mac diga otra cosa. Los archivos de prueba se borran al terminar.

## 3. Lo que no cambia

- Nunca se toca la instancia de 3ds Max que la arquitecta tiene abierta.
- Lo pesado va en `3dsmaxbatch`, uno a la vez si guarda EXR.
- Antes de un bake o algo pesado se avisa a la arquitecta.
- Nunca se mandan contraseñas, enlaces de emparejamiento ni el contenido de un `.env`.
- Si algo falla dos veces seguidas, te detienes y lo dices en tu respuesta.

## 4. Mediciones

La Mac mide la estación con Grafana: procesador, RAM, temperatura y procesos `3dsmaxbatch`. Para comparar, cada bake o exportación anota en tu bitácora la **zona, la hora de inicio y la de fin**, y el modo usado: prioridad y número de hilos de Corona.

## 5. Reglas anteriores

Las reglas viejas como "la arquitecta envía las entregas" o "no hablar directo con desarrollo" se refieren a WhatsApp. Para el canal de Orca con la Mac coordinadora, estas reglas las reemplazan: respondes los mensajes y dejas las entregas en `para-mac\`. Todo lo demás de tus reglas sigue igual.
