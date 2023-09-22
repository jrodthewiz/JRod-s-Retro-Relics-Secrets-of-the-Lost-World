import pygame
import pymunk

class Tile:
    def __init__(self, texture, is_solid, position):
        self.texture = texture
        self.is_solid = is_solid
        self.position = position  # tuple (x, y)
        self.body = None
        self.shape = None
        
        if self.is_solid:
            self.create_physics_object()
    
    def create_physics_object(self):
        # pymunk physics initialization
        mass = 1  # since it's a static object, mass doesn't matter
        inertia = pymunk.moment_for_box(mass, (self.texture.get_width(), self.texture.get_height()))
        self.body = pymunk.Body(mass, inertia, body_type=pymunk.Body.STATIC)
        self.body.position = self.position
        self.shape = pymunk.Poly.create_box(self.body, (self.texture.get_width(), self.texture.get_height()))
        self.shape.friction = 0.8  # adjust as needed
    
    def render(self, screen, camera_offset):
        # camera_offset is a tuple (x_offset, y_offset)
        screen.blit(self.texture, (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1]))
