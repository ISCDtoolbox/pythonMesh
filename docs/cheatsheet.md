# Cheatsheet

## 1 - blender
1. Model and texture a HR object for visualization
2. Duplicate the HR mesh
3. Work your way to a simpler, and clean (no intersecting faces, no non-manifold edges) mesh
4. Add a computational domain if you wish to simulate flow around the object, otherwise set up the different regions if you wish to simulate flow inside.
5. Export to .mesh format

![hr](https://user-images.githubusercontent.com/11873158/28914662-d3634c98-783c-11e7-9149-38c1fe100d3a.png)

## 2 - medit
In a terminal, type:
```bash
medit /path/to/the/exported/object/myObject.mesh
```
### 2.1 - navigation
* Left click to rotate
* Right click for the menu
* Middle click to translate
* **Shift + click** to get the reference of an element
### 2.2 - options
#### display
* "C" to toggle the color
* "L" to toggle the wireframe
* "E" to toggle the material colors
* "B" to toggle between white and black background
#### clipping plane
* "F1" to toggle the clipping plane
* "F2" to toggle the clipping plane edition (Left button to rotate, middle button to translate)

![screenshot from 2017-08-03 11 17 01](https://user-images.githubusercontent.com/11873158/28914853-6d71302a-783d-11e7-8e4d-38d4ff11ee43.png)

## 3 - mmgs (optionnal)
To remesh your object with **mmgs**, type in a terminal:
```bash
mmgs_O3 /path/to/the/exported/object/myObject.mesh
```
The remeshed file will be saved as *myObject.o.mesh*.

You can check the output with:
```bash
medit /path/to/the/exported/object/myObject.o.mesh
```

## 4 - tetgen
To create a volume mesh of your object, type in a terminal:
```bash
tetgen -pgA /path/to/the/exported/object/myObject.mesh
or
tetgen -pgA /path/to/the/exported/object/myObject.o.mesh
```
The new file will have a ".1" suffix: *myObject.1.mesh* or *myObject.o.1.mesh*.

Open it in **medit** with:
```bash
medit /path/to/the/exported/object/myObject(.o).1.mesh
```

![screenshot from 2017-08-03 11 19 46](https://user-images.githubusercontent.com/11873158/28914963-cc68eaf0-783d-11e7-8a2c-d17a8a271665.png)

We will now remove the unnecessary geometry (tetrahedra *inside* your LR mesh if you used an exterior domain, and blue triangles) created by **tetgen**.

If you used a computational domain (flow outside an object), get the reference of the tetrahedra inside your object (with medit, **Shift + click** on the inside domain gives you the reference in the terminal), and execute:
```bash
python /path/to/pythonMesh/src/removeReference.py /path/to/myObject.1.mesh theReferenceOfTheInsideDomain
```
Make sure to replace *theReferenceOfTheInsideDomain* with the actual reference of the inside domain.

If you want to simulate the flow inside an object, just type:
```bash
python /path/to/pythonMesh/src/removeReference.py /path/to/myObject.1.mesh 0
```

![screenshot from 2017-08-03 11 22 03](https://user-images.githubusercontent.com/11873158/28915051-293fc6e0-783e-11e7-98ac-526e1169c137.png)

## 5 - mmg3d
The last step before running the simulation is to refine the volume mesh with **mmg3d**, which will add a ".o" suffix to your file name:
```bash
mmg3d_O3 /path/to/the/exported/object/myObject(.o).1.mesh
medit /path/to/the/exported/object/myObject(.o).1.o.mesh
```
**Tip**: Type "M" to toggle the scalar field (here the size of edges).

![screenshot from 2017-08-03 11 25 30](https://user-images.githubusercontent.com/11873158/28915198-a858d606-783e-11e7-86b7-a38859882d14.png)

## 5 - DEFAULT.nstokes
Create a new file called **DEFAULT.nstokes** in the same directory that **myObject.mesh**, which will control the simulation parameter.
```bash
Dirichlet
4 # 4 different regions
1 triangle v 0. 0. 0. 
7 triangle v 0. 0. 0.
5 triangle v 0. 1. 0.
8 triangle v 0. 0. 0.
# the format for each region is:
# $referenceId triangle v $xVelocity $yVelocity $zVelocity
# Do not write a line for your outlet(s) region(s)

Domain
1 # 1 volume domain
1 1. 1. # ref 1, nu=1., rho=1.
```
**Shift + Left click** in **medit** to get a face reference.

## 6 - nstokes
Let's run the simulation:

Type in a terminal (replace 0.01 with lower values to get better results, at the cost of computation time):
```bash
nstokes -r 0.01 /path/to/the/exported/object/myObject(.o).1.o.mesh
```
After a while, the computation should be finished (depending on the size of your mesh). Open the file in medit:
```bash
medit /path/to/the/exported/object/myObject(.o).1.o.mesh
```
You should now see the velocity value:

![screenshot from 2017-08-03 11 34 42](https://user-images.githubusercontent.com/11873158/28915566-d45dd1c4-783f-11e7-98c0-454f51570177.png)

## 7 - Paraview
Let's convert this file to **Paraview** .vtk format:
```bash
python /path/to/pythonMesh/src/convertToParaview.py /path/to/myObject.1.d.o.mesh
```
Open Paraview, load the newly created file (.vtk extension), and click on apply in the properties panel:

![screenshot from 2017-08-03 11 42 32](https://user-images.githubusercontent.com/11873158/28916434-7c6954b8-7842-11e7-8304-bfdafc54d6ed.png)

You can now add some filters (Filters menu -> search ) in order to create the appropriate visualization. 

For instance: 
* *StreamTracer* filter (change the radius, which defaults to 0, and the point source location)
* *Tube*
* Coloring set to "Velocity"
* Don't forget to hit apply after every modification!


![screenshot from 2017-08-03 11 52 36](https://user-images.githubusercontent.com/11873158/28916396-5f876678-7842-11e7-8cfa-90d2074b4165.png)

Hide every object you don't want to import back to blender, and export the scene to .x3d format.

## 8 - blender
In blender, import your .x3d file, and delete the unwanted lamps and cameras.

Making sure that the rotation pivot point is at the center of the scene, rotate the imported object by 90° around the X axis, then by 180° around the Z axis:

Make sure that the imported object has a material, and that the "Vertex color paint" is checked in the material menu, in the "Options" panel.

![screenshot from 2017-08-03 12 06 46](https://user-images.githubusercontent.com/11873158/28916977-474c15ac-7844-11e7-9f20-c6200f3555fa.png)

Voila!

