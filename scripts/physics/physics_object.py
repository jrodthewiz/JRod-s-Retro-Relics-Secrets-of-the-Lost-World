import pymunk


# # Initialize pymunk space
# space = pymunk.Space()
# space.gravity = (0, -900)  # Some gravity to pull objects down

# # Create two physics objects
# player = PhysicsObject((100, 100), (50, 100))
# enemy = PhysicsObject((150, 150), (60, 120))

# # Set collision types (you might want to define these as constants somewhere)
# player.shape.collision_type = 1
# enemy.shape.collision_type = 2

# # Add objects to the pymunk space
# player.add_to_space(space)
# enemy.add_to_space(space)

# # Setup collision handler
# player.set_collision_handler(space, 1, 2)


# Now, in your game loop, whenever you call space.step(), the collision callbacks will be triggered if the player and enemy collide
# for i in range(100):  # Simulate 100 frames
#     space.step(1/60.0)  # Assuming 60 FPS

#     # You can then check collision flags on the player
#     if player.colliding_bottom:
#         print("Player collided with the bottom!")
#     if player.colliding_left:
#         print("Player collided on the left!")
#     # ... and so on


class PhysicsObject:
    def __init__(self, position, shape_description, body_type=pymunk.moment_for_box):
        # Create the pymunk body
        self.body = pymunk.Body(1, body_type)
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
        
    def add_to_space(self, space):
        space.add(self.body, self.shape)

    def update(self):
        # For now, this method can be a placeholder
        # Pymunk will automatically update the position and rotation of the body
        # as it interacts with other objects in the space
        # You can include any specific update logic if needed
        pass

    def set_collision_handler(self, space, collision_type, other_collision_type):
        # Define a collision handler between this object and another type
        handler = space.add_collision_handler(collision_type, other_collision_type)

        # Set callback functions
        handler.begin = self.collision_begin
        handler.separate = self.collision_separate

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
