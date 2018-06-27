import bpy
C = bpy.context
D = bpy.data

obj = C.object

group_id = obj.vertex_groups.find('combined')
if group_id == -1:
    print('creating vertex group')
    group_id = obj.vertex_groups.new('combined').index

group = obj.vertex_groups[group_id]
group.remove([vert.index for vert in obj.data.vertices])
group_count = len(obj.vertex_groups)-1

for vert in obj.data.vertices:
    print(vert.index)
    for sgroup in obj.vertex_groups:
        if sgroup.index != group_id:
            try:
                weight = sgroup.weight(vert.index)
            except:
                weight = 0
            print(sgroup.index, vert.index, weight, group_count)
            group.add([vert.index], weight/group_count, 'ADD')