# import
from pathlib import Path
import ifcopenshell

modelname = "Example"

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



# Get Infomation
wall = (model.by_type('IfcWall'))[0];
print(wall.get_info())


# Add informations 
products = model.by_type("IfcProduct")
owner_history = model.by_type("IfcOwnerHistory")[0]

walls=[]
for i in products:
    if i.is_a("IfcWall"):
        walls.append(i) 

property_values = [
    model.createIfcPropertySingleValue("Example Text ", "", model.create_entity("IfcText", "Hello World"), None),
]   
for wall in walls:
    property_set = model.createIfcPropertySet(wall.GlobalId, owner_history, "Example Property ", None, property_values)
    model.createIfcRelDefinesByProperties(wall.GlobalId, owner_history, None, None, [wall], property_set)

model.write(model_url)  

print("Done - Reload model")
