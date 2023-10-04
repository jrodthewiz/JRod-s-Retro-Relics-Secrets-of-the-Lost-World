import pygame
import pymunk

from scripts.sprites.animated_sprites import AnimatedSprite
from scripts.physics.physics_object import PhysicsObject
pygame.mixer.init()
class Player(AnimatedSprite, PhysicsObject):
    def __init__(self, game, texture_manager, position, collision_shape, player_scale_factor, body_type=pymunk.moment_for_circle):
        AnimatedSprite.__init__(self, texture_manager)
        PhysicsObject.__init__(self, position, collision_shape, body_type)
        self.collision_shape = collision_shape
        self.on_ground = False
        self.jump_strength = -600  
        self.move_speed = 1000 // 2
        self.in_air = False
        self.scale_factor = player_scale_factor
        self.flip = False
        self.rect = pygame.Rect(position[0], position[1], collision_shape[0], collision_shape[1])
        self.game = game
        print("Player: ", self, " Shape: ", self.shape, " Body: ", self.body)
        self.game.shape_to_object_map[self.shape] = self
        self.weapon = None
        self.jumps_made = 0
        self.max_jumps = 10  # Allow double jump
        self.was_moving = False
        self.display_text = None
        self.jump_animation_playing = False

    def render_text_on_screen(self, text):
        """Updates the display text buffer."""
        self.display_text = text

    def handle_input(self, input_handler):
        velocity_x = 0
        velocity_y = self.body.velocity.y
        moving = False
        combat_animation_set = False
        if self.in_air == False:
            self.jump_animation_playing = False
            self.jumps_made = 0   # Reset the jump count when the character is not in the air
            
        
        # Movement
        if input_handler.key_states.get(pygame.K_a, False) or input_handler.key_states.get(pygame.K_LEFT, False):
            velocity_x = -self.move_speed
            moving = True
            self.flip = True
            self.display_text = "Moving to the left"
        elif input_handler.key_states.get(pygame.K_d, False) or input_handler.key_states.get(pygame.K_RIGHT, False):
            velocity_x = self.move_speed
            moving = True
            self.flip = False
            self.display_text = "Moving to the right"
        
        

        # Weapon Toggle
        if input_handler.key_states.get(pygame.K_8, False):
            self.weapon = None
            self.display_text = "No weapon"
        elif input_handler.key_states.get(pygame.K_9, False):
            self.weapon = "sword"
            self.display_text = "sword"
        elif input_handler.key_states.get(pygame.K_0, False):
            self.weapon = "pistol"
            self.display_text = "pistol"

        
        # Combat Animations
        if input_handler.key_states.get(pygame.K_q, False) and self.weapon == "sword":
            self.set_animation("sword_slash")
            self.display_text = "sword_slash"
            combat_animation_set = True
            return
        elif input_handler.key_states.get(pygame.K_e, False) and self.weapon == "pistol":
            True# self.set_animation("pistol_walk_shoot" if self.was_moving else "pistol_shoot")
            # if self.was_moving:
            #     self.display_text = "pistol_walk_shoot"
            # else:
            #     self.display_text = "pistol_shoot"
            # return
        elif input_handler.key_states.get(pygame.K_1, False):
            self.set_animation("jab_double")
            self.display_text = "jab_double"
            combat_animation_set = True
            return
        elif input_handler.key_states.get(pygame.K_2, False):
            self.set_animation("jab_high")
            self.display_text = "jab_high"
            combat_animation_set = True
            return
        elif input_handler.key_states.get(pygame.K_3, False):
            self.set_animation("kick_low")
            self.display_text = "kick_low"
            combat_animation_set = True
            return
        elif input_handler.key_states.get(pygame.K_4, False):
            self.set_animation("kick_high")
            self.display_text = "kick_high"
            combat_animation_set = True
            return
        elif input_handler.key_states.get(pygame.K_5, False):
            self.set_animation("reverse_kick")
            self.display_text = "reverse_kick"
            combat_animation_set = True
            return

        if not combat_animation_set:
            # Jump
            jump_key_is_pressed = input_handler.key_states.get(pygame.K_w, False) or input_handler.key_states.get(pygame.K_SPACE, False)
            if jump_key_is_pressed and self.jumps_made < self.max_jumps:
                velocity_y = self.jump_strength
                self.jumps_made += 1
                self.display_text = "Jumping"
                if self.jumps_made == 1:
                    anim_map = {
                        None: "jump_A",
                        "sword": "sword_jump_A",
                        "pistol": "pistol_jump_A"
                    }
                    self.set_animation(anim_map.get(self.weapon))
                else:
                    anim_map = {
                        None: "jump_B",
                        "sword": "sword_jump_B",
                        "pistol": "pistol_jump_B"
                    }
                    self.set_animation(anim_map.get(self.weapon))

                self.jump_animation_playing = True
                self.in_air = True  # This ensures that after the jump, the character is recognized as being in the air

            # Animation based on movement and weapon
            elif moving and not self.in_air:
                
                anim_map = {
                    None: "run",
                    "sword": "sword_run",
                    "pistol": "pistol_run"
                }


                if input_handler.key_states.get(pygame.K_e, False) and self.weapon == "pistol":
                    self.set_animation("pistol_run_shoot")
                else:
                    self.set_animation(anim_map.get(self.weapon))
                    
            elif not moving:
                if self.was_moving and not self.in_air:
                    anim_map = {
                        None: "run_stop",
                        "sword": "sword_run_stop",
                        "pistol": "pistol_run_stop"
                    }
                    self.set_animation(anim_map.get(self.weapon))
                    self.display_text = "Running stop"
                elif not self.in_air:
                    anim_map = {
                        None: "idle",
                        "sword": "sword_idle",
                        "pistol": "pistol_idle"
                    }
                    self.set_animation(anim_map.get(self.weapon))
                    self.display_text = "Idling"

        self.body.velocity = pymunk.Vec2d(velocity_x, velocity_y)
        self.was_moving = moving


    


    def update(self):
        self.body.angle = 0
        self.rect.x = self.body.position.x - self.rect.width  / 2
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