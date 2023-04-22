import bpy #type:ignore

bl_info = {
    "name": "o2bottom",
    "author": "MSV",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Tool",
    "description": "用于将物体原点放置到包围盒底部的脚本插件-_-",
    "warning": "msv is watching you",
    "wiki_url": "msv",
    "category": "3D View",
}
from .Ops.o2bottom import align_to_bottom_OperatorClass
from .Panels.Panel import msvpanel
def register():
    print("hello")
    bpy.utils.register_class(msvpanel)
    bpy.utils.register_class(align_to_bottom_OperatorClass)
def unregister():
    bpy.utils.unregister_class(msvpanel)
    bpy.utils.unregister_class(align_to_bottom_OperatorClass)
if __name__ == "__main__":
    register()