import pygame
import pymunk

from scripts.sprites.animated_sprites import AnimatedSprite
from scripts.physics.physics_object import PhysicsObject

class Player(AnimatedSprite, PhysicsObject):
    def __init__(self, game, texture_manager, position, collision_shape, player_scale_factor, body_type=pymunk.moment_for_circle, ):
        AnimatedSprite.__init__(self, texture_manager)
        PhysicsObject.__init__(self, position, collision_shape, body_type)
        self.collision_shape = collision_shape#(collision_shape[0] * self.scale_factor[0], collision_shape[1] * self.scale_factor[1]) #collision_shape
        self.on_ground = False
        self.jump_strength = -600  # Negative because pymunk's y-axis is inverted
        self.move_speed = 1000
        self.in_air = False
        self.scale_factor = player_scale_factor
        print(self.collision_shape)
        self.flip = False

        #self.add_animation('idle')
        #self.set_animation('idle')
        #self.play_animation()


        self.rect = pygame.Rect(position[0], position[1], collision_shape[0], collision_shape[1])
        self.game = game
        


    def handle_input(self, input_handler):
        velocity_x = 0  
        velocity_y = self.body.velocity.y  
        moving = False  

        if input_handler.is_key_pressed(pygame.K_KP0):
            self.game.debug = not self.game.debug

        if input_handler.is_key_pressed(pygame.K_a) or input_handler.is_key_pressed(pygame.K_LEFT):
            velocity_x = -self.move_speed  
            moving = True
            self.flip = True
        elif input_handler.is_key_pressed(pygame.K_d) or input_handler.is_key_pressed(pygame.K_RIGHT):
            velocity_x = self.move_speed  
            moving = True
            self.flip = False
        
        if (input_handler.is_key_pressed(pygame.K_w) or input_handler.is_key_pressed(pygame.K_SPACE)) and not self.in_air:
            velocity_y = self.jump_strength
            self.set_animation("jump")
        elif moving:
            self.set_animation("run") 
        elif input_handler.is_key_pressed(pygame.K_KP1):
            self.set_animation("jab_double")
        elif input_handler.is_key_pressed(pygame.K_KP2):
            self.set_animation("jab_high")
        elif input_handler.is_key_pressed(pygame.K_KP3):
            self.set_animation("kick_low")
        elif input_handler.is_key_pressed(pygame.K_KP4):
            self.set_animation("kick_high")
        elif input_handler.is_key_pressed(pygame.K_KP5):
            self.set_animation("reverse_kick")
        else:
            self.set_animation("idle")

        self.body.velocity = pymunk.Vec2d(velocity_x, velocity_y)  # set the new velocity to the body

    def update(self):
        self.body.angle = 0
        self.rect.x = self.body.position.x - self.rect.width  / 2
        self.rect.y = self.body.position.y - self.rect.height / 2
        super().update()
    
    def render(self, screen, camera, position=None):
        pymunk_position = position or self.body.position
        pygame_y = pymunk_position[1] 
        pygame_rect = pygame.Rect(
            pymunk_position[0] - self.rect.width / 2,
            pygame_y - self.rect.height / 2,
            self.rect.width,
            self.rect.height
        )
        rendering_rect = camera.apply_rect(pygame_rect)
        super().render(screen, rendering_rect.topleft, self.flip)
        
        #Draw the physics collider
        if self.game.debug:
            vertices = [v.rotated(self.body.angle) + pymunk_position for v in self.shape.get_vertices()]
            vertices_camera_adjusted = [camera.apply((int(v.x), int(v.y))) for v in vertices]
            vertices_pygame = [self.game.pymunk_to_pygame_simple(v) for v in vertices_camera_adjusted]
            pygame.draw.polygon(screen, (0, 255, 0), vertices_pygame, 2)