import pymunk

class PhysicsObject:
    """
    The PhysicsObject class encapsulates a physics body and shape using the pymunk library.
    It provides methods for adding the object to a pymunk space, updating the object, and 
    setting up collision handling with other physics objects.
    """


    """
    Initializes a new PhysicsObject with a given position, shape description,
    and optionally a body type function to calculate the moment of inertia.
    
    Parameters:
        - position (tuple): The initial position of the object as a (x, y) tuple.
        - shape_description (tuple): The dimensions of the object as a (width, height) tuple.
        - body_type (function, optional): A function to calculate the moment of inertia, 
                                            default is pymunk.moment_for_box.
    """
    def __init__(self, position, shape_description, body_type=pymunk.moment_for_box):
        # Assume a default mass of 1 for now
        mass = 1

        # Calculate the moment of inertia based on the dimensions of a box
        # Assuming `shape_description` is a tuple of the form (width, height)
        width, height = shape_description
        moment = pymunk.moment_for_box(mass, (width, height))

        # Create the pymunk body
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        # Create the shape based on the description
        # For simplicity, we'll use a rectangle here.
        self.shape = pymunk.Poly.create_box(self.body, shape_description)
        self.shape.density = 1.0
        self.shape.friction = 0.5

        # Collision attributes
        self.colliding_left = False
        self.colliding_right = False
        self.colliding_top = False
        self.colliding_bottom = False
        self.in_air = True

    """
    Adds the PhysicsObject to a pymunk space.
    
    Parameters:
        - space (pymunk.Space): The pymunk space to which to add the object.
    """
    def add_to_space(self, space):
        space.add(self.body, self.shape)

    """
    Updates the PhysicsObject. This method serves as a placeholder for now,
    but can be overridden or extended with specific update logic if needed.
    """
    def update(self):
        # For now, this method can be a placeholder
        # Pymunk will automatically update the position and rotation of the body
        # as it interacts with other objects in the space
        # You can include any specific update logic if needed
        pass

    """
    Sets up a collision handler for interactions between this PhysicsObject
    and another type of physics object.
    
    Parameters:
        - space (pymunk.Space): The pymunk space in which the objects reside.
        - collision_type (int): The collision type identifier for this object.
        - other_collision_type (int): The collision type identifier for the other object.
    """
    def set_collision_handler(self, space, collision_type, other_collision_type):
        # Define a collision handler between this object and another type
        handler = space.add_collision_handler(collision_type, other_collision_type)

        # Set callback functions
        handler.begin = self.collision_begin
        handler.separate = self.collision_separate

    """
    Callback method called when a collision begins. Updates collision flags 
    based on the collision normal.
    
    Parameters:
        - arbiter (pymunk.Arbiter): The arbiter for the collision.
        - space (pymunk.Space): The pymunk space in which the collision occurred.
        - data (dict): Optional data associated with the collision.
        
    Returns:
        - True to process the collision normally.
    """
    def collision_begin(self, arbiter, space, data):
        # This function is called when a collision begins
        normal = arbiter.normal

        # Check direction of normal to determine collision side
        if abs(normal.x) > abs(normal.y):
            if normal.x > 0:
                self.colliding_left = True
            else:
                self.colliding_right = True
        else:
            if normal.y > 0:
                self.colliding_bottom = True
                self.in_air = False
            else:
                self.colliding_top = True

        return True  # Return True to process the collision normally

    """
    Callback method called when a collision ends. Resets collision flags based 
    on the collision normal.
    
    Parameters:
        - arbiter (pymunk.Arbiter): The arbiter for the collision.
        - space (pymunk.Space): The pymunk space in which the collision occurred.
        - data (dict): Optional data associated with the collision.
    """
    def collision_separate(self, arbiter, space, data):
        # This function is called when the collision ends
        normal = arbiter.normal

        # Reset collision flags
        if abs(normal.x) > abs(normal.y):
            if normal.x > 0:
                self.colliding_left = False
            else:
                self.colliding_right = False
        else:
            if normal.y > 0:
                self.colliding_bottom = False
                self.in_air = True
            else:
                self.colliding_top = False
