import pygame
import pymunk

from scripts.sprites.animated_sprites import AnimatedSprite
from scripts.physics.physics_object import PhysicsObject
pygame.mixer.init()
class Enemy(AnimatedSprite, PhysicsObject):
    def __init__(self, game, texture_manager, position, collision_shape, scale_factor, body_type=pymunk.moment_for_circle):
        super().__init__(texture_manager)
        PhysicsObject.__init__(self, position, collision_shape, body_type)
        self.collision_shape = collision_shape
        self.scale_factor = scale_factor
        self.rect = pygame.Rect(position[0], position[1], collision_shape[0], collision_shape[1])
        self.game = game
        self.game.shape_to_object_map[self.shape] = self
        self.weapon = None
        self.display_text = None
        # Additional properties to track AI state
        self.target = self.game.player
        self.alert_range = 1000  # Radius around the enemy where they start following the player
        self.flip = False
        self.move_speed = 100
        self.shape.collision_type = 3 
        print("Enemy: ", self, " Shape: ", self.shape, " Body: ", self.body)

    def compute_distance_to_target(self, target):
        dx = target.body.position.x - self.body.position.x
        dy = target.body.position.y - self.body.position.y
        return (dx**2 + dy**2)**0.5

    def ai_logic(self):
        dx = self.target.body.position.x - self.body.position.x
        dy = self.target.body.position.y - self.body.position.y
        distance_to_player = (dx**2 + dy**2)**0.5
        
        if distance_to_player < self.alert_range:
            if dx > 0:
                # Player is to the right, move right
                self.body.velocity = pymunk.Vec2d(self.move_speed, self.body.velocity.y)
                self.flip = False
                self.set_animation("run")
            else:
                # Player is to the left, move left
                self.body.velocity = pymunk.Vec2d(-self.move_speed, self.body.velocity.y)
                self.flip = True
                self.set_animation("run")
        else:
            self.body.velocity = pymunk.Vec2d(0, self.body.velocity.y)
            self.set_animation("idle")
        
        # Check distances to other enemies and avoid collisions
        for shape, enemy in self.game.shape_to_object_map.items():
            if enemy is not self and isinstance(enemy, Enemy):
                distance = self.compute_distance_to_target(enemy)
                if distance < self.alert_range / 2:  # If too close to another enemy
                    if enemy.body.position.x > self.body.position.x:
                        self.body.velocity = pymunk.Vec2d(-self.move_speed // 2, self.body.velocity.y)

                    else:
                        self.body.velocity = pymunk.Vec2d(self.move_speed // 2, self.body.velocity.y)


    def update(self):
        self.ai_logic()  # AI Behavior
        self.body.angle = 0
        self.rect.x = self.body.position.x - self.rect.width / 2
        self.rect.y = self.body.position.y - self.rect.height / 2

        # Check if we should play a sound for the current animation frame
        current_frame_index = self.current_frame
        current_animation_name = self.current_animation
        if self.game.texture_manager.should_play_sound(current_animation_name, current_frame_index):
            sound_name = current_animation_name + "_sound" 

            # if self.is_colliding_with_type1:
            #     sound_name = current_animation_name + "_sound" + "_collision1"


            sound_to_play = self.texture_manager.get_audio(sound_name)
            sound_to_play.set_volume(1.0)  # set to maximum volume
            sound_to_play.play()

        super().update()

    def render(self, screen, camera, position=None):

        #Rendering player sprite based on pymunk position and camera
        pymunk_position = position or self.body.position
        pygame_y = pymunk_position[1] 


        #Sprite rendering offset
        center_offset = 0
        if self.flip:
            center_offset = 100
        else:
            center_offset = -100

        pygame_rect = pygame.Rect(
            pymunk_position[0] - (self.rect.width / 2) - center_offset,
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

        if self.display_text:
            text_surface = self.game.font.render(self.display_text, True, (255, 0, 0))
            screen.blit(text_surface, (200, 10)) 