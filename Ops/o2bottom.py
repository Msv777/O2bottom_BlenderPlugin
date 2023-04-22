import bpy # type: ignore
from mathutils import Vector # type: ignore

def align_to_bottom(context):
    print("debug success")
    # 在这里添加操作代码
    try:
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            #取消选择物体,因为设置原点用的代码会将所有物体原点设置到游标而不能使用只在循环内用obj.origin_set
            for obj2 in selected_objects:
                obj2.select_set(False)
            #复制一份,以计算应用旋转后的bbox
            CaculateBboxObj = obj.copy()
            CaculateBboxObj.data = obj.data.copy()
            bpy.context.collection.objects.link(CaculateBboxObj)
            #选中需要计算的bbox以应用其旋转,同理应用也是用的bpy.ops,所以也只能选中一个物体
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
            #移除网格数据,同时也会移除物体
            bpy.data.meshes.remove(CaculateBboxObj.data,do_unlink=True)
            obj.select_set(True)
            bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
            cursor.rotation_euler = cursor_rot
            cursor.location = cursor_loc               
        #因为是逐个选中处理的,所以最后还原选中状态
        for obj in selected_objects:
                obj.select_set(True)
        bpy.ops.ed.undo_push(message="Align_ori_to_Bottom")
    except Exception as e:
        print("An error occurred:", e)     


class align_to_bottom_OperatorClass(bpy.types.Operator):
    bl_idname = "o2bottom.align_to_bottom"
    bl_label = "Align to Bottom"
    bl_description = "Align object origin to the bottom of its bounding box"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            self.report({"WARNING"}, "msv:Please switch to ObjectMode")
            return {"CANCELLED"}
        else:
            align_to_bottom(context)
        return {"FINISHED"}