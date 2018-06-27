import bpy

GROUP_NAME = 'combined'
SHARP_EDGES_INNER = True
SHARP_EDGES_OUTER = True    
CLEAR_SHARP = True
QUANTITIZATION_LEVELS = 10

C = bpy.context
D = bpy.data
obj = C.object

if CLEAR_SHARP:
    bpy.ops.object.mode_set(mode='OBJECT')
    for vert in obj.data.vertices:
        vert.select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.mark_sharp(clear=True)
    

bpy.ops.object.mode_set(mode='OBJECT')

weights = []
q_offset = 1/QUANTITIZATION_LEVELS/2

group = obj.vertex_groups[GROUP_NAME]
for vert in obj.data.vertices:
    try:
        weight = group.weight(vert.index)
    except:
        weight = 0
    for q in range(1,QUANTITIZATION_LEVELS+1):
        if weight>=q/10-q_offset and weight<=q/10+q_offset:
            weights.append((q, vert.index))
            break

for q in range(1,QUANTITIZATION_LEVELS+1):
    for v in obj.data.vertices:
        v.select = False
    for w in weights:
        if w[0] == q:
            obj.data.vertices[w[1]].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    if SHARP_EDGES_OUTER:
        bpy.ops.mesh.select_more()
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_sharp()
        bpy.ops.mesh.loop_to_region()
        bpy.ops.mesh.select_less()
    if SHARP_EDGES_INNER:
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_sharp()
    bpy.ops.object.mode_set(mode='OBJECT')
    
bpy.ops.object.mode_set(mode='EDIT')