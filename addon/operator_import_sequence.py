import bpy
from . import msh
from . import operator_import_mesh
from bpy_extras.io_utils import ExportHelper
import os
import re

#Functions to sort nicely
def tryint(s):
    try:
        return int(s)
    except:
        return s
def alphanum_key(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]
def sort_nicely(l):
    l.sort(key=alphanum_key)

#Define the operator names, properties and function
operatorID   = "import_mesh.sequence"
operatorText = "Morphing sequence"

class sequence_operator(bpy.types.Operator, ExportHelper):
    """Imports a morphing sequence"""
    bl_idname = operatorID
    bl_label = operatorText

    filter_glob = bpy.props.StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
    )
    check_extension = True
    filename_ext = ".mesh"

    def execute(self, context):
        keywords = self.as_keywords(ignore=('filter_glob','check_existing'))
        err = operatorFunction(self, context, **keywords)
        if err:
            return {'CANCELLED'}
        else:
            return {'FINISHED'}

def operatorFunction(operator, context, filepath):
    print(filepath)
    [verts, tris, quads] = msh.readMesh(filepath)

    tris = [t.tolist()[:-1] for t in tris]
    verts = [t.tolist()[:-1] for t in verts]

    mesh_name = "basis"
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

    path = "/".join(filepath.split("/")[:-1])
    root = (filepath.split("/")[-1]).split(".")[0]

    files = [f for f in os.listdir(path) if ".mesh" in f and root in f]
    sort_nicely(files)

    for f in files[1:]:
        print(f)
        [verts, tris, quads] = msh.readMesh(path + "/" + f)
        tris = [t.tolist()[:-1] for t in tris]
        verts = [t.tolist()[:-1] for t in verts]
        for basis in bpy.context.scene.objects:
            basis.select=True
            if basis.type == "MESH":
                shapeKey = basis.shape_key_add(from_mix=False)
                shapeKey.name = "1"
                for vert, newV in zip(basis.data.vertices, verts):
                    shapeKey.data[vert.index].co = newV
            basis.select=False

    for basis in bpy.context.scene.objects:
        if basis.type == "MESH":
            nb = len(files)
            scene = bpy.context.scene
            scene.frame_start = 1
            scene.frame_end   = 1 + nb * 3

            for i in range(nb):
                for j,key in enumerate(basis.data.shape_keys.key_blocks):
                    if i == j:
                        key.value = 1
                    else:
                        key.value = 0
                    key.keyframe_insert("value", frame=1 + 3*i)

    return 0



#register and unregister
def register():
    bpy.utils.register_class(sequence_operator)
def unregister():
    bpy.utils.unregister_class(sequence_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
