import msh
import sys
# Import, modify and save a .mesh as .vtk file

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("The script takes a .mesh file as first argument, and the reference of the domain you wish to suppress as second argument ")
        sys.exit()
    mesh = msh.Mesh(sys.argv[1])
    mesh.removeRef(int(sys.argv[2]), keepTris=True)
    mesh.removeRef(0)
    mesh.discardUnused()
    mesh.write(sys.argv[1][:-4] + "d.mesh")
    print("Cleaned file written to " + sys.argv[1][:-4] + "d.mesh")
