# import bpy
# from mathutils import Vector # type: ignore
# from mathutils import Matrix
# selected_objects = bpy.context.selected_objects 
# for obj in selected_objects:
#     for obj2 in selected_objects:
#         obj2.select_set(False)
#     obj.select_set(True)
   
#     for obj2 in selected_objects:
#         obj2.select_set(False)
#     obj.select_set(True)
#     bbox = obj.bound_box
#     bbox_world = [obj.matrix_world @ Vector(b) for b in bbox]
                    
#     # bbox底部,分别是负半象限顺时针旋转一圈,正半象限旋转一圈,最后一个点和第一个点是斜对角线
#     bottomcenter = (bbox_world[0] + bbox_world[7]) / 2
    
#     bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=bbox_world[0])
#     bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=bbox_world[7]) 
#     print(bbox_world[0],bbox_world[7])
#     # 用游标设置哈
#     cursor = bpy.context.scene.cursor
#     cursor_loc = cursor.location.copy()
#     cursor_rot = cursor.rotation_euler.copy()
                    
#     cursor.rotation_euler = (0,0,0)#obj.rotation_euler.copy()
#     cursor.location = bottomcenter
#     bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
#     cursor.rotation_euler = cursor_rot
#     cursor.location = cursor_loc

import bpy
from mathutils import Vector # type: ignore

selected_objects = bpy.context.selected_objects
for obj in selected_objects:
    for obj2 in selected_objects:
        obj2.select_set(False)
    CaculateBboxObj = obj.copy()
    CaculateBboxObj.data = obj.data.copy()
    bpy.context.collection.objects.link(CaculateBboxObj)
    CaculateBboxObj.select_set(True)
    #如果物体有旋转值,那么bbox也会跟着旋转;而不是还是保持不旋转
    if obj.rotation_euler != (0,0,0):
        #应用的是复制物体的旋转
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bbox =  CaculateBboxObj.bound_box
    bbox_world = [CaculateBboxObj.matrix_world @ Vector(b) for b in bbox]
                    
    # bbox底部,分别是负半象限顺时针旋转一圈,正半象限旋转一圈,最后一个点和第一个点是斜对角线
    bottomcenter = (bbox_world[0] + bbox_world[7]) / 2

    # 用游标设置哈
    cursor = bpy.context.scene.cursor
    cursor_loc = cursor.location.copy()
    cursor_rot = cursor.rotation_euler.copy()
                    
    cursor.rotation_euler = (0,0,0)#obj.rotation_euler.copy()
    cursor.location = bottomcenter
    bpy.data.meshes.remove(CaculateBboxObj.data,do_unlink=True)
    obj.select_set(True)
    bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
    cursor.rotation_euler = cursor_rot
    cursor.location = cursor_loc               

bpy.ops.ed.undo_push(message="Align_ori_to_Bottom")

    
   