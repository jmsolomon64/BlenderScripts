import bpy, bmesh

OBJECT_TYPE = 'MESH'


#get currently active object
active = bpy.context.active_object

#throw exception if active object is not a mesh
if active.type != OBJECT_TYPE:
    raise Exception(f'Active type must be a {OBJECT_TYPE.lower()}.')

closed = active.attributes.get('closed')
posted = active.attributes.get('posted')

print(f'closed count: {len(closed)}')
print(f'posted count: {len(posted)}')

#---- NEED to research link_edges
