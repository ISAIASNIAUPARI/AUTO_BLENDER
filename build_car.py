"""
build_car.py — Reconstruye el auto deportivo procedural completo.

Uso: Blender > pestaña Scripting > abrir este archivo > Run Script (o botón ▶).
Limpia la escena actual y construye todo desde cero.

Requiere Blender 4.x / 5.x. Motor recomendado: EEVEE.
"""
import bpy, bmesh, math

# ============================================================
# 0. LIMPIAR ESCENA
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for m in list(bpy.data.materials):
    bpy.data.materials.remove(m)
for msh in list(bpy.data.meshes):
    bpy.data.meshes.remove(msh)


def mat(name, color, metallic=0.0, rough=0.4, emit_color=None, emit_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs["Base Color"].default_value = color
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    if emit_color:
        b.inputs["Emission Color"].default_value = emit_color
        b.inputs["Emission Strength"].default_value = emit_strength
    return m


mat_paint = mat("Paint", (0.85, 0.42, 0.04, 1), metallic=0.3, rough=0.12)
mat_dark = mat("Dark", (0.02, 0.02, 0.02, 1), metallic=0.1, rough=0.55)
mat_glass = mat("Glass", (0.05, 0.08, 0.09, 1), metallic=0.0, rough=0.05)
mat_chrome = mat("Chrome", (0.85, 0.85, 0.85, 1), metallic=1.0, rough=0.3)
mat_leather = mat("Leather", (0.35, 0.18, 0.08, 1), metallic=0.0, rough=0.55)
mat_headlight = mat("HeadLight", (1, 1, 0.95, 1), emit_color=(1, 1, 0.9, 1), emit_strength=1.0)
mat_redlight = mat("RedLight", (1, 0.05, 0.02, 1), emit_color=(1, 0.05, 0.02, 1), emit_strength=1.5)

# ============================================================
# 1. CARROCERIA — 12 estaciones transversales x anillo de 8 puntos
# (x, wt,wu,wm,wb, zt,zu,zm,zb)
#   wt/wu/wm/wb = medio-ancho en: techo/tapa, superior, hombro(max), inferior
#   zt/zu/zm/zb = altura en:      techo/tapa, superior, hombro,      inferior
# ============================================================
stations = [
    (4.60, 0.05, 0.15, 0.28, 0.18, 0.38, 0.36, 0.33, 0.24),
    (4.45, 0.08, 0.25, 0.55, 0.42, 0.42, 0.40, 0.35, 0.22),
    (4.15, 0.12, 0.35, 0.92, 0.78, 0.55, 0.50, 0.44, 0.22),  # rueda delantera aqui
    (3.55, 0.14, 0.40, 0.85, 0.74, 0.63, 0.55, 0.44, 0.22),
    (2.90, 0.12, 0.38, 0.82, 0.72, 0.72, 0.55, 0.44, 0.22),
    (2.30, 0.10, 0.34, 0.80, 0.70, 1.03, 0.68, 0.44, 0.22),
    (1.75, 0.10, 0.34, 0.80, 0.70, 1.10, 0.70, 0.44, 0.22),
    (1.10, 0.10, 0.34, 0.80, 0.70, 1.03, 0.68, 0.44, 0.22),
    (0.55, 0.12, 0.36, 0.85, 0.74, 0.78, 0.60, 0.46, 0.22),
    (0.05, 0.14, 0.42, 1.00, 0.86, 0.65, 0.55, 0.46, 0.22),  # rueda trasera aqui
    (-0.35, 0.12, 0.32, 0.75, 0.62, 0.56, 0.50, 0.42, 0.22),
    (-0.68, 0.08, 0.20, 0.42, 0.32, 0.46, 0.42, 0.36, 0.24),
]

bm = bmesh.new()
rings = []
for (x, wt, wu, wm, wb, zt, zu, zm, zb) in stations:
    v0 = bm.verts.new((x, wt, zt))
    v1 = bm.verts.new((x, wu, zu))
    v2 = bm.verts.new((x, wm, zm))
    v3 = bm.verts.new((x, wb, zb))
    v4 = bm.verts.new((x, -wb, zb))
    v5 = bm.verts.new((x, -wm, zm))
    v6 = bm.verts.new((x, -wu, zu))
    v7 = bm.verts.new((x, -wt, zt))
    rings.append([v0, v1, v2, v3, v4, v5, v6, v7])

for i in range(len(rings) - 1):
    r1, r2 = rings[i], rings[i + 1]
    for k in range(8):
        a, b_ = r1[k], r1[(k + 1) % 8]
        c, d = r2[(k + 1) % 8], r2[k]
        bm.faces.new((a, b_, c, d))
bm.faces.new(rings[0][::-1])
bm.faces.new(rings[-1])
bm.normal_update()

mesh = bpy.data.meshes.new("Body_mesh")
bm.to_mesh(mesh)
bm.free()

body = bpy.data.objects.new("Car_Body", mesh)
bpy.context.collection.objects.link(body)
body.data.materials.append(mat_paint)

# ============================================================
# 2. ARCOS DE RUEDA (boolean) — usar solver FLOAT, EXACT crashea Blender
# ============================================================
wheel_positions = [(4.15, -0.90, 0.35), (4.15, 0.90, 0.35), (0.05, -0.90, 0.35), (0.05, 0.90, 0.35)]
cutters = []
for i, pos in enumerate(wheel_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.5, location=pos, vertices=20)
    c = bpy.context.active_object
    c.name = f"ArchCutter_{i}"
    c.rotation_euler[0] = math.radians(90)
    bpy.ops.object.transform_apply(rotation=True)
    cutters.append(c)

bpy.ops.object.select_all(action='DESELECT')
for c in cutters:
    c.select_set(True)
bpy.context.view_layer.objects.active = cutters[0]
bpy.ops.object.join()
cutter_all = bpy.context.active_object
cutter_all.name = "ArchCutterAll"

bool_mod = body.modifiers.new("WheelArches", 'BOOLEAN')
bool_mod.object = cutter_all
bool_mod.operation = 'DIFFERENCE'
bool_mod.solver = 'FLOAT'
bpy.context.view_layer.objects.active = body
bpy.ops.object.modifier_apply(modifier="WheelArches")
bpy.data.objects.remove(cutter_all, do_unlink=True)

bev = body.modifiers.new("Bevel", 'BEVEL')
bev.width = 0.02
bev.segments = 2
sub = body.modifiers.new("Subsurf", 'SUBSURF')
sub.levels = 1
sub.render_levels = 1

# ============================================================
# 3. RUEDAS (neumatico + rin), escaladas 0.78x para proporcion correcta
# ============================================================
WHEEL_SCALE = 0.78
for i, pos in enumerate(wheel_positions):
    bpy.ops.mesh.primitive_torus_add(location=pos, major_radius=0.36, minor_radius=0.14,
                                      major_segments=24, minor_segments=12)
    tire = bpy.context.active_object
    tire.name = f"Tire_{i}"
    tire.rotation_euler[0] = math.radians(90)
    bpy.ops.object.transform_apply(rotation=True)
    tire.scale = (WHEEL_SCALE, WHEEL_SCALE, WHEEL_SCALE)
    tire.data.materials.append(mat_dark)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.06, location=pos, vertices=24)
    rim = bpy.context.active_object
    rim.name = f"Rim_{i}"
    rim.rotation_euler[0] = math.radians(90)
    bpy.ops.object.transform_apply(rotation=True)
    rim.scale = (WHEEL_SCALE, WHEEL_SCALE, WHEEL_SCALE)
    rim.data.materials.append(mat_chrome)

