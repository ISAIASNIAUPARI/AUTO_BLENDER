# KOMI — modelo 3D de personaje (image → 3D)

Modelo 3D de un personaje estilo Komi-san generado a partir de una hoja de personaje
2D, mediante **Higgsfield → Tripo H3.1 Multiview**, y limpiado en Blender 5.2.1 LTS.

No tiene relación con la escena COMPARATIVA de viviendas del repo — es trabajo aparte
guardado aquí.

## Contenido

```
komi/
├── komi.blend              Blender 5.2.1 LTS, autocontenido (texturas empacadas).
│                           Escena "Scene": colección KOMI_3D → objeto HERO_komi.
│                           Escena "KOMI_REVIEW": HERO_komi + KomiCam + KomiKey/KomiFill
│                           (set de luces para renders de vueltas).
├── komi_limpio.glb         Export glTF del modelo YA LIMPIO (sin el artefacto). 738.669 verts / 1.424.770 caras.
├── komi_original.glb       Export tal cual salió de Tripo, CON el artefacto de lámina flotante. Solo referencia.
├── hoja_personaje.png      Imagen fuente (hoja de personaje 2D, 1024×1536).
├── vistas_usadas/          Los 3 recortes exactos que se pasaron al generador.
│   ├── 1_frontal.png       crop=242:748:42:14  (de hoja_personaje.png)
│   ├── 2_perfil.png        crop=236:748:296:14
│   └── 3_trasera.png       crop=216:748:540:14
└── renders/                Renders de referencia (EEVEE, escena KOMI_REVIEW).
    ├── turnaround.png       4 ángulos en fila (modelo limpio)
    └── clean_front/threeq/left/back.png
```

## Cómo se generó (para replicar)

| Paso | Detalle |
|------|---------|
| Entrada | 1 hoja de personaje → recortada en 3 vistas (ver `vistas_usadas/`) |
| Modelo | **Tripo H3.1 Multiview to 3D** (`tripo_h3_1_multiview_to_3d`) vía Higgsfield MCP `generate_3d` |
| Prompt | **ninguno** — Tripo multiview ignora el texto; todo viene de las imágenes |
| Parámetros | `texture=true`, `pbr=true`, `orientation=align_image`, geometría/textura `standard` |
| Orden de imágenes | frontal → perfil → trasera |
| Costo | 9 créditos Higgsfield |

## Limpieza aplicada en Blender

Tripo dejó una **lámina plana flotante** (~1–5 mm de grosor) fragmentada en 27 islas,
todas desplazadas al -X (`x ≈ -0.148` local) respecto al personaje (`x ≈ +0.06`).
Se eliminaron por detección de islas de malla: se borró toda isla con
`centro_x < -0.08` **y** `flatness < 0.2`. El cuerpo (toda su geometría en `x > -0.05`)
quedó intacto. Resultado: −23.015 verts / −42.606 caras.

## Notas

- El modelo mira hacia **+X** tal como está en `komi.blend`. Rótalo −90° en Z para que mire a −Y (frente estándar de Blender).
- Está escalado a **1,6 m**, pies en `z = 0`, centrado en XY.
- **1,42 M triángulos** — pesado. Para animar conviene retopología / decimate.
- La cara sale plana/estilizada y el pelo algo "blob": límites normales de single/multi-image → 3D con arte anime.
- Fuente de verdad de este submódulo: `komi.blend`. Los `.glb` son para previsualizar.
