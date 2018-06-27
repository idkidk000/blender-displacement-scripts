import bpy
import bmesh
import random

ITERATIONS = 5
SELECT_PERCENT = 1
SELECT_MAX = 50
MIN_EDGES = 3
SMOOTHING = 15
EDGE_LOOP_SELECT_PROBABILITY = 0.8
NON_EDGE_LOOP_EXPAND_PROBABILITY = 0.9
EDGE_LOOP_EXPAND_PROBABILITY = 0.8
CLEAR_GROUP = True
MARK_SHARP = True
MARK_SHARP_OUTER = True
CLEAR_SHARP = True
EDGE_SPLIT = False
SHADE_SMOOTH = True
SUBDIVIDE = True
SUBDIV_MIN_VERTS = 256
SUBDIV_LEVEL = 4
SUBDIV_TYPE = 'CATMULL_CLARK' #or SIMPLE

C = bpy.context
D = bpy.data

obj = C.object
bpy.ops.object.mode_set(mode='OBJECT')
group_id = obj.vertex_groups.find('displace')
if group_id == -1:
    print('creating vertex group')
    group_id = obj.vertex_groups.new('displace').index

group = obj.vertex_groups[group_id]

if SUBDIVIDE and len(obj.data.vertices)<SUBDIV_MIN_VERTS:
    have_modifier = False
    for mod in obj.modifiers:
        if mod.type == 'SUBSURF':
            have_modifier = True
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
    if not have_modifier:
        mod = obj.modifiers.new(name='TEMP_SUBSURF',type='SUBSURF')
        mod.subdivision_type=SUBDIV_TYPE
        mod.levels=SUBDIV_LEVEL
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier='TEMP_SUBSURF')
        

if CLEAR_GROUP:
    group.remove([vert.index for vert in obj.data.vertices])
    
if CLEAR_SHARP:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')        
    bpy.ops.mesh.mark_sharp(clear=True)

for i in range(0,ITERATIONS):
    print('iteration', i)
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = bmesh.from_edit_mesh(obj.data)
    mesh_total_verts=len(mesh.verts)
    # select_percent=SELECT_VERTS/len(mesh.verts)
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_random(percent=SELECT_PERCENT, seed=i*random.randint(1,100), action='SELECT')
    layer_weight = 1/ITERATIONS
    selected = [vert for vert in mesh.verts if vert.select==True]
    deselect_probability = (len(selected)-SELECT_MAX)/max(len(selected),1)
    for vert in selected:
        if (len(vert.link_edges) >= MIN_EDGES - 1) and (random.random() > deselect_probability):
            edge = vert.link_edges[random.randint(0,len(vert.link_edges)-1)]
            for vert2 in edge.verts:
                vert2.select = True
        else:
            vert.select = False
    mesh.select_flush(True)
    edge_loop_mode =  random.random() <= EDGE_LOOP_SELECT_PROBABILITY
    if edge_loop_mode:
        bpy.ops.mesh.loop_multi_select(ring=False)
    mesh.select_flush(True)
    for l in range(0,SMOOTHING):
        if (len([vert for vert in bmesh.from_edit_mesh(obj.data).verts if vert.select == True]) < mesh_total_verts/max(2,ITERATIONS)) or (l==0) or (not edge_loop_mode and random.random()<=NON_EDGE_LOOP_EXPAND_PROBABILITY) or (edge_loop_mode and random.random()<=EDGE_LOOP_EXPAND_PROBABILITY):
            print('select more')
            bpy.ops.mesh.select_more(use_face_step=True)
            mesh.select_flush(True)
        else:
            break
        if l==SMOOTHING-1:
            print('unable to select enough verts')
    for l in range(0,SMOOTHING):
        if (len([vert for vert in bmesh.from_edit_mesh(obj.data).verts if vert.select == True]) >= mesh_total_verts/max(2,ITERATIONS)): 
            print('select fewer')
            bpy.ops.mesh.select_less()
            mesh.select_flush(True)
        else:
            break
        if l==SMOOTHING-1:
            print('unable to deselect enough verts')
            
    verts = [vert.index for vert in mesh.verts if vert.select == True]
    print(len(verts),' verts selected')
    if MARK_SHARP_OUTER:
        bpy.ops.mesh.select_more(use_face_step=True)
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_sharp()
        bpy.ops.mesh.loop_to_region()
        bpy.ops.mesh.select_less()
        
    if MARK_SHARP:
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_sharp()
        bpy.ops.mesh.loop_to_region()
        
    bpy.ops.object.mode_set(mode='OBJECT')
    group.add(verts, layer_weight, 'ADD')

have_modifier = False
for mod in obj.modifiers:
    if mod.type=='DISPLACE':
        if mod.vertex_group=='displace':
            have_modifier = True

if not have_modifier:
    mod = obj.modifiers.new(name='Displace', type='DISPLACE')
    mod.vertex_group = 'displace'
    mod.mid_level = 0
    mod.strength = 0.2

if EDGE_SPLIT:
    have_modifier = False
    for mod in obj.modifiers:
        if mod.type=='EDGE_SPLIT':
            if mod.use_edge_sharp==False:
                mod.use_edge_sharp=True
            have_modifier = True

    if not have_modifier:
        mod = obj.modifiers.new(name='EdgeSplit', type='EDGE_SPLIT')
        mod.use_edge_angle=False
        mod.use_edge_sharp=True

if SHADE_SMOOTH:
    obj.data.use_auto_smooth=not EDGE_SPLIT
    bpy.ops.object.shade_smooth()
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
bpy.ops.object.mode_set(mode='OBJECT')
