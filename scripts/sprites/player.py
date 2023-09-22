import pygame
import pymunk

from scripts.sprites.animated_sprites import AnimatedSprite
from scripts.physics.physics_object import PhysicsObject


class Player(AnimatedSprite, PhysicsObject):
    def __init__(self, position, texture_folder, collision_shape, body_type=pymunk.moment_for_circle):
        AnimatedSprite.__init__(self, texture_folder)
        PhysicsObject.__init__(self, position, collision_shape, body_type)

        # Attributes specific to the Player class
        self.on_ground = False
        self.jump_strength = -300  # Negative because pymunk's y-axis is inverted