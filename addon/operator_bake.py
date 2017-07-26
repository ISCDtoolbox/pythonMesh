import bpy
import mathutils
import numpy as np

#Define the operator names, properties and function
operatorID   = "mesh.bake"
operatorText = "Bakes a HR mesh (AO, textures and normals) to a LR one"

class bake_operator(bpy.types.Operator):
    """Export a Mesh file"""
    bl_idname = operatorID
    bl_label = operatorText

    imgRes  = bpy.props.IntProperty(name="texture resolution", description="target resolution", default=1024, min=128, max=8192)
    bakeTEX = bpy.props.BoolProperty(name="bakeTEX", description="bake the texture", default=True)
    bakeNOR = bpy.props.BoolProperty(name="bakeNOR", description="bake the normals", default=True)
    bakeAO  = bpy.props.BoolProperty(name="bakeAO",  description="bake the ambient occlusion", default=False)
    bakeVC  = bpy.props.BoolProperty(name="bakeVC",  description="bake the vertex colors", default=False)
    bakeSHD = bpy.props.BoolProperty(name="bakeSHD", description="bake shadows", default=False)
    saveIm  = bpy.props.BoolProperty(name="saveIm",  description="save the images", default=False)

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and context.active_object.type == 'MESH' and len(context.selected_objects)==2)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        #Identify the different objects
        sourceObject,targetObject = None, None
        sourceVerts, targetVerts = None, None
        for obj in context.selected_objects:
            if context.active_object == obj:
                targetObject = obj
            else:
                sourceObject = obj
        #Prepare the target object
        if not targetObject.data.uv_layers:
            bpy.ops.uv.smart_project()
        for i in range(len(targetObject.material_slots)):
            bpy.ops.object.material_slot_remove({'object': targetObject})
        #Add an empty material
        mat = bpy.data.materials.new('default')
        targetObject.data.materials.append(mat)

        #For blender render:
        render = bpy.context.scene.render.engine
        names = ['TEXTURE', 'NORMALS', 'AO', 'VERTEX_COLORS', 'SHADOWS']
        bake  = [self.bakeTEX, self.bakeNOR, self.bakeAO, self.bakeVC, self.bakeSHD]
        if render == "CYCLES":
            names = ['DIFFUSE', 'NORMAL', 'AO', 'VERTEX_COLORS', 'SHADOWS']
            bake  = [self.bakeTEX, self.bakeNOR, self.bakeAO, self.bakeVC, self.bakeSHD]

        for i,n in enumerate(names):
            if bake[i]:
                tex = bpy.data.textures.new( 'texture_'+n, type = 'IMAGE')
                img = bpy.data.images.new("image_"+n, width=self.imgRes, height=self.imgRes)
                img.file_format='PNG'
                tex.image = img

                if render == "BLENDER_RENDER":
                    mtex = mat.texture_slots.add()
                    mtex.texture = tex
                    mtex.texture_coords = 'UV'

                if render == "BLENDER_RENDER":
                    bpy.context.scene.render.use_bake_selected_to_active = True

                bpy.ops.object.editmode_toggle()
                bpy.data.screens['UV Editing'].areas[1].spaces[0].image = img

                if render == "BLENDER_RENDER":
                    bpy.context.object.active_material.use_textures[i] = False
                if render == "CYCLES":
                    mat.use_nodes = True
                    node = mat.node_tree.nodes.new("ShaderNodeTexImage")
                    node.select = True
                    mat.node_tree.nodes.active = node
                    node.image = img

                #bpy.context.space_data.context = 'RENDER'
                if render == "BLENDER_RENDER":
                    bpy.context.scene.render.bake_type = n
                elif render == "CYCLES":
                    bpy.context.scene.cycles.bake_type = n

                if n == "AO":
                    bpy.context.scene.render.use_bake_normalize = True

                if render == "CYCLES":
                    bpy.ops.object.bake(type=n, pass_filter=set({'COLOR'}), filepath="", margin=32, use_selected_to_active=True, save_mode='INTERNAL')
                else:
                    bpy.ops.object.bake_image()

                img.filepath_raw = "bake_"+n+".png"
                if self.saveIm:
                    img.save()

                bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "imgRes", text="target resolution")
        self.layout.prop(self, "bakeTEX", text="bake color")
        self.layout.prop(self, "bakeAO", text="bake ambient occlusion")
        self.layout.prop(self, "bakeNOR", text="bake normals")
        self.layout.prop(self, "bakeVC", text="bake vertex colors")
        self.layout.prop(self, "bakeSHD", text="bake shadows")
        self.layout.prop(self, "saveIm", text="save images")
        col = self.layout.column(align=True)

#register and unregister
def register():
    bpy.utils.register_class(bake_operator)
def unregister():
    bpy.utils.unregister_class(bake_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
