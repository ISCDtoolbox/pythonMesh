import msh
import sys
# Import, modify and save a .mesh as .vtk file

if __name__=="__main__":
    if len(sys.argv)!=2:
        print("The script takes a .mesh file as only argument!")
        sys.exit()
    mesh = msh.Mesh(sys.argv[1])
    mesh.readSol()
    mesh.writeVTK(sys.argv[1][:-4] + "vtk")
    print("Paraview file written to " + sys.argv[1][:-4] + "vtk")