# ============================================================
# 4. PISO
# ============================================================
mat_floor = bpy.data.materials.new("Floor")
mat_floor.use_nodes = True
bf = next(n for n in mat_floor.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
bf.inputs["Base Color"].default_value = (0.14, 0.14, 0.15, 1)
bf.inputs["Roughness"].default_value = 0.5
bpy.ops.mesh.primitive_plane_add(size=20, location=(2, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
floor.data.materials.append(mat_floor)

# ============================================================
# 5. VIDRIOS, LUCES, ESPEJOS, ESCAPE, SPOILER
# (posiciones ya verificadas con raycast contra la malla evaluada)
# ============================================================
bpy.ops.mesh.primitive_plane_add(size=1, location=(2.62, 0, 0.85))
w = bpy.context.active_object; w.name = "Windshield"
w.scale = (0.02, 0.68, 0.24); w.rotation_euler[1] = math.radians(33)
bpy.ops.object.transform_apply(scale=True, rotation=True)
w.data.materials.append(mat_glass)

bpy.ops.mesh.primitive_plane_add(size=1, location=(0.85, 0, 0.89))
r = bpy.context.active_object; r.name = "RearGlass"
r.scale = (0.02, 0.65, 0.22); r.rotation_euler[1] = math.radians(-35)
bpy.ops.object.transform_apply(scale=True, rotation=True)
r.data.materials.append(mat_glass)

for i, y in enumerate([-0.60, 0.60]):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(1.70, y, 0.77))
    sw = bpy.context.active_object; sw.name = f"SideWindow_{i}"
    sw.scale = (0.5, 0.02, 0.18)
    bpy.ops.object.transform_apply(scale=True)
    sw.data.materials.append(mat_glass)

for i, y in enumerate([-0.42, 0.42]):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(4.42, y, 0.37), segments=14, ring_count=8)
    hl = bpy.context.active_object; hl.name = f"Headlight_{i}"
    hl.scale = (0.55, 1.0, 0.65)
    bpy.ops.object.transform_apply(scale=True)
    hl.data.materials.append(mat_headlight)

for i, y in enumerate([-0.4, 0.4]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.53, y, 0.44))
    tl = bpy.context.active_object; tl.name = f"Taillight_{i}"
    tl.scale = (0.04, 0.13, 0.06)
    bpy.ops.object.transform_apply(scale=True)
    tl.data.materials.append(mat_redlight)

