import msh

if __name__=="__main__":
    mesh = msh.Mesh("demo/Theatre.mesh")
    mesh.readSol()
    mesh.caracterize()
    mesh.writeXYZ("demo/Theatre.xyz")
    mesh.writeSTL("demo/Theatre.stl")
    mesh.writeOBJ("demo/Theatre.obj")
    mesh.writeVTK("demo/Theatre.vtk")
