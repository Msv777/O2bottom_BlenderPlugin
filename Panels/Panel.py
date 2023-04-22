import bpy  # type: ignore

class msvpanel(bpy.types.Panel):

    bl_label = 'O2Bottom'
    bl_idname = 'msvpanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=False)
        row.operator("o2bottom.align_to_bottom", text="对齐原点到底部")

