import bpy
import bmesh
C = bpy.context
D = bpy.data
obj = C.active_object

VERTEX_GROUP = 'displace'
QUANTITIZATION_LEVELS  = 20
EXTRUDE_DISTANCE=-0.1

group = obj.vertex_groups[VERTEX_GROUP]
q_offset=1/QUANTITIZATION_LEVELS/2

orig_verts = obj.data.vertices
for q in range(1, QUANTITIZATION_LEVELS+1):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    selected = 0
    for v in orig_verts:
        try:
            weight=group.weight(v.index)
        except:
            weight=0
        select = weight>=q/QUANTITIZATION_LEVELS-q_offset and weight<=q/QUANTITIZATION_LEVELS+q_offset and weight > 0
        v.select = select #Setting to false doesn't actually deselect!!
        if select:
            print(v.index, weight, select)
            selected += 1
            
    print(q/QUANTITIZATION_LEVELS,'SELECTED:',selected)
    if selected > 0:
        obj.data.vertices.update()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.extrude_region_shrink_fatten(TRANSFORM_OT_shrink_fatten={"value":q/QUANTITIZATION_LEVELS*EXTRUDE_DISTANCE,"use_even_offset":True})

bpy.ops.object.mode_set(mode='OBJECT')