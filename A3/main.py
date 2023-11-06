from pathlib import Path
import ifcopenshell

modelname = "ARK_new"

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


# ---------------- Slabs ----------------

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

# ---------------- Coverings ----------------

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

# Saving the new IFC-model
model.write(model_url)  
print("Done - Reload the model")