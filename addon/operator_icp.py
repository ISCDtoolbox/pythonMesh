import bpy
import mathutils
from . import icp
import numpy as np


#Define the operator names, properties and function
operatorID   = "mesh.icp"
operatorText = "Runs an ICP between two meshes"
class icp_operator(bpy.types.Operator):
    """Export a Mesh file"""
    bl_idname = operatorID
    bl_label = operatorText

    maxIt = bpy.props.IntProperty(name="maxIt", description="Maximum number of iterations", default=50, min=1, max=200)
    numPtSource = bpy.props.IntProperty(name="numPtSource", description="Approximate number of points for the source", default=5000, min=100, max=20000)
    numPtTarget = bpy.props.IntProperty(name="numPtTarget", description="Approximate number of points for the target", default=5000, min=100, max=20000)
    toler = bpy.props.FloatProperty(name="toler", description="Tolerance threshold", default=0.001, min=0.00001, max=0.1)
    weigh = bpy.props.BoolProperty(name="weigh", description="Use the target weight as a segmentation region on source", default=True)

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

        bpy.context.scene.objects.active=sourceObject
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
        source = sourceObject.to_mesh(context.scene, True, 'PREVIEW')
        sourceMat = sourceObject.matrix_world
        sourceVerts = [[x for x in sourceMat*v.co] for v in source.vertices[:]]
        step1 = int(len(sourceVerts)/self.numPtSource) + 1

        vgrp = sourceObject.vertex_groups.keys()
        if(len(vgrp)>0 and self.weigh):
            GROUP = sourceObject.vertex_groups.active
            cols = [0.0] * len(sourceVerts)
            for i,t in enumerate(source.polygons):
                for j,v in enumerate(t.vertices):
                    try:
                        cols[v] = float(GROUP.weight(v))
                    except:
                        continue
            sourceVerts = [v for v,c in zip(sourceVerts,cols) if c>0.5]

        sourceVerts = sourceVerts[::step1]


        bpy.context.scene.objects.active=targetObject
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
        target = targetObject.to_mesh(context.scene, True, 'PREVIEW')
        targetMat = targetObject.matrix_world
        targetVerts = np.array([[x for x in targetMat*v.co] for v in target.vertices])
        step2 = int(len(targetVerts)/self.numPtTarget) + 1
        targetVerts = targetVerts[::step2]

        T = icp.icp(sourceVerts, targetVerts, max_iterations=self.maxIt, tolerance=self.toler)
        sourceObject.matrix_world = mathutils.Matrix(T)

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "numPtSource", text="Approx pts for source")
        self.layout.prop(self, "numPtTarget", text="Approx pts for target")
        self.layout.prop(self, "maxIt", text="Max iterations")
        self.layout.prop(self, "toler", text="Tolerance")
        self.layout.prop(self, "weigh", text="Use weight paint")
        col = self.layout.column(align=True)


#register and unregister
def register():
    bpy.utils.register_class(icp_operator)
def unregister():
    bpy.utils.unregister_class(icp_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
