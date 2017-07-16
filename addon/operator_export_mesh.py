import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
import colorsys
from . import msh


#Define the operator names, properties and function
operatorID   = "export_mesh.mesh"
operatorText = "Export .mesh"
class export_mesh_operator(bpy.types.Operator, ExportHelper):
    """Export a Mesh file"""
    bl_idname = operatorID
    bl_label = operatorText
    filter_glob = StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
    )
    check_extension = True
    filename_ext = ".mesh"

    refAtVerts = bpy.props.BoolProperty(name="refAtVerts", description="reference at vertices", default=False)
    triangulate = bpy.props.BoolProperty(name="triangulate", description="triangulate the mesh", default=True)

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and context.active_object.type == 'MESH' and len(context.selected_objects)==1)


    def execute(self, context):
        keywords = self.as_keywords(ignore=('filter_glob','check_existing'))
        print(keywords)
        err = operatorFunction(self, context, **keywords)
        if err:
            return {'CANCELLED'}
        else:
            return {'FINISHED'}

def operatorFunction(operator, context, filepath, refAtVerts):
    #Get the selected object
    APPLY_MODIFIERS = True
    scene = context.scene
    bpy.ops.object.duplicate()
    obj = scene.objects.active

    #Convert the big n-gons in triangles if necessary
    bpy.context.tool_settings.mesh_select_mode=(False,False,True)
    bpy.ops.object.convert(target='MESH')

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    if triangulate:
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_face_by_sides(number=3, type='GREATER')
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.editmode_toggle()

    mesh = obj.to_mesh(scene, APPLY_MODIFIERS, 'PREVIEW')
    mesh.transform(obj.matrix_world)

    #Get the info
    verts = [[v.co[0], v.co[1], v.co[2], 0] for v in mesh.vertices[:]]
    triangles = [ [v for v in f.vertices] + [f.material_index + 1] for f in mesh.polygons if len(f.vertices) == 3 ]
    quads = [ [v for v in f.vertices] + [f.material_index + 1]  for f in mesh.polygons if len(f.vertices) == 4 ]

    if refAtVerts:
        for i in range(len(obj.data.materials[:])):
            for f in mesh.polygons:
                if f.material_index == i:
                    for v in f.vertices:
                        verts[v][3] = f.material_index + 1

    exportMesh = msh.Mesh()
    exportMesh.verts = msh.np.array(verts)
    exportMesh.tris  = msh.np.array(triangles)
    exportMesh.quads = msh.np.array(quads)
    exportMesh.write(filepath)

    #Solutions according to the weight paint mode (0 to 1 by default)
    vgrp = bpy.context.active_object.vertex_groups.keys()
    if(len(vgrp)>0):
        GROUP = bpy.context.active_object.vertex_groups.active
        cols = [0.0] * len(verts)
        for i,t in enumerate(mesh.polygons):
            for j,v in enumerate(t.vertices):
                try:
                    cols[v] = float(GROUP.weight(v))
                except:
                    continue
        exportMesh.scalars = msh.np.array(cols)
        exportMesh.writeSol(filepath[:-5] + ".sol")

    bpy.ops.object.delete()
    bpy.data.meshes.remove(mesh)
    del exportMesh

    return {'FINISHED'}

#register and unregister
def register():
    bpy.utils.register_class(export_mesh_operator)
def unregister():
    bpy.utils.unregister_class(export_mesh_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()









"""
import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
from . import msh

class ExportMESH(bpy.types.Operator, ExportHelper):
    bl_idname = "export_mesh.mesh"
    bl_label = "Export Mesh file"
    filter_glob = StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
    )
    check_extension = True
    filename_ext = ".mesh"

    def execute(self, context):
        keywords = self.as_keywords(ignore=('filter_glob','check_existing'))
        return save(self, context, **keywords)


def menu_func_export(self, context):
    self.layout.operator(ExportMESH.bl_idname, text="Mesh format (.mesh)")

def register():
    bpy.utils.register_class(ExportMESH)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportMESH)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

def save(operator, context, filepath):
    #Get the selected object
    APPLY_MODIFIERS = True
    scene = context.scene
    bpy.ops.object.duplicate()
    obj = scene.objects.active

    #Convert the big n-gons in triangles if necessary
    bpy.context.tool_settings.mesh_select_mode=(False,False,True)
    bpy.ops.object.convert(target='MESH')

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.editmode_toggle()

    mesh = obj.to_mesh(scene, APPLY_MODIFIERS, 'PREVIEW')
    mesh.transform(obj.matrix_world)

    #Get the info
    verts = [[v.co[0], v.co[1], v.co[2], 0] for v in mesh.vertices[:]]
    triangles = [ [v for v in f.vertices] + [f.material_index + 1] for f in mesh.polygons if len(f.vertices) == 3 ]
    quads = [ [v for v in f.vertices] + [f.material_index + 1]  for f in mesh.polygons if len(f.vertices) == 4 ]

    #Open and write the .mesh file
    msh.writeMesh(filepath, verts, triangles, quads)

    #Solutions according to the weight paint mode (0 to 1 by default)
    vgrp = bpy.context.active_object.vertex_groups.keys()
    if(len(vgrp)>0):
        GROUP = bpy.context.active_object.vertex_groups.active
        cols = [0.0] * len(verts)
        for i,t in enumerate(mesh.polygons):
            for j,v in enumerate(t.vertices):
                try:
                    cols[v] = float(GROUP.weight(v))
                except:
                    continue
        msh.writeSol(filepath[:-5] + ".sol",cols)

    bpy.ops.object.delete()
    bpy.data.meshes.remove(mesh)

    return {'FINISHED'}

if __name__ == "__main__":
    register()
"""
