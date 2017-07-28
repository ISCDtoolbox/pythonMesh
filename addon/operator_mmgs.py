import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
import colorsys
from . import msh
from . import operator_export_mesh
import os

#Define the operator names, properties and function
operatorID   = "mesh.mmgs"
operatorText = "MMGS remesh"
class mmgs_operator(bpy.types.Operator):
    """Remeshes a mesh with mmgs"""
    bl_idname = operatorID
    bl_label = operatorText

    hmin = bpy.props.FloatProperty(name="hmin",  description="Minimal edge length ratio", default=0.001, min=0.00001, max=0.1)
    hmax = bpy.props.FloatProperty(name="hmax",  description="Maximal edge length ratio", default=0.1, min=0.01, max=1)
    haus = bpy.props.FloatProperty(name="hausd", description="Haussdorf distance ratio", default=0.01, min=0.00001, max=0.1)
    hgra = bpy.props.FloatProperty(name="hgrad", description="Gradation", default=1.08, min=1, max=5)
    nr   = bpy.props.BoolProperty(name="nr", description="normal regulation", default=True)
    ar   = bpy.props.BoolProperty(name="ar", description="angle regulation", default=False)
    prev = bpy.props.BoolProperty(name="preview", description="preview only", default=True)
    sol  = bpy.props.BoolProperty(name="solution", description="use weight paint for metrics", default=False)

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

        bpy.context.scene["mmgsMini"] = self.hmin*maxDim
        bpy.context.scene["mmgsMaxi"] = self.hmax*maxDim
        bpy.ops.export_mesh.mesh(filepath="tmp.mesh")
        bpy.context.scene.objects.active = obj

        if not hasTriangulate:
            bpy.ops.object.modifier_remove(modifier="Triangulate")

        if not self.sol:
            os.system("rm tmp.sol")
        cmd = "mmgs_O3 tmp.mesh -o tmp.o.mesh"
        cmd+= " -hmin " + str(self.hmin*maxDim)
        cmd+= " -hmax " + str(self.hmax*maxDim)
        cmd+= " -hausd " + str(self.haus*maxDim)
        cmd+= " -hgrad " + str(self.hgra)
        if self.nr:
            cmd+=" -nr"
        if self.ar:
            cmd+=" -ar 1"

        os.system(cmd)

        os.system("medit tmp.o.mesh")

        if not self.prev:
            bpy.ops.import_mesh.mesh(filepath="tmp.o.mesh")

        os.system("rm tmp.o.mesh tmp.o.sol")

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "hmin", text="hmin")
        self.layout.prop(self, "hmax", text="hmax")
        self.layout.prop(self, "haus", text="hausd")
        self.layout.prop(self, "hgra", text="hgrad")
        self.layout.prop(self, "nr", text="nr")
        self.layout.prop(self, "ar", text="ar")
        self.layout.prop(self, "sol", text="Use solution")
        self.layout.prop(self, "prev", text="Preview only")
        col = self.layout.column(align=True)
        col.label("Pick a material above, or click outside")
        col.label("of this dialog box to cancel.")

#register and unregister
def register():
    bpy.utils.register_class(mmgs_operator)
def unregister():
    bpy.utils.unregister_class(mmgs_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
