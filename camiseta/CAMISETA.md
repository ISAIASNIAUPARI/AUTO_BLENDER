# CAMISETA — modelo 3D de producto (image → 3D, sin Blender)

Camiseta técnica (mockup 2D estilo Nike Academy) reconstruida en 3D con
**Higgsfield → Tripo H3.1 Multiview**. A diferencia de `komi/`, esta **NO pasó por
Blender**: se limitó la geometría en la propia generación y se comprimió con
`@gltf-transform/cli` (herramienta CLI, no Blender).

## Contenido

```
camiseta/
├── camiseta_original.glb   Tal cual salió de Tripo (face_limit=40000). 1.6 MB, ~22 k tris, texturas 2K JPEG.
├── camiseta_web.glb        Optimizado con gltf-transform: 1K WebP + Draco. 224 KB. Es el que sirve la web.
├── hoja_mockup.png         Imagen fuente (1536×1024, 3 vistas + detalles).
└── vistas_usadas/          Los 3 recortes exactos pasados al generador.
    ├── 1_frontal.png       crop=470:740:35:55   (de hoja_mockup.png)
    ├── 2_perfil.png        crop=430:740:555:55
    └── 3_trasera.png       crop=470:740:1035:55
```

## Cómo se generó (replicable)

| Paso | Detalle |
|------|---------|
| Entrada | 1 hoja mockup → 3 recortes (frontal / perfil / trasera), en ese orden |
| Modelo | **Tripo H3.1 Multiview to 3D** (`tripo_h3_1_multiview_to_3d`) vía Higgsfield MCP |
| Prompt | ninguno (multiview lo ignora) |
| Parámetros | `texture=true`, `pbr=true`, `orientation=align_image`, **`face_limit=40000`** |
| Costo | 9 créditos Higgsfield |
| Post (sin Blender) | `npx @gltf-transform/cli optimize in.glb out.glb --texture-size 1024 --texture-compress webp --compress draco` → 1.6 MB → 224 KB |

## En la web

Servido desde Cloudinary raw: `https://res.cloudinary.com/foewxv45/raw/upload/web_con_animacion/camiseta_web.glb`
Sección "Camiseta técnica Academy" en `londres-jet.vercel.app` (componente `ShirtViewer.tsx`, `<model-viewer>`), con descripción de marca + precios de venta a la derecha.

## Nota

El `face_limit` en la generación evitó tener que decimar en Blender — para un objeto
simple (una prenda) 22 k tris ya es suficiente. Para personajes con más detalle
(ver `komi/`) sí conviene el paso por Blender o subir el face_limit.
