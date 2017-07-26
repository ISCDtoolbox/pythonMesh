bl_info = {
    'name': 'ISCD Addon',
    'category': 'Import-Export',
    'version': (0, 0, 2),
    'blender': (2, 78, 0),
    "description": "Imports and exports 3d  meshes and interfaces with ISCD tools",
    "author": "Loïc NORGEOT",
    "warning": "Needs the installation of exterior software!"
}

modulesNames = [
'msh',
'operator_bake',
'operator_domain',
'operator_export_mesh',
'operator_import_mesh',
'operator_import_sequence',
'layout'
]

import sys
import importlib
import os

if importlib.find_loader('scipy') is not None:
    modulesNames.append('icp')
    modulesNames.append('operator_icp')
if not os.system("which mmgs_O3"):
    modulesNames.append('operator_mmgs')
if not os.system("which medit"):
    modulesNames.append('operator_medit')
if not os.system("which tetgen"):
    modulesNames.append('operator_tetgen_hull')
    modulesNames.append('operator_tetgen_fill')
if not os.system("which mpmetis"):
    modulesNames.append('operator_metis_partition')
if not os.system("which cork"):
    modulesNames.append('operator_cork')
if not os.system("which super4PCS"):
    modulesNames.append('operator_superPCS')

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()

if __name__ == "__main__":
    register()
