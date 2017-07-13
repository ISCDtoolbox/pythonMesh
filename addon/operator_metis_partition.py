import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
import colorsys
from . import msh
from . import operator_export_mesh
import os

#Define the operator names, properties and function
operatorID   = "mesh.metis_partition"
operatorText = "Metis partition"
class metis_partition_operator(bpy.types.Operator):
    """Partition a mesh with metis"""
    bl_idname = operatorID
    bl_label = operatorText
    nPar = bpy.props.IntProperty(name="n partitions",  description="Number of partitions", default=5, min=2, max=50)
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and context.active_object.type == 'MESH' and len(context.selected_objects)==1)
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    def execute(self, context):
        err = operatorFunction(self, context, self.nPar)
        if err:
            return {'CANCELLED'}
        else:
            return {'FINISHED'}
    def draw(self, context):
        self.layout.prop(self, "nPar", text="n partitions")
        col = self.layout.column(align=True)
        col.label("Pick a material above, or click outside")
        col.label("of this dialog box to cancel.")
def operatorFunction(operator, context, nPar):
    root="tmp"
    obj = bpy.context.scene.objects.active
    partition(obj,nPar)
    return 0

def partition(object, nb):
    #Metis file writing
    mesh = object.to_mesh(bpy.context.scene, apply_modifiers=True, settings='PREVIEW')
    triangles = mesh.polygons
    with open(os.path.join("tmp.txt"),"w") as f:
        f.write( str(len(triangles)) + " 1\n")
        for t in triangles:
            for v in t.vertices:
                f.write(str(v+1))
                f.write(" ")
            f.write('\n')
    #Partitionning
    os.system("mpmetis " + "tmp.txt" + " " + str(nb))
    #Reading the results
    with open("tmp.txt.epart." + str(nb)) as f:
        partition = [int(line) for line in f]
        #Write the .mesh file
        with open("tmp.mesh","w") as f:
            f.write("MeshVersionFormatted 2\nDimension 3\n")
            f.write("Vertices\n" + str(len(mesh.vertices)) + "\n")
            for v in mesh.vertices:
                f.write(str(v.co[0]) + " " + str(v.co[1]) + " " + str(v.co[2]) + " " + str(0) + "\n")
            f.write("Triangles\n" + str(len(triangles)) + "\n")
            for i,t in enumerate(triangles):
                for v in t.vertices:
                    f.write(str(v+1))
                    f.write(" ")
                f.write(str(partition[i]))
                f.write('\n')
    #Import the new mesh
    #bpy.ops.object.select_all(action='DESELECT')
    #object.select = True
    #bpy.ops.object.delete()

    bpy.ops.import_mesh.mesh(filepath="tmp.mesh")

#register and unregister
def register():
    bpy.utils.register_class(metis_partition_operator)
def unregister():
    bpy.utils.unregister_class(metis_partition_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
