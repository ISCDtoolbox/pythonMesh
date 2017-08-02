# ISCD summer school 2017

On this page:
* 1 - How to install:
* 2 - Workflow:

## 1 - Installation

First of all, clone the github repository on your computer:
```bash
git clone https://github.com/ISCDtoolbox/pythonMesh.git
cd pythonMesh
cd src
```

One of the software will need external dependencies:
```bash
sudo apt-get install libxmu-dev libxi-dev
```

Before installing the collection of softwares, add the following line at the end of the ".bashrc" file, which is located in your home directory (this will allow your system to locate the compiled executables):
```bash
export PATH=$PATH:~/bin/
```
In order to allow your computer to take the changes into account, either restart a terminal or type the following command:
```bash
souurce ~/.bashrc
```

### 1.1 - Running the install script
Navigate to the src directory, and execute the "install.sh" script:
```bash
cd src
sh install.sh
```

To test that everything went fine (if there were no errors), type in a terminal,, try to open the demo/Theatre.mesh file with the software medit:
```bash
medit ~/pythonMesh/demo/Theatre.mesh
```

### 1.2 - Installing blender addons
Addons installation: File -> User Preferences -> Addons

First, install the "3D print toolbox" addon, which will allow us to check the quality of our mesh.

Now, download the [Zip archive](https://github.com/ISCDtoolbox/pythonMesh/releases/download/1.0/addon.zip) which will allow to interface the .mesh 3D format (used by the installed softwares) with blender, and install it by selecting it in the User preferences window, and checking the corresponding checkbox (ISCD addon):
<p align="center">
<img src="https://user-images.githubusercontent.com/11873158/28865179-44744866-776f-11e7-993a-72902a2e0a05.png"/>
<h4 align="center">Install the addon from the zip archive</h4>
</p>

You should now have two new tabs on the left part of the Tools menu (which can be opened with the shortcut "T"):
<p align="center">
<img src="https://user-images.githubusercontent.com/11873158/28865364-eb9aefbe-776f-11e7-9cd3-721e5dada275.png"/>
<h4 align="center">Addons installed</h4>
</p>

## 2 - Workflow

### 2.1 - Preparing the simulation in blender
* 1 - Model a High Resolution object: it can be as complex or heavy (millions of points) as you wish
* 2 - Create a Low Resolution copy (remeshed, or a new object made from scratch) of your object, removing details but staying loyal to your objects surface. **Check that your object is closed and has no intersection with the 3D print toolbox**
* 3 - (optional) add a computational domain to your LR model
* 4 - Create different materials for the fluid inlet, the outlet, the obstacle (your mesh) and the boundaries of your domain (if you had to go through step 3)
* 5 - Export your LR model to .mesh format
* 6 - Check that your file exported correctly with **medit**

### 2.2 - Create a tetrahedral domain
* 1 - Run **tetgen** on your exported LR model
* 2 - (optional) Get the reference of the inside domain with **medit**
* 3 - (optional) Remove the reference of the inside domain with **removeReference.py**
* 4 - Remesh the volume with **mmg3d**
* 5 - Check that the remeshing went correctly with **medit**

### 2.3 - Run the simulation
* 1 - Write the DEFAULT.nstokes file
* 2 - Run the simulation with **nstokes**
* 3 - Grab a cup of coffee
* 4 - Check your results with **medit**

### 2.4 - Create the visualization with Paraview
* 1 - Convert your results to Paraview format with **convertToParaview.py**
* 2 - Open your file in **Paraview**
* 3 - Prepare your visualization
* 4 - Export the scene to .x3d format

### 2.5 - Put it all together in blender
* 1 - Import the x3d scene in blender
* 2 - Remove unnecessary objects and clean the scene
* 3 - Adjust the materials
* 4 - Render

### 3.1 - Examples
* [Fluid outside an object](docs/fluidsOutside.md)
* [Fluid inside  an object](docs/fluidsInside.md)
