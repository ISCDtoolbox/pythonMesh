import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
import colorsys
from . import msh
from . import operator_export_mesh
import os

#Define the operator names, properties and function
operatorID   = "mesh.tetgen_fill"
operatorText = "Tetgen fill"
class tetgen_fill_operator(bpy.types.Operator):
    """Fills a closed surface with tetgen"""
    bl_idname = operatorID
    bl_label = operatorText

    opt_p = bpy.props.BoolProperty(name="opt_p", description="Piecewise Complex Linear", default=True)
    opt_q = bpy.props.BoolProperty(name="opt_q", description="Refines mesh to improve quality", default=True)
    opt_a = bpy.props.BoolProperty(name="opt_a", description="Maximum volume Constraint", default=True)
    opt_A = bpy.props.BoolProperty(name="opt_A", description="Attributes in different regions", default=True)
    opt_Y = bpy.props.BoolProperty(name="opt_Y", description="Preserves the surface", default=True)
    opt_Q = bpy.props.BoolProperty(name="opt_Q", description="Quiet", default=True)
    prev = bpy.props.BoolProperty(name="preview", description="preview only", default=True)

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and context.active_object.type == 'MESH' and len(context.selected_objects)==1)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        hasTriangulate = False
        obj = bpy.context.scene.objects.active
        maxDim = max(obj.dimensions)
        for m in bpy.context.scene.objects.active.modifiers:
            if m.type == 'TRIANGULATE':
                hasTriangulate = True
        if not hasTriangulate:
            bpy.ops.object.modifier_add(type='TRIANGULATE')

        bpy.ops.export_mesh.mesh(filepath="tmp.mesh")
        bpy.context.scene.objects.active = obj

        if not hasTriangulate:
            bpy.ops.object.modifier_remove(modifier="Triangulate")

        cmd = "/home/norgeot/dev/ext/tetgen1.5.1-beta1/build/tetgen"
        if self.opt_p:
            cmd+= " -p"
        if self.opt_q:
            cmd+= " -q"
        if self.opt_a:
            cmd+= " -a"
        if self.opt_A:
            cmd+= " -A"
        if self.opt_Y:
            cmd+= " -Y"
        if self.opt_Q:
            cmd+= " -Q"
        cmd+= " -g"
        cmd+= " tmp.mesh"

        os.system(cmd)

        os.system("medit tmp.1.mesh")

        if self.prev:
            os.system("rm tmp.mesh tmp.1.*")
        else:
            os.system("mv tmp.1.mesh fill.mesh")
            os.system("rm tmp.mesh tmp.1.*")

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "opt_p", text="PCL")
        self.layout.prop(self, "opt_q", text="mesh refinement")
        self.layout.prop(self, "opt_a", text="maximum volume")
        self.layout.prop(self, "opt_A", text="attributes in regions")
        self.layout.prop(self, "opt_Y", text="keep surface")
        self.layout.prop(self, "opt_Q", text="quiet")
        self.layout.prop(self, "prev", text="Preview only")
        col = self.layout.column(align=True)

#register and unregister
def register():
    bpy.utils.register_class(tetgen_fill_operator)
def unregister():
    bpy.utils.unregister_class(tetgen_fill_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
