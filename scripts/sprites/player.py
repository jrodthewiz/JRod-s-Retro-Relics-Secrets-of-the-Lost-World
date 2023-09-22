import pygame
import pymunk

from scripts.sprites.animated_sprites import AnimatedSprite
from scripts.physics.physics_object import PhysicsObject
from scripts.sprites.sprite import Sprite

class Player(AnimatedSprite, PhysicsObject):
    def __init__(self, texture_manager, position, collision_shape, body_type=pymunk.moment_for_circle):
        AnimatedSprite.__init__(self, texture_manager)
        PhysicsObject.__init__(self, position, collision_shape, body_type)
        self.on_ground = False
        self.jump_strength = -300  # Negative because pymunk's y-axis is inverted
        self.in_air = False
        self.rect = pygame.Rect(position[0], position[1], collision_shape[0], collision_shape[1])


    def handle_input(self, input_handler):
        if input_handler.is_key_pressed(pygame.K_LEFT):
            force = (-2000, 0)  # Horizontal force to the left
            self.body.apply_force_at_local_point(force, (0, 0))
            self.set_animation('idle')
        elif input_handler.is_key_pressed(pygame.K_RIGHT):
            force = (2000, 0)  # Horizontal force to the right
            self.body.apply_force_at_local_point(force, (0, 0))
            self.set_animation('idle')
        else:
            new_velocity_x = self.body.velocity.x * 0.9  # Simple damping to reduce horizontal velocity
            self.body.velocity = pymunk.Vec2d(new_velocity_x, self.body.velocity.y)

        if input_handler.is_key_pressed(pygame.K_SPACE) and not self.in_air:
            impulse = (0, self.jump_strength)  # Upward impulse
            self.body.apply_impulse_at_local_point(impulse, (0, 0))
            self.set_animation('idle')



    def update(self):
        # Call the parent update method
        super().update()
        # Any player-specific update logic

    
    def render(self, screen, camera, position=None):
        pymunk_position = position or self.body.position
        pygame_position = (pymunk_position.x, camera.height - pymunk_position.y)  # Flipping Y-coordinate
        rendering_position = camera.apply_rect(pygame.Rect(pygame_position, self.rect.size)).topleft
        super().render(screen, rendering_position)