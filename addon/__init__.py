bl_info = {
    'name': 'ISCD Addon',
    'category': 'Import-Export',
    'version': (0, 0, 2),
    'blender': (2, 78, 0),
    "description": "Imports and exports 3d  meshes and interfaces with ISCD tools",
    "author": "Loïc NORGEOT",
    "warning": "Needs the installation of exterior software!"
}

modulesNames = ['msh',
'operator_bake',
'operator_cork',
'operator_export_mesh',
'operator_import_mesh',
'operator_import_sequence',
'operator_mmgs',
'operator_medit',
'operator_tetgen_hull',
'operator_tetgen_fill',
'operator_metis_partition',
'operator_superPCS',
'layout']

import sys
import importlib

if importlib.find_loader('scipy') is not None:
    modulesNames.append('icp')
    modulesNames.append('operator_icp')

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
