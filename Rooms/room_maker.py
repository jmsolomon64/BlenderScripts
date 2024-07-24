import bpy, bmesh, random

#Goal: Proceduraly create a grid with missing sections to create a room
#1) Create a grid with a 'random' size 
#  X-Create bmesh object 
#  X-Render Grid
#2) Remove pieces from the grid to create a unique shape
#  -'Randomly' remove pieces of the grid 
#  -Check if one cell can reach all other cells
#  -If not add cells until a connection is made 
#3) Add walls around all the missing pieces
#  X-Give edges that touch one face the 'closed' attribute
#  X-Apply maze modifier to grid
#  -May need to alter maze modifier so that posts don't render in every point of the grid

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

def calculate_remove_amount():
    removeAmount = 0
    if cols == GRID_SIZE_RANGE[0]:
        removeAmount = 1
    elif cols == GRID_SIZE_RANGE[1]:
        removeAmount = 3
    else:
        removeAmount= 2
    if rows == GRID_SIZE_RANGE[0]:
        removeAmount += 1
    elif rows == GRID_SIZE_RANGE[1]:
        removeAmount += 3
    else:
        removeAmount += 2
    return removeAmount

def deselect_all(bm):
    for f in bm.faces:
        f.select = False
    for e in bm.edges:
        e.select = False
    for v in bm.verts:
        v.select = False

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

# Toggle into edit mode and fill bmesh with edit mode data
bpy.ops.object.editmode_toggle()
bm = bmesh.from_edit_mesh(mesh)
# Deselect every face in edit mode
bpy.ops.mesh.select_all(action='DESELECT')

# Determine how many faces to remove
# Then select random faces up to that amount
removeAmount = calculate_remove_amount()
for i in range(removeAmount):
    face = random.choice([face for face in bm.faces]).select = True


# bmesh.update_edit_mesh(mesh=mesh, destructive=True)
bpy.ops.mesh.delete(type='FACE')

#Return to object mode and refresh bmesh data for object mode data
bpy.ops.object.editmode_toggle()
bm = bmesh.new()
bm.from_mesh(mesh) 

#Check for/create modifier
closed = mesh.attributes.get('closed')
posted = mesh.attributes.get('posted')
if not closed:
    closed = mesh.attributes.new(name='closed', type='BOOLEAN', domain='EDGE')
    closed.name = 'closed'
if not posted:
    posted = mesh.attributes.new(name='posted', type='BOOLEAN', domain='POINT')
    posted.name = 'posted'


#Set closed attribute for all edges with only one linked face
for e in bm.edges: 
    setattr(closed.data[e.index], 'value', True)
    if len(e.link_faces) == 1:
        setattr(closed.data[e.index], 'value', True)
        
    else:
        setattr(closed.data[e.index], 'value', False)

#Set posted attribute for all verts with less than four linked faces
for v in bm.verts:
    if len(v.link_faces) < 4:
        setattr(posted.data[v.index], 'value', True)
    else:
        setattr(posted.data[v.index], 'value', False)
        

