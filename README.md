<div align="center">

# 🛰️ Agentic Orchestration & Virtualization

**Orquestación de agentes de IA entre las estaciones de trabajo de arquitectura de UONDR**

![Estado](https://img.shields.io/badge/estado-en%20construcci%C3%B3n-f59e0b?style=for-the-badge&logo=hammer&logoColor=white)
![Fase](https://img.shields.io/badge/fase-evaluaci%C3%B3n%20de%20herramientas-6366f1?style=for-the-badge&logo=target&logoColor=white)
![Privado](https://img.shields.io/badge/repo-privado-334155?style=for-the-badge&logo=github&logoColor=white)

![Claude Code](https://img.shields.io/badge/Claude%20Code-D97757?style=flat-square&logo=claude&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-111827?style=flat-square&logo=modelcontextprotocol&logoColor=white)
![Orca](https://img.shields.io/badge/Orca-0EA5E9?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IndoaXRlIi8+PC9zdmc+&logoColor=white)
![Tailscale](https://img.shields.io/badge/Tailscale-242424?style=flat-square&logo=tailscale&logoColor=white)
![Revit 2027](https://img.shields.io/badge/Revit%202027-0696D7?style=flat-square&logo=autodesk&logoColor=white)
![3ds Max](https://img.shields.io/badge/3ds%20Max-37A5CC?style=flat-square&logo=autodesk&logoColor=white)

</div>

---

## 🎯 ¿De qué trata?

En UONDR trabajamos con agentes de IA que operan **Revit** y **3ds Max** a través de servidores MCP en las estaciones de trabajo del equipo de arquitectura. Hoy la comunicación entre agentes es manual (mensajes, zips y reportes `.md`) y cada agente bloquea la aplicación mientras trabaja.

Este proyecto busca que **arquitectos y agentes trabajen en paralelo** y que los agentes **se comuniquen directamente** entre máquinas cuando no se necesita el criterio de una persona.

## 🧩 Objetivos

- ⚡ **Trabajo en paralelo**: que el agente y el arquitecto usen Revit o 3ds Max al mismo tiempo sin bloquearse.
- 🔁 **Canal entre agentes**: mensajes, tareas y resultados sin pasar por WhatsApp.
- 📦 **Entregas automáticas**: que los archivos lleguen, se validen y se publiquen solos.
- 🔥 **Bakes y renders distribuidos**: mover los procesos pesados a nodos de render para acortar ciclos de horas.

## 🧪 Herramientas en evaluación

| | Herramienta | Para qué la estamos revisando |
|---|---|---|
| 🛰️ | **Tailscale** | Red privada y segura entre la Mac de coordinación y las estaciones Windows |
| 🐋 | **Orca** | Servidores remotos y workers federados para orquestar agentes entre máquinas |
| 🤖 | **Claude Code** | Agentes coordinador y trabajadores, en modo interactivo y headless |
| 🏗️ | **rvt-mcp** | Puente MCP con Revit; soporte para varias instancias por proceso |
| 🎨 | **3dsmax-mcp** | Puente MCP con 3ds Max; selección de instancia por proceso |
| 🔥 | **3dsmaxbatch / Backburner** | Bakes y exportaciones sin interfaz y en nodos de render |

## 🗺️ Estado

> [!NOTE]
> 🚧 **Proyecto en construcción.** Estamos en la fase de investigación y pruebas de herramientas. La arquitectura y la documentación cambiarán conforme validemos cada pieza.

- [x] Diagnóstico del flujo actual y de los cuellos de botella
- [x] Investigación de MCPs, licenciamiento de Autodesk y opciones de virtualización
- [ ] Red Tailscale entre las tres máquinas
- [ ] Piloto de Orca con un worker remoto
- [ ] Prueba de segunda instancia de Revit y de bakes con 3dsmaxbatch
- [ ] Ingesta automática de entregas

---

<div align="center">
<sub>Hecho con 🧠 + 🤖 por el equipo de UONDR</sub>
</div>
