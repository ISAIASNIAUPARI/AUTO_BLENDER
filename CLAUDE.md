# Proyecto: AUTO_BLENDER — escena comparativa de viviendas

Cuando alguien abra este repo en una sesión nueva pidiendo "restaura la escena de
Blender" o similar:

1. Asegúrate de que Blender está abierto y el **MCP de Blender** conectado.
2. Lee **RESTORE.md** y síguelo. En resumen: abrir `assets/scene.blend` con
   `bpy.ops.wm.open_mainfile()` restaura el 100% del estado (archivo autocontenido,
   Blender 5.2.1 LTS, EEVEE).
3. Verifica con el bloque de comprobación de RESTORE.md: 4 escenas
   (`COMPARATIVA`, `MANSION`, `PLAN_A`, `PLAN_B`), 648 objetos, 40 materiales.

## Reglas

- La fuente de verdad es `assets/scene.blend`. `exports/COMPARATIVA.glb` es solo
  previsualización — nunca restaurar desde el GLB.
- El bloque CASA + GARAJE no lleva coche (se eliminó a propósito). No lo vuelvas a añadir
  salvo que lo pidan.
- No modifiques la geometría al restaurar; solo abrir y verificar.
- Si guardas cambios, hazlo sobre `assets/scene.blend` y actualiza `renders/comparativa.png`.
