import bpy
import mathutils
import os

#Define the operator names, properties and function
operatorID   = "mesh.superpcs"
operatorText = "Runs a super4PCS alignement between two meshes"
class superPCS_operator(bpy.types.Operator):
    """runs a super4PCS"""
    bl_idname = operatorID
    bl_label = operatorText

    #maxIt = bpy.props.IntProperty(name="maxIt", description="Maximum number of iterations", default=50, min=1, max=200)
    #numPtSource = bpy.props.IntProperty(name="numPtSource", description="Approximate number of points for the source", default=5000, min=100, max=20000)
    #numPtTarget = bpy.props.IntProperty(name="numPtTarget", description="Approximate number of points for the target", default=5000, min=100, max=20000)
    #toler = bpy.props.FloatProperty(name="toler", description="Tolerance threshold", default=0.001, min=0.00001, max=0.1)
    #weigh = bpy.props.BoolProperty(name="weigh", description="Use the target weight as a segmentation region on source", default=True)

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

        bpy.ops.object.select_all(action='DESELECT')
        sourceObject.select = True
        bpy.context.scene.objects.active=sourceObject
        bpy.ops.export_scene.obj(filepath="/home/norgeot/source.obj",use_selection=True, use_materials=False)

        bpy.ops.object.select_all(action='DESELECT')
        targetObject.select = True
        bpy.context.scene.objects.active=targetObject
        bpy.ops.export_scene.obj(filepath="/home/norgeot/target.obj",use_selection=True, use_materials=False)

        os.system("super4PCS -i /home/norgeot/source.obj /home/norgeot/target.obj -d 0.2 -r /home/norgeot/output.obj")

        """
        T = icp.icp(sourceVerts, targetVerts, max_iterations=self.maxIt, tolerance=self.toler)
        sourceObject.matrix_world = mathutils.Matrix(T)
        """

        return {'FINISHED'}

    def draw(self, context):
        """
        self.layout.prop(self, "numPtSource", text="Approx pts for source")
        self.layout.prop(self, "numPtTarget", text="Approx pts for target")
        self.layout.prop(self, "maxIt", text="Max iterations")
        self.layout.prop(self, "toler", text="Tolerance")
        self.layout.prop(self, "weigh", text="Use weight paint")
        """
        col = self.layout.column(align=True)


#register and unregister
def register():
    bpy.utils.register_class(superPCS_operator)
def unregister():
    bpy.utils.unregister_class(superPCS_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
