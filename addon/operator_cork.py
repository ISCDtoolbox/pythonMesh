import bpy

C = bpy.context
D = bpy.data

#Define the operator names, properties and function
operatorID   = "mesh.cork"
operatorText = "Cork boolean operations"

class cork_operator(bpy.types.Operator):
    """Applies existing boolean with the cork suite"""
    bl_idname = operatorID
    bl_label = operatorText

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and context.active_object.type == 'MESH' and len(context.selected_objects)==1)

    #def invoke(self, context, event):
    #    return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        OBJ = bpy.context.scene.objects.active
        cork = "/home/norgeot/dev/ext/cork/bin/cork"

        basis_file = "bool_" + OBJ.name + ".off"

        objects = []
        operations = []
        commands = []

        #Export the basis mesh
        #Get boolean information
        for m in OBJ.modifiers:
            if m.type == 'BOOLEAN':
                m.show_viewport = False
        bpy.ops.object.modifier_add(type="TRIANGULATE")
        m = OBJ.modifiers[-1]
        m.quad_method = 'BEAUTY'
        m.ngon_method = 'BEAUTY'
        bpy.ops.export_mesh.off(filepath=basis_file)
        bpy.ops.object.modifier_remove(modifier=m.name)

        #Get boolean information
        for m in OBJ.modifiers:
            if m.type == 'BOOLEAN':

                bool_file = "bool_" + m.object.name + ".off"
                m.show_viewport = True

                OPE = None
                if m.operation == "INTERSECT":
                    OPE = " -isct "
                if m.operation == "UNION":
                    OPE = " -union "
                if m.operation == "DIFFERENCE":
                    OPE = " -diff "
                commands.append(cork + OPE + basis_file + " " + bool_file + " " + basis_file)
                commands.append("echo 'Finished " + m.operation + " with " + m.object.name + "'")

                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = m.object
                m.object.select = True

                m.object.hide=False
                bpy.ops.object.modifier_add(type="TRIANGULATE")
                tri = bpy.context.scene.objects.active.modifiers[-1]
                tri.quad_method = 'BEAUTY'
                tri.ngon_method = 'BEAUTY'
                bpy.ops.export_mesh.off(filepath=bool_file)
                bpy.ops.object.modifier_remove(modifier=tri.name)
                m.object.hide = True


        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = OBJ

        with open("bool_script.sh", "w") as f:
            for c in commands:
                f.write(c + "\n")

        print("The cork files should be available in the current directory\nlaunch sh bool_script.sh to obtain the final .off file")

        return {'FINISHED'}


#register and unregister
def register():
    bpy.utils.register_class(cork_operator)
def unregister():
    bpy.utils.unregister_class(cork_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
