import bpy, bmesh, random

#Constants
MODIFIER_NAME = 'Maze'
MODIFIER_TYPE = 'NODES'
OBJECT_TYPE = 'MESH'


#get currently active object
active = bpy.context.active_object

#throw exception if active object is not a mesh
if active.type != OBJECT_TYPE:
    raise Exception(f'Active type must be a {OBJECT_TYPE.lower()}.')

#--Ensure active object has maze modifier
#Get maze object for comparison and set empty to store active object's modifier
maze_nodes = bpy.data.node_groups[MODIFIER_NAME]
maze_modifier = None
#Loop through active objects modifiers checking for maze geometry nodes modifier
for modifier in active.modifiers:
    if modifier.type == MODIFIER_TYPE and modifier.node_group == maze_nodes:
        maze_modifier = modifier
        break #stop looping once the modifier is found
#Check if maze modifier was found
if not maze_modifier:
    #create new maze modifier 
    maze_modifier = active.modifiers.new(MODIFIER_NAME, MODIFIER_TYPE)
    maze_modifier.node_group = bpy.data.node_groups[MODIFIER_NAME]
    for i in range(len(active.modifiers) - 1):
        bpy.ops.object.modifier_move_up(modifier = maze_modifier.name)

#Get the active mesh and make sure it has the 'closed' attribute
mesh = active.data
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
#randomly choose a cell to start carving out the maze from
current_cell = random.choice(list(bm.faces))
visited = [current_cell]
stack = [current_cell]
#loop until entire maze has been carved out
while len(stack) > 0:
    current_cell = stack.pop()

    #get list of unvisited neighbors to the current cell
    unvisited_neighbors = []
    for edge in current_cell.edges:
        for neighbor in edge.link_faces:
            if neighbor != current_cell and neighbor not in visited:
                unvisited_neighbors.append(neighbor)
    
    #if there are any univisited neighbors then 'randomly' choose one to visit
    if len(unvisited_neighbors) > 0:
        stack.append(current_cell)
        chosen_neighbor = random.choice(unvisited_neighbors)
        visited.append(chosen_neighbor)
        stack.append(chosen_neighbor)

        #open all the edges between the current cell and the chosen neighbor
        for edge in current_cell.edges:
            if edge in chosen_neighbor.edges:
                setattr(closed.data[edge.index], 'value', False)

mesh.update()