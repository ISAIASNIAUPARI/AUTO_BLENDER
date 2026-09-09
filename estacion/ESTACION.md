# ESTACION — escena de estación de tren nocturna (3D Jutsu)

Escena de blocking cinematográfico creada por el usuario manualmente en
**Higgsfield 3D Jutsu** (constructor de escenas en navegador).

- Proyecto Higgsfield: `9d222b57-7cbb-4ad4-aef1-76d5b7af149f` (revisión 34)
- 255 objetos, EEVEE, 480×270, 24 fps, frames 1–360 (15 s)
- Cámara `CAM_main` (26 mm) + `TGT_cam_look`, ambas animadas 1→360:
  plano abierto del andén → push-in avanzando junto al tren → cierre en una
  ventana iluminada del vagón ("reveal").
- Contenido: andén mojado con charcos, marquesina con lámpara cálida, máquina
  expendedora, banco, cartel, **2 trenes** (ventanas, puertas, ruedas,
  pantógrafo), catenaria, vías con traviesas, ~16 árboles, montañas, bancos de
  niebla, nieve, luna (SUN) + 6 luces (frías + prácticas cálidas).

## Archivos

| Archivo | Qué es |
|---|---|
| `estacion_jutsu.glb` | 217 KB — export glTF de la escena (con la cámara animada) |
| `estacion_jutsu.blend` | 2 MB — Blender 5.2, editable |
| `jf040.png` `jf200.png` `jutsu_f360.png` | frames 40 / 200 / 360 (blocking, ruidosos) |

## Estado / siguiente paso

Es **blocking**, no acabado. El flujo previsto: exportar el video desde 3D Jutsu
→ pasarlo a Claude como referencia → prompt segundo a segundo → generar el video
fotorrealista con un motor IA (Kling/Seedance). También reutilizable como
**escenario / nivel** para un juego de navegador (ver el prompt de la sesión de juego).
