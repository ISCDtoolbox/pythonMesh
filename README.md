# pythonMesh [![Build Status](https://travis-ci.org/ISCDtoolbox/pythonMesh.svg?branch=master)](https://travis-ci.org/ISCDtoolbox/pythonMesh)
A python module for manipulating .mesh files

## ISCD summer school
Please, refer to the [Related page](docs/summerschool.md)

## python example
```python
import msh
# Import, modify and save a .mesh as .vtk file
mesh = msh.Mesh("myFile.mesh")
mesh.readSol("myFile.sol")
mesh.replaceRef(2,3)
mesh.scale(0.1)
mesh.writeVTK("myFile.vtk")
```

## external tools
Adds useful mesh manipulation options and interfaces:
* [tetgen](http://wias-berlin.de/software/tetgen/)
* [mmgTools](https://www.mmgtools.org/)
* [ISCDtoolbox](https://github.com/ISCDtoolbox)
* [cork boolean operations](https://github.com/gilbo/cork)
* [super4PCS](https://github.com/nmellado/Super4PCS)
* [Metis](http://glaros.dtc.umn.edu/gkhome/metis/metis/overview)
* Easy baking between high res and low resolution meshes
* Efficient local registration with the Iterative Closest Point
* Fast animation loading (from a sequence of meshes)
