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
        
        mass = 10
        moment = float('inf') 
        self.body                 = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position        = position
        self.body.angle           = 0  
        self.body.moment          = moment 

        hardcoded_offset_x = 150
        hardcoded_offset_y = 90
        adjusted_shape_description = (
            shape_description[0] - 2*hardcoded_offset_x,
            shape_description[1] - 2*hardcoded_offset_y
        )

        self.shape = pymunk.Poly.create_box(self.body, adjusted_shape_description)

        #self.shape                = pymunk.Poly.create_box(self.body, shape_description)
        self.shape.density        = 2.0
        self.shape.friction       = 1.0
        self.shape.elasticity     = 0.0
        self.shape.collision_type = 1 
        
        self.colliding_left = False
        self.colliding_right = False
        self.colliding_top = False
        self.colliding_bottom = False
        self.in_air = True
        self.bottom_collisions = 0

    def add_to_space(self, space):
        space.add(self.body, self.shape)

    def update(self):
        pass
    
    def set_collision_handler(self, space, collision_type, other_collision_type):
        # Define a collision handler between this object and another type
        handler = space.add_collision_handler(collision_type, other_collision_type)

        # Set callback functions
        handler.begin = self.collision_begin
        handler.separate = self.collision_separate

    def collision_begin(self, arbiter, space, data):
        a_shape, b_shape = arbiter.shapes
        normal = arbiter.normal  # Get the collision normal
            
        right_vector = pymunk.Vec2d(1, 0).rotated(self.body.angle)
        up_vector = pymunk.Vec2d(0, 1).rotated(self.body.angle)

        dot_right = normal.dot(right_vector)
        dot_up = normal.dot(up_vector)

        if abs(dot_right) > abs(dot_up):
            if dot_right > 0:
                self.colliding_left = True
            else:
                self.colliding_right = True
        else:
            if dot_up > 0:
                self.colliding_bottom = True
                self.bottom_collisions += 1
                self.in_air = False
            else:
                self.colliding_top = True

        return True

    def collision_separate(self, arbiter, space, data):
        a_shape, b_shape = arbiter.shapes
        normal = arbiter.normal  # Get the collision normal
            
        right_vector = pymunk.Vec2d(1, 0).rotated(self.body.angle)
        up_vector = pymunk.Vec2d(0, 1).rotated(self.body.angle)

        dot_right = normal.dot(right_vector)
        dot_up = normal.dot(up_vector)

        if abs(dot_right) > abs(dot_up):
            if dot_right > 0:
                self.colliding_left = False
            else:
                self.colliding_right = False
        else:
            if dot_up > 0:
                self.colliding_bottom = False
                self.bottom_collisions -= 1
                if self.bottom_collisions <= 0:
                    self.in_air = True
                    self.bottom_collisions = 0  # Ensure it doesn't go negative
            else:
                self.colliding_top = False