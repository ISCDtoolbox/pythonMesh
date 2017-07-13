import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
import colorsys
from . import msh
from . import operator_export_mesh as exp
import os

#Define the operator names, properties and function
operatorID   = "preview.medit"
operatorText = "Preview in medit"
class operator(bpy.types.Operator):
    """Previews a .mesh file in medit"""
    bl_idname = operatorID
    bl_label = operatorText
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and context.active_object.type == 'MESH' and len(context.selected_objects)==1)
    def execute(self, context):
        err = operatorFunction(self, context)
        if err:
            return {'CANCELLED'}
        else:
            return {'FINISHED'}
def operatorFunction(operator, context):
    bpy.ops.export_mesh.mesh(filepath="tmp.mesh")
    os.system("medit tmp.mesh")
    os.system("rm tmp.mesh")
    return 0

#register and unregister
def register():
    bpy.utils.register_class(operator)
def unregister():
    bpy.utils.unregister_class(operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
