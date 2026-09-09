# RESTORE.md — Restaurar esta escena en una sesión nueva

Instrucciones para un agente (Claude Code con el **MCP de Blender** conectado y Blender
abierto). Objetivo: dejar la escena EXACTAMENTE igual que cuando se subió a este repo.

## 0. Requisitos

- Blender **5.2.1 LTS** o superior, abierto, con el add-on MCP activo y conectado.
- Este repositorio clonado en local. La ruta del `.blend` clave es:
  `<repo>/assets/scene.blend`

## 1. Abrir el archivo (paso único de restauración)

Todo el estado vive dentro de `assets/scene.blend`. Es autocontenido: sin librerías
enlazadas, sin archivos que falten, sin texturas externas. Ejecuta vía MCP:

```python
import bpy, os
ruta = os.path.abspath(os.path.join(RUTA_DEL_REPO, "assets", "scene.blend"))
bpy.ops.wm.open_mainfile(filepath=ruta)
```

Con eso la escena queda restaurada al 100%. Los pasos siguientes son solo verificación.

## 2. Verificar que coincide

Ejecuta y compara con los valores esperados:

```python
import bpy
chk = {
    "blender": bpy.app.version_string,           # esperado: "5.2.1 LTS" o superior
    "escenas": sorted(s.name for s in bpy.data.scenes),
    "objetos_totales": len(bpy.data.objects),    # esperado: 648
    "materiales": len(bpy.data.materials),       # esperado: 41
    "escena_activa": bpy.context.window.scene.name,
    "cam_comparativa": bpy.data.scenes["COMPARATIVA"].camera.name,  # esperado: "C_Cam"
}
print(chk)
```

Valores esperados:

| Clave | Valor |
|-------|-------|
| escenas | `['COMPARATIVA', 'MANSION', 'PLAN_A', 'PLAN_B']` |
| objetos_totales | `648` |
| materiales | `41` |
| cam_comparativa | `C_Cam` |

### Escenas y su contenido

| Escena | Objetos | Cámara | Motor | Resolución | Colecciones |
|--------|--------:|--------|-------|------------|-------------|
| **COMPARATIVA** | 9 | `C_Cam` | EEVEE | 2400×1250 | (usa empties de instancia) |
| **MANSION** | 289 | `CAM` | EEVEE | 2200×1240 | MANSION, GROUNDS, ROOFS, PORTICO, WINDOWS, DETAIL |
| **PLAN_A** (casa + garaje) | 176 | `PA_Cam` | EEVEE | 2000×1450 | PLAN_A_C |
| **PLAN_B** (apartamento 3 dorm.) | 174 | `PB_Cam` | EEVEE | 2000×1450 | PLAN_B_C |

### Estructura de la escena COMPARATIVA

`Scene Collection` contiene:
- `C_Cam` (cámara), `C_Ground` (mesh), `C_Sun` (luz)
- `I_Mansion` — empty de instancia → colección `MANSION_GRP`
- `I_PlanA` — empty de instancia → colección `PLAN_A_C`
- `I_PlanB` — empty de instancia → colección `PLAN_B_C`
- `LBL_MANSION`, `LBL_CASA + GARAJE`, `LBL_APARTAMENTO 3 DORM.` (objetos de texto)

Mundo: `C_World`. Workspace de Blender activo: `Genérico`.

## 3. Render de referencia

Debe verse igual que `renders/comparativa.png` (los tres bloques en fila, la mansión a
la izquierda; el bloque CASA + GARAJE **NO tiene coche**).

```python
import bpy
bpy.context.window.scene = bpy.data.scenes["COMPARATIVA"]
bpy.ops.render.render(write_still=False)
```

## 4. Estado / historial

- El coche que había en el garaje (`f_carb`, `f_carc`, `f_carg`, `f_wheel`,
  `f_wheel.001..003`) fue **eliminado** antes de subir. No debe reaparecer.
- `exports/COMPARATIVA.glb` es solo para previsualizar en visores glTF; **no** es la
  fuente de verdad. Restaura siempre desde `assets/scene.blend`.

## 5. Si el .blend no abre

- Confirma versión de Blender (`bpy.app.version_string`). El archivo se guardó con 5.2.1 LTS.
- Comprueba archivos que falten:
  ```python
  import bpy
  print([f for f in bpy.utils.blend_paths(absolute=True)])
  ```
  La lista debe estar vacía (todo empaquetado).
