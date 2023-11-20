# Welcome
# This script is created by Group 5 in the 'Advanced BIM'-course at DTU (Fall-2023)
# This script creates a new CustomPropertySet for the standard reflectance of the walls, floors and ceilings, to prepair
# the IFC moodels for a daylight analysis. The standard reflectances are from the ISO 17037.


# Importing the Path-function + its library
from pathlib import Path
# Importing IFC OpenShell
import ifcopenshell

# Defineing the file name of the IFC model:
modelname = "ARK_new"

# Loading the IFC model by using the Path-function
try:
    dir_path = Path(__file__).parent
    model_url = Path.joinpath(dir_path, 'model', modelname).with_suffix('.ifc')
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")


# Print project name
project = (model.by_type('IfcProject'))
print(f'The loaded project is: {project[0].LongName}')

# Defining the IfcProduct and IfcOwnerHistory
products = model.by_type("IfcProduct")
owner_history = model.by_type("IfcOwnerHistory")[0]


# ---------------- Walls ----------------

walls=[]
for i in products:
    if i.is_a("IfcWall"):
        walls.append(i) 
# Creating a new Single Value for the Standard Reflectance for walls (from DS/ISO 17037)
property_values = [
    model.createIfcPropertySingleValue("Reflectance ", "Some Property  Name", model.create_entity("IfcText", "0,5"), None),
]   
# Creating a new Custom Property Set for every wall
for wall in walls:
    property_set = model.createIfcPropertySet(wall.GlobalId, owner_history, "Custom Property Set", None, property_values)
    model.createIfcRelDefinesByProperties(wall.GlobalId, owner_history, None, None, [wall], property_set)


# ---------------- Slabs (Floors) ----------------

Slabs=[]
for i in products:
    if i.is_a("IfcSlab"):
        Slabs.append(i) 
# Creating a new Single Value for the Standard Reflectance for floors (from DS/ISO 17037)  
property_values = [
    model.createIfcPropertySingleValue("Reflectance ", "Some Property  Name", model.create_entity("IfcText", "0,2"), None),
]   
# Creating a new Custom Property Set for every slab
for Slab in Slabs:
    property_set = model.createIfcPropertySet(Slab.GlobalId, owner_history, "Custom Property Set", None, property_values)
    model.createIfcRelDefinesByProperties(Slab.GlobalId, owner_history, None, None, [Slab], property_set)

# ---------------- Coverings (Ceilings) ----------------

Coverings=[]
for i in products:
    if i.is_a("IfcCovering"):
        Coverings.append(i) 
# Creating a new Single Value for the Standard Reflectance for ceiling (from DS/ISO 17037)
property_values = [
    model.createIfcPropertySingleValue("Reflectance ", "Some Property  Name", model.create_entity("IfcText", "0,7"), None),
]   
# Creating a new Custom Property Set for every covering
for covering in Coverings:
    property_set = model.createIfcPropertySet(covering.GlobalId, owner_history, "Custom Property Set", None, property_values)
    model.createIfcRelDefinesByProperties(covering.GlobalId, owner_history, None, None, [covering], property_set)


# ----------------- Updating the IFC-file ------------------

# Writing(saves) updated IFC-file to disk
model.write(model_url)  
print("Done - Reload the model")
