import bpy
from mathutils import Color
import random
from bpy.props import *

import bmesh


bl_info = {
    "name": "Weight2VertexCol",
    "author": "Kursad Karatas",
    "version": (0, 1, 0),
    "blender": (2, 6 ,6),
    "location": "View3D > UI panel > CopyWeightColors",
    "description": "Transfers Weights as Vertex Colors",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}


class Weight2VertexCol(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.weight2vertexcol"
    bl_label = "Weight2VertexCol"
    bl_space_type = "VIEW_3D"
    bl_options = {'REGISTER', 'UNDO'}

    method=bpy.props.BoolProperty(name="Color", description="Choose the coloring method", default=False)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        transferWeight2VertexCol(context, self.method)
        context.active_object.data.update()
        return {'FINISHED'}


def transferWeight2VertexCol(context, method):
    me=context.active_object
    verts=me.data.vertices

    col=Color()
    col.h=0
    col.s=1
    col.v=1

    #vcolgrp=bpy.context.active_object.data.vertex_colors.keys()

    try:
        assert bpy.context.active_object.vertex_groups
        if not bpy.context.active_object.data.vertex_colors:
            bpy.context.active_object.data.vertex_colors.new()
        assert bpy.context.active_object.data.vertex_colors

    except AssertionError:
        bpy.ops.error.message('INVOKE_DEFAULT',
                type = "Error",
                message = 'you need at least one vertex group and one color group')
        return

    vgrp=bpy.context.active_object.vertex_groups.keys()

    vcolgrp=bpy.context.active_object.data.vertex_colors


    #Check to see if we have at least one vertex group and one vertex color group
    if len(vgrp) > 0 and len(vcolgrp) > 0:
        print ("enough parameters")
        if not method:
            for poly in me.data.polygons:
                for loop in poly.loop_indices:
                    vertindex=me.data.loops[loop].vertex_index
                    #weight=me.vertex_groups['Group'].weight(vertindex)
                    #Check to see if the vertex has any geoup association
                    try:
                        weight=me.vertex_groups.active.weight(vertindex)
                    except:
                        continue

                    col.r= (weight*-1.0)+1.0
                    col.g=col.r
                    col.b=col.r
                    me.data.vertex_colors.active.data[loop].color = (col.b, col.g, col.r)


class MessageOperator(bpy.types.Operator):
    bl_idname = "error.message"
    bl_label = "Message"
    type = StringProperty()
    message = StringProperty()

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=800, height=200)

    def draw(self, context):
        self.layout.label("A message has arrived")
        row = self.layout.split(0.25)
        row.prop(self, "type")
        row.prop(self, "message")
        row = self.layout.split(0.80)
        row.label("")
        row.operator("error.ok")

#
#   The OK button in the error dialog
#
class OkOperator(bpy.types.Operator):
    bl_idname = "error.ok"
    bl_label = "OK"
    def execute(self, context):
        return {'FINISHED'}

def menu_draw(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.operator(Bevel.bl_idname, "Weight2VertexCol")

def register():
    bpy.utils.register_class(Weight2VertexCol)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_draw)
    #error window
    bpy.utils.register_class(OkOperator)
    bpy.utils.register_class(MessageOperator)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_draw)
    bpy.utils.unregister_class(Weight2VertexCol)
