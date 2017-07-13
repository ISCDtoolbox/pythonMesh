import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
import colorsys
from . import msh


#Define the operator names, properties and function
operatorID   = "import_mesh.mesh"
operatorText = "Import .mesh"
class operator(bpy.types.Operator, ExportHelper):
    """Import a Mesh file"""
    bl_idname = operatorID
    bl_label = operatorText
    filter_glob = StringProperty(
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

    [verts, tris, quads] = msh.readMesh(filepath)

    meshes = []
    rTris = tris[:,-1].tolist() if tris.size else []
    rQuads = quads[:,-1].tolist() if quads.size else []
    tris = [t.tolist() for t in tris]
    quads = [q.tolist() for q in quads]
    verts = [v.tolist()[:-1] for v in verts]
    REFS = set(rTris + rQuads)
    for i,r in enumerate(REFS):
        refFaces = [t[:-1] for t in tris + quads if t[-1]==r]
        #refFaces = refFaces + [[q[:-1] for q in quads if q[-1] == r]]
        mesh_name = bpy.path.display_name_from_filepath(filepath)
        mesh = bpy.data.meshes.new(name=mesh_name)
        meshes.append(mesh)
        mesh.from_pydata(verts, [], refFaces)
        mesh.validate()
        mesh.update()
    del verts, tris, quads

    if not meshes:
        return 1

    scene = context.scene

    objects = []
    for i,m in enumerate(meshes):
        obj = bpy.data.objects.new(m.name, m)
        bpy.ops.object.select_all(action='DESELECT')
        scene.objects.link(obj)
        scene.objects.active = obj
        mat = bpy.data.materials.new(m.name+"_material_"+str(i))
        if i==0:
            mat.diffuse_color = colorsys.hsv_to_rgb(0,0,1)
        else:
            mat.diffuse_color = colorsys.hsv_to_rgb(float(i/len(meshes)),1,1)
        obj.data.materials.append(mat)
        objects.append(obj)
    del meshes

    scene.update()
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select=True
    bpy.ops.object.join()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()

    return 0

#register and unregister
def register():
    bpy.utils.register_class(operator)
def unregister():
    bpy.utils.unregister_class(operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
