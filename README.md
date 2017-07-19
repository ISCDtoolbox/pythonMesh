# pythonMesh [![Build Status](https://api.travis-ci.org/loicNorgeot/pythonMesh.svg)](https://travis-ci.org/loicNorgeot/pythonMesh)
A python module for manipulating .mesh files

## usage
```python
import msh
# Import, modify and save a .mesh as .vtk file
mesh = msh.Mesh("myFile.mesh")
mesh.readSol("myFile.sol")
mesh.replaceRef(2,3)
mesh.scale(0.1)
mesh.writeVTK("myFile.vtk")
```

## blender addon
Adds useful mesh manipulation options and interfaces:
* [tetgen](http://wias-berlin.de/software/tetgen/)
* [mmgTools](http://wias-berlin.de/software/tetgen/)
* [ISCDtoolbox](https://github.com/ISCDtoolbox)
* [cork boolean operations](https://github.com/gilbo/cork)
* [super4PCS](https://github.com/nmellado/Super4PCS)
* [Metis](http://glaros.dtc.umn.edu/gkhome/metis/metis/overview)
* Easy baking between high res and low resolution meshes
* Efficient local registration with the Iterative Closest Point
* Fast animation loading (from a sequence of meshes)
