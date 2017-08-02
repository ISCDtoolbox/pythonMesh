# Fluid outside an object

## 1 - Preparation in Blender

### HR mesh
![alt text](https://user-images.githubusercontent.com/11873158/28868549-15f6c2ba-777a-11e7-8473-676d720e807d.png)

### Checking LR mesh with 3D print toolbox
Using check all to compute the quality, and clicking on intersect faces and non manifold to get the intersections and holes
![alt text](https://user-images.githubusercontent.com/11873158/28868590-3b803cb4-777a-11e7-82bd-52b6e47a1cfa.png)

### Closing the model
With the "F" shortcut, after selecting loops with Shift + Alt + Right click for instance
![alt text](https://user-images.githubusercontent.com/11873158/28868654-6c84d568-777a-11e7-9585-9dac566a355d.png)

### Adding a computational domain
![](https://user-images.githubusercontent.com/11873158/28868916-3e62e2aa-777b-11e7-90d1-59abb773cdd5.png)

![](https://user-images.githubusercontent.com/11873158/28868913-3e600cce-777b-11e7-8af3-4d16e69b1dcd.png)

![](https://user-images.githubusercontent.com/11873158/28868914-3e601e3a-777b-11e7-9b24-413740aced98.png)

![](https://user-images.githubusercontent.com/11873158/28868917-3e64e474-777b-11e7-914c-619f34bb0de9.png)

### Exporting to .mesh
![](https://user-images.githubusercontent.com/11873158/28868915-3e622798-777b-11e7-95c5-4ac5f44fc888.png)

### Checking in medit
```bash
medit suzanne.mesh
```
* Z to zoom in
* Shift + Z to zoom out
* F1 to toogle clip
* e to display references
* b to change background
* l to toggle wireframe

![](https://user-images.githubusercontent.com/11873158/28868918-3e66b04c-777b-11e7-998c-aebbea30a944.png)

### Running tetgen
```bash
tetgen -pgaA suzanne.mesh
```
Writes to suzanne.1.mesh

You can get the reference of a tetrahedra with Shift + click, and looking in the terminal (blue = 0, red = 1, green = 2)

![](https://user-images.githubusercontent.com/11873158/28868919-3e74e086-777b-11e7-9af6-a322cefa9bf2.png)

### Removing the green domain (reference 2)
```bash
python pythonMesh/src/removeReference.py suzanne.1.mesh 2
```
![](https://user-images.githubusercontent.com/11873158/28868920-3e75b57e-777b-11e7-847e-91c7231b6792.png)

### Remeshing with mmg3d
```bash
mmg3d suzanne.1.d.mesh
```
Writes in + "suzanne.1.d.o.mesh"

![](https://user-images.githubusercontent.com/11873158/28868921-3e7a200a-777b-11e7-92f1-d8acd68a559e.png)
