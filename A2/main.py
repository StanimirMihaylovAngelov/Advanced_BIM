# import IfcOpenShell
import ifcopenshell

# open model
model = ifcopenshell.open('models\ARK_new.ifc')
project = (model.by_type('IfcProject'))
print(f'The loaded project is: {project[0].LongName}')


#----------------- WINDOWS ---------------------

window = model.by_type('IfcWindow')[0]
windows = (model.by_type('IfcWindow'))

# for every window, ID, height, width and area is found:
x=[]
totalWindowArea = 0
for window in windows: #every window with data   
    #overall width for each window:
    w = window.OverallWidth
    #overall height for each window:
    h = window.OverallHeight
    #propertySet for each window:
    windowPropSet = ifcopenshell.util.element.get_psets(window)
    #area for each window:
    area = (w/1000)*(h/1000)
    #writing data into matrix x:
    x.append([window.id(),window.OverallHeight,window.OverallWidth,area,windowPropSet.get('Pset_WindowCommon').get('IsExternal')])
 

#----------------- SPACES ---------------------

# Finding the windows related to the spaces:
y=[]
for space in model.by_type("IfcSpace"):
    near = space.BoundedBy
    #print("\n\t####{}\n".format(space.id()))
    for objects in near:
        if (objects.RelatedBuildingElement != None):
            if (objects.RelatedBuildingElement.is_a('IfcWindow')):
                #print(objects.RelatedBuildingElement.id())
                if space.id() not in x:
                    y.append([space.id(),objects.RelatedBuildingElement.id()])

# Filtering so only external windows are in the list:
filtered_list = [row for row in x if row[-1]]
# Filtering so only windows which are related to a space are in the list:
result = [[item[0]] + row for row in filtered_list for item in y if row[0] == item[1]]


# Floor area of the spaces:
space_ids = [row[0] for row in result]
areas = {}
for space_id in space_ids:
    space = model.by_id(space_id)

    for prop_set_def in space.IsDefinedBy:
        if prop_set_def.is_a("IfcRelDefinesByProperties"):
            prop_set = prop_set_def.RelatingPropertyDefinition
            if prop_set.is_a("IfcPropertySet"):
                for prop in prop_set.HasProperties:
                    if prop.Name == 'NetFloorArea' or prop.Name == 'GrossFloorArea':  
                        areas[space_id] = prop.NominalValue.wrappedValue
            elif prop_set.is_a("IfcElementQuantity"):
                for quant in prop_set.Quantities:
                    if quant.Name == 'NetFloorArea' or quant.Name == 'GrossFloorArea':  
                        areas[space_id] = quant.AreaValue

# For spaces with multiple windows, the window areas are summed:
aggregate_dict = {}
for row in result:
    id_ = row[0]
    value = row[4]

    if id_ in aggregate_dict:
        aggregate_dict[id_][4] += value
    else:
        aggregate_dict[id_] = row.copy()  # Create a copy of the row

# Convert the aggregated dictionary back to a list
new_result = list(aggregate_dict.values())


#----------------- OUTPUT ---------------------

# Lists of spaces, floor areas, and window areas
SpaceID = [row[0] for row in new_result]
floor_area = list(areas.values())
window_area = [row[4] for row in new_result]

# Iterate through the spaces and calculate the W2F ratio for each space
for i in range(len(SpaceID)):
    space = SpaceID[i]
    #spacename = model.by_type('IfcSpace')[].LongName
    area = floor_area[i]
    w_area = window_area[i]
    
    # Calculate the W2F ratio
    w2f_ratio = (w_area / area) * 100
    
    # Check if the ratio is below 10%
    if w2f_ratio < 10:
        print(f"Space with ID '{space}' has a W2F ratio < 10%, and needs to be changed.")
    else:
        print(f"Space with ID '{space}' has a W2F ratio >/= 10%")


