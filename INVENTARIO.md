# INVENTARIO — assets reutilizables

Todo lo generado en el proyecto WEB_CON_ANIMACION, guardado para reutilizar
(ej. en un juego de navegador de Higgsfield).

| Asset | Carpeta | Archivo principal | Origen | Notas |
|---|---|---|---|---|
| **Personaje anime (Komi)** | `komi/` | `komi_limpio.glb` (~40 MB) · `komi.blend` (59 MB) | Tripo H3.1 Multiview desde hoja 2D | limpiado en Blender; para web hay una versión de 0.58 MB (ver repo WEB / cerebro) |
| **Camiseta técnica (Nike Academy)** | `camiseta/` | `camiseta_web.glb` (224 KB) · `camiseta_original.glb` (1.6 MB) | Tripo H3.1 Multiview, `face_limit=40000` (sin Blender) | Draco + WebP 1K; lista para navegador |
| **Estación de tren nocturna** | `estacion/` | `estacion_jutsu.glb` (217 KB) · `estacion_jutsu.blend` (2 MB) | Higgsfield 3D Jutsu (manual) | escenario completo: 2 trenes, andén, catenaria, bosque, niebla, nieve; cámara animada |
| **Comparativa de viviendas** | `assets/` | `scene.blend` (324 KB) · `exports/COMPARATIVA.glb` | Blender (proyecto original del repo) | MANSION + CASA/GARAJE + APARTAMENTO. El coche del garaje fue **eliminado** — NO hay asset de coche |

## No disponible
- **Coche / auto**: no existe como asset. Había uno en el garaje de la escena de viviendas y se borró antes de subir.
- **Video final de Londres (jet)**: no está aquí; está en Cloudinary y en la web `londres-jet.vercel.app`.

## Dónde está el resto
- Web viva de referencia: https://londres-jet.vercel.app
- Cerebro/protocolo (Obsidian): vault `ARQUITECTURA_DE_DATOS` → carpeta `protocolo-web-3d/`
