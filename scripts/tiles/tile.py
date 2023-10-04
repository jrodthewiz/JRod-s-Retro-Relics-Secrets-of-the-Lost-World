import pygame
import pymunk

class Tile:
    def __init__(self, texture, is_solid, position, game):
        self.texture = texture
        self.is_solid = is_solid
        self.position = position  # tuple (x, y)
        self.body = None
        self.shape = None
        self.game = game
        
        if self.is_solid:
            self.create_physics_object()
    
    def create_physics_object(self):
        # pymunk physics initialization
        mass = 1  # since it's a static object, mass doesn't matter
        inertia = pymunk.moment_for_box(mass, (self.texture.get_width(), self.texture.get_height()))
        self.body = pymunk.Body(mass, inertia, body_type=pymunk.Body.STATIC)
        self.body.position = (self.position[0] + self.texture.get_width() / 2, self.position[1] + self.texture.get_height() / 2)
        self.shape = pymunk.Poly.create_box(self.body, (self.texture.get_width(), self.texture.get_height()))
        self.shape.friction = 1.0  
        self.shape.elasticity = 0.0
        self.shape.collision_type = 2  # Set a common collision type or different types if you have a handler for them
        self.body.angle = 0  # This sets the angle of the body to 0
        self.body.moment = float('inf')  # This will prevent the body from rotating
        self.game.space.add(self.body, self.shape)
        self.game.shape_to_object_map[self.shape] = self
        #print(f"Creating physics object at {self.position} with size {(self.texture.get_width(), self.texture.get_height())}")  # Debug line

    def render(self, screen, camera):
        
        adjusted_position = self.position  # This line now correctly retains the original position of the tile.

        #screen.blit(self.texture, adjusted_position)
        
        # Debugging: render a pygame rect around the tile
        tile_rect = pygame.Rect(
            adjusted_position[0], adjusted_position[1],
            self.texture.get_width(), self.texture.get_height()
        )

        # Apply the camera transformation to get the rendering position
        rendering_rect = camera.apply_rect(tile_rect)

        # Render the tile texture at the transformed position
        screen.blit(self.texture, rendering_rect.topleft)

        #pygame.draw.rect(screen, (255, 0, 0), rendering_rect, 2)
        
