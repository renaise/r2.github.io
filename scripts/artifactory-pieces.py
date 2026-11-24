# Artifactory card cover: six pieces in smooth cool materials, no textures (2026-11-24).
# blender -b -P scripts/artifactory-pieces.py -- <outdir>/   then ffmpeg the frames to stage/artifactory/pieces.mp4
import bpy, bmesh, math, sys
from mathutils import Vector

OUT = sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else '/tmp/art/'
SEG = 60            # frames per piece (2s at 30fps)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = 1440, 810
sc.render.fps = 30
sc.frame_start, sc.frame_end = 1, SEG*6
try: sc.render.engine = 'BLENDER_EEVEE'
except TypeError: sc.render.engine = 'BLENDER_EEVEE_NEXT'
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = OUT + 'f_'
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast' if 'AgX - Medium High Contrast' in [i.identifier for i in bpy.types.ColorManagedViewSettings.bl_rna.properties['look'].enum_items] else 'None'

# world: near-black with a faint cool lift
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
bg.inputs[0].default_value = (0.0075, 0.0085, 0.0095, 1); bg.inputs[1].default_value = 1.0

# backdrop: a curved sweep so the floor falls off into the dark like the old cover
back = None
bm = bpy.data.materials.new('back'); bm.use_nodes = True
p = next(n for n in bm.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
p.inputs['Base Color'].default_value = (0.018, 0.019, 0.021, 1); p.inputs['Roughness'].default_value = 0.9


def light(kind, loc, energy, color, size=4):
    d = bpy.data.lights.new(kind+str(loc), kind); d.energy = energy; d.color = color
    if kind == 'AREA': d.size = size
    o = bpy.data.objects.new(d.name, d); o.location = loc; sc.collection.objects.link(o)
    o.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
light('AREA', (-4, -3, 5), 900, (0.86, 0.92, 1.0), 5)     # key, cool
light('AREA', (5, -1, 2), 250, (0.70, 0.82, 1.0), 3)      # fill, colder
light('AREA', (0, 5, 4), 600, (0.80, 0.90, 1.0), 4)       # rim

cam_d = bpy.data.cameras.new('cam'); cam_d.lens = 48
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0, -11.5, 1.4); cam.rotation_euler = (math.radians(84), 0, 0)

def mat(name, rgb, metal=0.0, rough=0.35, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if coat: b.inputs['Coat Weight'].default_value = coat
    return m

def smooth(o):
    for f in o.data.polygons: f.use_smooth = True

def join(objs, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join()
    o = bpy.context.object; o.name = name
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS'); o.location = (0, 0, 0)
    return o

pieces = []
# 1 endless column: stacked rhomboid units
parts = []
for i in range(5):
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.55, radius2=0.22, depth=0.42, location=(0, 0, i*0.84 - 1.68 + 0.21))
    parts.append(bpy.context.object)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.22, radius2=0.55, depth=0.42, location=(0, 0, i*0.84 - 1.68 - 0.21))
    parts.append(bpy.context.object)
o = join(parts, 'column'); o.rotation_euler.z = math.radians(45)
o.data.materials.append(mat('steel', (0.42, 0.50, 0.60), metal=0.6, rough=0.32)); pieces.append(o)

# 2 Möbius ribbon: a thin rectangle swept once round with a half twist; closed, so it shades cleanly
bm2 = bmesh.new(); U, R, Wd, T = 360, 1.15, 0.42, 0.045
cs = [(-Wd, -T), (Wd, -T), (Wd, T), (-Wd, T)]
rings = []
for i in range(U):
    u = 2*math.pi*i/U; ring = []
    for (v, t) in cs:
        c, s_ = math.cos(u/2), math.sin(u/2)
        rv, rz = v*c - t*s_, v*s_ + t*c      # rotate the section by u/2 in the (radial, z) plane
        ring.append(bm2.verts.new(((R+rv)*math.cos(u), (R+rv)*math.sin(u), rz)))
    rings.append(ring)
for i in range(U):
    a_, b_ = rings[i], rings[(i+1) % U]
    sh = 2 if i == U-1 else 0               # after a full turn the section has turned 180 degrees
    for j in range(4):
        bm2.faces.new((a_[j], b_[(j+sh) % 4], b_[(j+1+sh) % 4], a_[(j+1) % 4]))
bmesh.ops.recalc_face_normals(bm2, faces=bm2.faces)
me = bpy.data.meshes.new('mobius'); bm2.to_mesh(me); o = bpy.data.objects.new('mobius', me); sc.collection.objects.link(o)
bv = o.modifiers.new('b', 'BEVEL'); bv.width = 0.02; bv.segments = 3
smooth(o); o.modifiers.new('wn', 'WEIGHTED_NORMAL')
o.rotation_euler = (math.radians(62), 0, 0)
o.data.materials.append(mat('ice', (0.50, 0.66, 0.82), rough=0.22, coat=0.6)); pieces.append(o)

