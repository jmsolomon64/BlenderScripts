import bpy

def is_mesh(active_object, object_type):
    '''
        Check if an object is of mesh type

        Args:
            active_object: object for comparison
            object_type: type object should be compared against

        Returns:
            bool
    '''
    if active_object.type != object_type:
        return False
    else:
        return True

def find_modifier(modifier_name, modifier_type, active_object ):
    '''
    Get object for comparison and set empty to store active object's modifier
       
        Args:
            modifier_name: name of the modifier to look for
            modifier_type: type associated with modifier
            active_object: object search will be performed on
        Returns:
            objects modifier
    '''
    nodes = bpy.data.node_groups[modifier_name]
    node_modifier = None
    #Loop through active objects modifiers checking for maze geometry nodes modifier
    for modifier in active_object.modifiers:
        if modifier.type == modifier_type and modifier.node_group == nodes:
            node_modifier = modifier
            return node_modifier #stop looping once the modifier is found
        
def add_modifier(active_object, modifier_name, modifier_type):
    '''
    Add modifier to an object
    
        Args:
    '''
    modifier = active_object.modifiers.new(modifier_name, modifier_type)
    modifier.node_group = bpy.data.node_groups[modifier_name]
    for i in range(len(active_object.modifiers) - 1):
        bpy.ops.object.modifier_move_up(modifier = modifier.name)



