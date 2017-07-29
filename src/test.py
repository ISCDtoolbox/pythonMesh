import msh

if __name__=="__main__":
    #Read the geometry .mesh file (triangles and tetrahedra)
    mesh = msh.Mesh("demo/Theatre.mesh")

    #Read the .sol file for associated solution fields
    mesh.readSol()

    #Prints the info about the mesh
    mesh.caracterize()

    #Exports the mesh in different formats
    mesh.verts+=[100.,100.,100.,0]
    mesh.writeXYZ("demo/Theatre.xyz")
    mesh.writeSTL("demo/Theatre.stl")
    mesh.writeOBJ("demo/Theatre.obj")
    mesh.writeVTK("demo/Theatre.vtk")
