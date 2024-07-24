import bpy, bmesh, random

#---Constants
OBJ_NAME = 'Fresh_Made_Room'
'''Name of object to be made'''
GRID_CELL_SIZE = 1
'''Size of a single cell in grid'''
GRID_SIZE_RANGE = (3, 10)
'''Possible size of rows/columns'''
MOD_NAME = 'Room'
'''Name of modifier to add'''
MOD_TYPE = 'NODES'
'''Type of modifier to add'''

#---Methods
def Verts(cols, rows):
    '''Create Verts that will have center around (0, 0)'''
    first_x = float(-1 * cols/2) + .5
    # Set y to go downwards on grid half the count of the rows
    first_y = float(-1 * rows/2) + .5
    # Set list of x cords from the first
    return  [(float(first_x + (x * GRID_CELL_SIZE)),
            float(first_y + (y * GRID_CELL_SIZE)), 0) 
            for x in range(cols) 
            for y in range(rows)]

def Face(column, row): 
    '''Create a single face'''
    return (column* rows + row, 
           (column + 1) * rows + row, 
           (column + 1) * rows + 1 + row, 
           column * rows + 1 + row)

def add_modifier(active_object, modifier_name, modifier_type):
    '''Add modifier to an object'''
    modifier = active_object.modifiers.new(modifier_name, modifier_type)
    modifier.node_group = bpy.data.node_groups[modifier_name]
    for i in range(len(active_object.modifiers) - 1):
        bpy.ops.object.modifier_move_up(modifier = modifier.name)

#Create Column/Row sizes for grid
cols = random.randint(GRID_SIZE_RANGE[0], GRID_SIZE_RANGE[1])
rows = random.randint(GRID_SIZE_RANGE[0], GRID_SIZE_RANGE[1])
#Pass Column/Row sizes for list of verts
verts = Verts(cols, rows)
faces = [Face(x, y) for x in range(cols - 1) for y in range(rows - 1)]

#---Create mesh with prior made lists linked
mesh = bpy.data.meshes.new(OBJ_NAME)
mesh.from_pydata(verts, [], faces)
#---Add object into blender
obj = bpy.data.objects.new(OBJ_NAME, mesh)
# Get the current scene
scene = bpy.context.scene
# Get the main collection of the scene
main_collection = scene.collection
# Link the object to the main collection
main_collection.objects.link(obj)
#---Select newly linked object
bpy.context.view_layer.objects.active = obj

add_modifier(obj, MOD_NAME, MOD_TYPE)

#Create BMesh
bm = bmesh.new()
bm.from_mesh(mesh) 
closed = mesh.attributes.get('closed')
if not closed:
    closed = mesh.attributes.new(name='closed', type='BOOLEAN', domain='EDGE')
    closed.name = 'closed'

#--Carve out the maze
#reset maze by closing all edges
for e in bm.edges:
    setattr(closed.data[e.index], 'value', True) 
