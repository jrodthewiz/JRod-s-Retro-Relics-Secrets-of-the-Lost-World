import pymunk
import time
class PhysicsObject:
    
    def __init__(self, position, shape_description, body_type=pymunk.moment_for_box):
        
        mass = 10
        moment = float('inf') 
        self.body                 = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position        = position
        self.body.angle           = 0  
        self.body.moment          = moment 

        hardcoded_offset_x = 200
        hardcoded_offset_y = 90
        adjusted_shape_description = (
            shape_description[0] - 2*hardcoded_offset_x,
            shape_description[1] - 2*hardcoded_offset_y
        )


        self.shape = pymunk.Poly.create_box(self.body, adjusted_shape_description)
        self.shape.data = self

        self.shape.friction = 1.0  # You could try increasing this value slightly
        self.shape.elasticity = 0.0  # Ensure this remains at 0 to prevent bouncing
        self.shape.density = 2.0  # You could experiment with different density values
        self.shape.collision_type = 1 
        
        self.colliding_left = False
        self.colliding_right = False
        self.colliding_top = False
        self.colliding_bottom = False
        self.in_air = True
        self.bottom_collisions = 0
        self.last_ground_contact = time.time()  # Add this line to track the last time the player touched the ground
        self.ground_contact_buffer = 0.2  # Duration (in seconds) before setting in_air to True
        self.is_colliding_with_type1 = False

    def add_to_space(self, space):
        space.add(self.body, self.shape)
        

    def update(self):
        pass
    
    def set_collision_handler(self, space, collision_type, other_collision_type):
        handler = space.add_collision_handler(collision_type, other_collision_type)
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
                self.jumps_made = 0  # Reset the jumps when on the ground
                self.last_ground_contact = time.time()
            else:
                self.colliding_top = True


        # character_a = self.game.shape_to_object_map.get(a_shape)
        # character_b = self.game.shape_to_object_map.get(b_shape)

        # print(type(character_a))
        # print(type(character_b))


        # if b_shape.collision_type == 2:
        #     print("started to collide with collision_type ", 2)
        #     self.is_colliding_with_type1 = True
            
        #     # Adjust the position of the object to overlap by the overlap_distance
        #     overlap_vector = normal * 1.0
        #     self.body.position += overlap_vector


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
                    if time.time() - self.last_ground_contact >= self.ground_contact_buffer:
                        self.in_air = True
                    self.bottom_collisions = 0  # Ensure it doesn't go negative
            else:
                self.colliding_top = False

        if b_shape.collision_type == 2:
            self.is_colliding_with_type1 = False
            print("ending our collision with collision_type ", 2)