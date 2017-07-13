import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
import colorsys
from . import msh
from . import operator_export_mesh
import os

#Define the operator names, properties and function
operatorID   = "mesh.tetgen_hull"
operatorText = "Tetgen hull"
class tetgen_hull_operator(bpy.types.Operator):
    """Gets the convex hull of a mesh with tetgen"""
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
    root="tmp"
    bpy.ops.export_mesh.mesh(filepath=root+".mesh")
    os.system("rm " + root + ".sol")
    os.system("/home/norgeot/dev/ext/tetgen1.5.1-beta1/build/tetgen -cAzn " + root + ".mesh")
    #Extracting the hull from this file
    neigh = []
    with open(root+ ".1.neigh") as f:
        for l in f.readlines()[1:-1]:
            neigh.append( [int(l.split()[i]) for i in range(1,5)] )
    tets = []
    with open(root + ".1.ele") as f:
        for l in f.readlines()[1:-1]:
            tets.append( [int(l.split()[i]) for i in range(1,5)] )
    verts = []
    with open(root+ ".1.node") as f:
        for l in f.readlines()[1:-1]:
            verts.append( [float(l.split()[i]) for i in range(1,4)] )
    tris = []
    for i,n in enumerate(neigh):
        for j,c in enumerate(n):
            if c==-1:
                tris.append([tets[i][k] for k in range(4) if k!=j])

    mesh_name = "hull"
    mesh = bpy.data.meshes.new(name=mesh_name)
    mesh.from_pydata(verts, [], tris)
    mesh.validate()
    mesh.update()
    del verts, tris
    scene = context.scene
    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.ops.object.select_all(action='DESELECT')
    scene.objects.link(obj)
    scene.objects.active = obj
    scene.update()

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.editmode_toggle()

    os.system("rm " + root + ".*")
    return 0

#register and unregister
def register():
    bpy.utils.register_class(tetgen_hull_operator)
def unregister():
    bpy.utils.unregister_class(tetgen_hull_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
