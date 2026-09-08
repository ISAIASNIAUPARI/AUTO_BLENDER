# AUTO_BLENDER — Proyecto de auto deportivo procedural

Este repositorio contiene el trabajo hecho en una sesión de Claude Code usando el MCP de Blender: un auto deportivo estilizado (inspirado en un Porsche 911) construido **100% por código Python/bpy** — carrocería por secciones transversales, arcos de rueda cortados con boolean, interior, luces, vidrios y materiales.

## Contenido

- `porsche_project.blend` — el archivo de Blender con la escena completa (carrocería, ruedas, interior, luces, cámara).
- `build_car.py` — script Python standalone que reconstruye el auto desde cero dentro de Blender (por si el `.blend` se pierde o se corrompe).
- `renders/` — capturas de referencia del resultado (vista 3/4 y vista lateral).

## Cómo restaurar esto en Blender

### Opción A — Abrir el archivo directamente (más rápido)
1. Abre Blender.
2. `Archivo > Abrir` → selecciona `porsche_project.blend`.
3. Listo, la escena completa se carga tal cual quedó.

### Opción B — Reconstruir desde cero con el script
Si prefieres reconstruir todo desde código (por ejemplo, para seguir iterando con Claude + MCP de Blender):

1. Abre Blender con una escena vacía.
2. Ve a la pestaña **Scripting**.
3. Abre `build_car.py` y ejecútalo (▶ Run Script), o pégalo en la consola Python.
4. El script limpia la escena y reconstruye: carrocería (12 estaciones transversales), arcos de rueda (boolean), ruedas, vidrios, luces, interior, materiales, cámara e iluminación de estudio.

### Opción C — Restaurar vía MCP con Claude
Si estás trabajando con Claude Code + el MCP de Blender, simplemente pide:

> "Abre el archivo porsche_project.blend de este repo en Blender"

o

> "Ejecuta build_car.py en Blender para reconstruir el auto"

## Notas técnicas

- La carrocería usa una técnica de **secciones transversales (bmesh)**: 12 estaciones a lo largo del eje X, cada una con un anillo de 8 vértices, conectadas para formar la silueta lateral tipo fastback.
- Los **arcos de rueda** están cortados con un modifier Boolean (solver `FLOAT`, más estable que `EXACT` en esta versión de Blender — `EXACT` causó un crash de Blender durante el desarrollo).
- Motor de render probado: EEVEE.
- Todas las posiciones de detalles (luces, escape, spoiler, vidrios) fueron verificadas con raycast contra la malla evaluada (post-modifiers) para evitar que queden flotando separados de la carrocería.

## Estado del proyecto

Interpretación estilizada de un auto deportivo — **no es una réplica exacta** de ninguna foto de referencia. La silueta, los arcos de rueda integrados y las proporciones generales están correctas; algunos detalles menores (nariz, acabados) quedan pendientes de pulir.
