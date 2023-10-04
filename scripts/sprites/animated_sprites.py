import pygame
from scripts.sprites.sprite import Sprite
import os as os 
class AnimatedSprite(Sprite):
    def __init__(self, texture_manager):
        self.texture_manager = texture_manager
        self.animations = {}  
        self.current_animation = None
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = 40
        self.playing = False
        self.one_shot_playing = False
        super().__init__(None)  

    def add_animation(self, animation_name, frame_duration=40, loop=True):
        animation_frames = self.texture_manager.get_animation(animation_name)
        if animation_frames:
            self.animations[animation_name] = {
                'frames': animation_frames, 
                'frame_duration': frame_duration,
                'loop': loop
            }

    def set_animation(self, animation_name):
        if animation_name in self.animations:
            is_one_shot = not self.animations[animation_name]['loop']
            # Only change the animation if it's different from the current one
            if self.current_animation != animation_name:
                # Don't interrupt a playing one-shot animation
                if self.one_shot_playing:
                    return

                self.current_animation = animation_name
                self.current_frame = 0
                self.playing = True
                self.one_shot_playing = is_one_shot

        

    def play_animation(self):
        if not self.playing:
            return

        if self.current_animation:
            now = pygame.time.get_ticks()
            elapsed_time = now - self.last_update
            frame_duration = self.animations[self.current_animation]['frame_duration']

            if elapsed_time > frame_duration:
                self.last_update = now
                if self.current_frame == len(self.animations[self.current_animation]['frames']) - 1:
                    # If at the end of the animation
                    if self.animations[self.current_animation]['loop']:
                        self.current_frame = 0
                    else:
                        self.playing = False
                        self.one_shot_playing = False
                        if not self.playing and self.current_animation in ["jump", "sword_jump", "pistol_jump"]:
                            self.jump_animation_playing = False
                else:
                    self.current_frame += 1

                self.texture = self.animations[self.current_animation]['frames'][self.current_frame]
                

        # Handle one-shot animations
        if self.one_shot_playing and not self.playing:
            # Transition to the appropriate movement or idle state
            if self.was_moving:
                self.set_state_animation("move_right" if self.flip else "move_left", True)
            else:
                self.set_state_animation("idle", False)
            self.one_shot_playing = False

        
    def render(self, screen, position, flip):
        self.play_animation()
        super().render(screen, position, flip)