for i, y in enumerate([-0.80, 0.80]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.35, y, 0.72))
    m_ = bpy.context.active_object; m_.name = f"Mirror_{i}"
    m_.scale = (0.12, 0.05, 0.06)
    bpy.ops.object.transform_apply(scale=True)
    m_.data.materials.append(mat_paint)

for i, y in enumerate([-0.22, 0.22]):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.18, location=(-0.63, y, 0.40), vertices=12)
    ex = bpy.context.active_object; ex.name = f"Exhaust_{i}"
    ex.rotation_euler[1] = math.radians(90)
    bpy.ops.object.transform_apply(rotation=True)
    ex.data.materials.append(mat_chrome)

bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.38, 0, 0.70))
sp = bpy.context.active_object; sp.name = "Spoiler"
sp.scale = (0.12, 0.68, 0.02)
bpy.ops.object.transform_apply(scale=True)
sp.data.materials.append(mat_paint)
for i, y in enumerate([-0.42, 0.42]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.38, y, 0.616))
    st = bpy.context.active_object; st.name = f"SpoilerStrut_{i}"
    st.scale = (0.02, 0.02, 0.064)
    bpy.ops.object.transform_apply(scale=True)
    st.data.materials.append(mat_dark)

# ============================================================
# 6. INTERIOR — asientos, tablero, volante
# ============================================================
for i, y in enumerate([-0.32, 0.32]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.75, y, 0.38))
    sb = bpy.context.active_object; sb.name = f"SeatBase_{i}"
    sb.scale = (0.28, 0.26, 0.07)
    bpy.ops.object.transform_apply(scale=True)
    sb.data.materials.append(mat_leather)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.95, y, 0.60))
    sk = bpy.context.active_object; sk.name = f"SeatBack_{i}"
    sk.scale = (0.05, 0.26, 0.24)
    sk.rotation_euler[1] = math.radians(-12)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    sk.data.materials.append(mat_leather)

bpy.ops.mesh.primitive_cube_add(size=1, location=(2.45, 0, 0.55))
dash = bpy.context.active_object; dash.name = "Dashboard"
dash.scale = (0.08, 0.62, 0.1)
bpy.ops.object.transform_apply(scale=True)
dash.data.materials.append(mat_dark)

bpy.ops.mesh.primitive_torus_add(location=(2.35, -0.30, 0.58), major_radius=0.12, minor_radius=0.015,
                                  major_segments=16, minor_segments=8)
swh = bpy.context.active_object; swh.name = "SteeringWheel"
swh.rotation_euler[1] = math.radians(80)
bpy.ops.object.transform_apply(rotation=True)
swh.data.materials.append(mat_dark)

# ============================================================
# 7. CAMARA, LUCES DE ESTUDIO, FONDO
# ============================================================
bpy.ops.object.light_add(type='AREA', location=(5, -5, 4))
key = bpy.context.active_object
key.data.energy = 500; key.data.size = 5
key.rotation_euler = (math.radians(55), 0, math.radians(45))

bpy.ops.object.light_add(type='AREA', location=(-4, 4, 3))
fill = bpy.context.active_object
fill.data.energy = 200; fill.data.size = 6
fill.rotation_euler = (math.radians(60), 0, math.radians(-135))

bpy.ops.object.light_add(type='AREA', location=(0, 5, 2.5))
rim_l = bpy.context.active_object
rim_l.data.energy = 250; rim_l.data.size = 4
rim_l.rotation_euler = (math.radians(70), 0, math.radians(180))

bpy.ops.object.camera_add(location=(12, -11, 3.2))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(76), 0, math.radians(48))
cam.data.lens = 35
bpy.context.scene.camera = cam

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.12, 0.12, 0.13, 1)

# Viewport en Material Preview para ver colores de inmediato
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'

print("Auto reconstruido: carroceria + arcos de rueda + ruedas + vidrios + luces + interior + camara.")