# 3 bust: head, neck, plinth
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.62, location=(0, 0, 0.55)); h = bpy.context.object; h.scale = (0.86, 0.9, 1.12)
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.22, depth=0.7, location=(0, 0, -0.3)); n = bpy.context.object
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.85)); c = bpy.context.object; c.scale = (0.95, 0.75, 0.45)
bev = c.modifiers.new('b', 'BEVEL'); bev.width = 0.03; bev.segments = 3
for x in (h, n): smooth(x)
bpy.context.view_layer.objects.active = c; bpy.ops.object.modifier_apply(modifier='b')
o = join([h, n, c], 'bust'); smooth(o)
o.data.materials.append(mat('porcelain', (0.78, 0.82, 0.88), rough=0.3, coat=0.4)); pieces.append(o)

# 4 pierced sphere (the gyroid's silhouette, without its ripple)
bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=1.15); g = bpy.context.object; smooth(g)
for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.62, location=tuple(1.15*k for k in d))
    cut = bpy.context.object; m = g.modifiers.new('c', 'BOOLEAN'); m.object = cut; m.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = g; bpy.ops.object.modifier_apply(modifier='c'); bpy.data.objects.remove(cut)
bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=0.95); inner = bpy.context.object
m = g.modifiers.new('c', 'BOOLEAN'); m.object = inner; m.operation = 'DIFFERENCE'
bpy.context.view_layer.objects.active = g; bpy.ops.object.modifier_apply(modifier='c'); bpy.data.objects.remove(inner)
rm = g.modifiers.new('r', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = 0.018
bpy.context.view_layer.objects.active = g; bpy.ops.object.modifier_apply(modifier='r')
cs = g.modifiers.new('cs', 'CORRECTIVE_SMOOTH'); cs.iterations = 6
smooth(g); g.name = 'pierced'
g.rotation_euler = (math.radians(20), math.radians(15), 0)
g.data.materials.append(mat('glacier', (0.70, 0.76, 0.84), rough=0.4)); pieces.append(g)

# 5 armillary: three rings and a core
parts = []
for rot in [(0, 0, 0), (math.radians(90), 0, 0), (math.radians(90), 0, math.radians(90))]:
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.035, major_segments=128, minor_segments=16, rotation=rot); parts.append(bpy.context.object)
bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.035, major_segments=128, minor_segments=16, rotation=(math.radians(66), 0, math.radians(30))); parts.append(bpy.context.object)
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.2); parts.append(bpy.context.object)
for x in parts: smooth(x)
o = join(parts, 'armillary'); o.rotation_euler = (math.radians(18), 0, 0)
o.data.materials.append(mat('satin', (0.62, 0.70, 0.80), metal=0.5, rough=0.3)); pieces.append(o)

# 6 totem: stacked solids
parts = []
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.62, depth=0.45, location=(0, 0, -1.3)); parts.append(bpy.context.object)
bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, 0, -0.68)); parts.append(bpy.context.object)
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.4, location=(0, 0, 0.12)); parts.append(bpy.context.object)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.45, depth=0.5, location=(0, 0, 0.77)); parts.append(bpy.context.object)
bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.45, depth=0.6, location=(0, 0, 1.32)); parts.append(bpy.context.object)
for x in parts: smooth(x)
o = join(parts, 'totem')
o.data.materials.append(mat('slate', (0.24, 0.30, 0.40), rough=0.42)); pieces.append(o)

# each piece shows for one segment, turning half a revolution, floating a touch
for k, o in enumerate(pieces):
    o.location = (0, 0, 0.15)
    a, b = 1 + k*SEG, (k+1)*SEG
    for f, hide in [(1, True), (a, False), (b+1, True)]:
        if f < 1: continue
        o.hide_render = hide; o.keyframe_insert('hide_render', frame=f)
        o.hide_viewport = hide; o.keyframe_insert('hide_viewport', frame=f)
    if k == 0:
        o.hide_render = False; o.keyframe_insert('hide_render', frame=1)
    base = o.rotation_euler.z
    o.rotation_euler.z = base - math.radians(40); o.keyframe_insert('rotation_euler', index=2, frame=a)
    o.rotation_euler.z = base + math.radians(40); o.keyframe_insert('rotation_euler', index=2, frame=b)
    for fc in (o.animation_data.action.fcurves if hasattr(o.animation_data.action, 'fcurves') else []):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR' if fc.data_path == 'rotation_euler' else 'CONSTANT'

if '--still' in sys.argv:
    for k in range(6):
        sc.frame_set(1 + k*SEG + SEG//2); sc.render.filepath = OUT + f'still_{k}.png'; bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
