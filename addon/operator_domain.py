import bpy
import mathutils
import bmesh
import numpy as np


#Define the operator names, properties and function
operatorID   = "mesh.adddomain"
operatorText = "Adds a computation domain to the object"
class domain_operator(bpy.types.Operator):
    """Creates a computation domain"""
    bl_idname = operatorID
    bl_label = operatorText

    flowAxis = bpy.props.EnumProperty(items=[ ("xp","xp","minus X to plus X"),  ("xm","xm","plus X to minus X"), ("yp","yp","minus Y to plus Y"), ("ym","ym","plus Y to minus Y"), ("zp","zp","minus Z to plus Z"), ("zm","zm","plus Z to minus Z") ],
    name="flowAxis", description="Axis of the flow for a fluid simulation (side boundaries)", default="yp")
    scaleX = bpy.props.FloatProperty(name="scaleX", description="scale X", default=1.2, min=1.1, max=10)
    scaleY = bpy.props.FloatProperty(name="scaleY", description="scale X", default=2, min=1.1, max=10)
    scaleZ = bpy.props.FloatProperty(name="scaleZ", description="scale X", default=1.2, min=1.1, max=10)
    differentBottom = bpy.props.BoolProperty(name="differentBottom", description="Use a different reference for the bottom boundary", default=False)
    merge = bpy.props.BoolProperty(name="merge", description="Merge with the original object", default=False)

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and context.active_object.type == 'MESH' and len(context.selected_objects)==1)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        #Get bounding box info
        active = bpy.context.scene.objects.active
        loca = active.location
        dims = active.dimensions
        bbox = active.bound_box
        matr = active.matrix_world
        corners = [matr*mathutils.Vector(x) for x in bbox]
        min = np.min(corners, axis=0)
        max = np.max(corners, axis=0)
        mean = (max + min)/2.

        #Add a cube around the mesh
        bpy.ops.mesh.primitive_cube_add(location=mean)
        domain = bpy.context.scene.objects.active
        domain.dimensions = max-min
        domain.scale[0] = domain.scale[0]*self.scaleX
        domain.scale[1] = domain.scale[1]*self.scaleY
        domain.scale[2] = domain.scale[2]*self.scaleZ

        #Prepare the references materials
        names = ["inlet", "outlet", "boundaries"]
        colors = [(0,1,0), (1,0,0), (0,0,1)]
        refs = []
        if self.flowAxis == "xp":
            refs = [ [0], [2], [1,3,5] ]
        if self.flowAxis == "xm":
            refs = [ [2], [0], [1,3,5] ]
        if self.flowAxis == "yp":
            refs = [ [3], [1], [0,2,5] ]
        if self.flowAxis == "ym":
            refs = [ [1], [3], [0,2,5] ]
        if self.flowAxis == "zp":
            refs = [ [4], [5], [0,1,2,3] ]
        if self.flowAxis == "zm":
            refs = [ [5], [4], [0,1,2,3] ]
        if self.differentBottom and self.flowAxis!=4 and self.flowAxis!=5:
            names.append("bottom")
            colors.append( (1,1,0) )
            refs.append([4])
        if not self.differentBottom:
            refs[-1].append(4)

        #Get the mesh info and into edit mode
        bpy.ops.object.editmode_toggle()
        mesh = bmesh.from_edit_mesh(domain.data)
        for i,r in enumerate(refs):
            #Create a new material
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.context.object.active_material_index = i
            mat = bpy.data.materials.new(name=names[i])
            domain.data.materials.append(mat)
            mat.diffuse_color = colors[i]
            for j,f in enumerate(mesh.faces):
                if j in r:
                    f.select = True
            bpy.ops.object.material_slot_assign()
        bpy.ops.object.editmode_toggle()

        #Subdivide the cube
        bpy.ops.object.modifier_add(type='SUBSURF')
        domain.modifiers["Subsurf"].subdivision_type = 'SIMPLE'
        domain.modifiers["Subsurf"].levels = 3
        domain.modifiers["Subsurf"].render_levels = 3
        bpy.ops.object.modifier_apply(modifier="Subsurf")

        if self.merge:
            #Join with the mesh
            active.select = True
            domain.select = True
            bpy.context.scene.objects.active = active
            for mod in active.modifiers:
                bpy.ops.object.modifier_apply(modifier = mod.name)
            nbMat = len(active.data.materials)
            bpy.ops.object.join()

        #Print the default.nstokes file
        nstokes = ""
        materials = bpy.context.scene.objects.active.data.materials
        dirichlet, slip = [],[]
        for i,m in enumerate(materials):
            #Inlet material = Dirichlet with non null speed
            if "inlet" in m.name:
                if self.flowAxis == "xp":
                    speed = "1. 0. 0."
                if self.flowAxis == "xm":
                    speed = "-1. 0. 0."
                if self.flowAxis == "yp":
                    speed = "0. 1. 0."
                if self.flowAxis == "ym":
                    speed = "0. -1. 0."
                if self.flowAxis == "zp":
                    speed = "0. 0. 1."
                if self.flowAxis == "zm":
                    speed = "0. 0. -1."
                dirichlet.append([i+1, speed])
            #Outlet material = pass
            elif "outlet" in m.name:
                pass
            #Boundary materials = slip condition
            elif "bounaries" in m.name:
                dirichlet.append([i+1, "0. 0. 0."])
            #Bottom = dirichlet with null value
            elif "bottom" in m.name:
                dirichlet.append([i+1, "0. 0. 0."])
            #Original object = dirichlet with null value
            else:
                dirichlet.append([i+1, "0. 0. 0."])

        #Writing the file
        if len(dirichlet):
            nstokes += "Dirichlet\n"+str(len(dirichlet))+"\n"
            for d in dirichlet:
                nstokes += str(d[0]) + " triangle v " + d[1] + "\n"
            nstokes+="\n"
        if len(slip):
            nstokes += "Slip\n"+str(len(slip))+"\n"
            for s in slip:
                nstokes += str(s[0]) + " triangle v " + s[1] + "\n"
            nstokes+="\n"
        nstokes+="Gravity\n0. 0. -0.1\n\n"
        nstokes+="Domain\n1 1. 1."
        print(nstokes)

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "flowAxis", text="Main axis of th fluid flow")
        self.layout.prop(self, "scaleX", text="X scale for the domain")
        self.layout.prop(self, "scaleY", text="Y scale for the domain")
        self.layout.prop(self, "scaleZ", text="Z scale for the domain")
        self.layout.prop(self, "merge", text="Merge the object and the domain")
        self.layout.prop(self, "differentBottom", text="Different ref for the bottom")
        col = self.layout.column(align=True)


#register and unregister
def register():
    bpy.utils.register_class(domain_operator)
def unregister():
    bpy.utils.unregister_class(domain_operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
