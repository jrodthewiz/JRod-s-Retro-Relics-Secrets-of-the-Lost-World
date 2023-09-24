import pygame
from scripts.sprites.sprite import Sprite
import os as os 
class AnimatedSprite(Sprite):
    def __init__(self, texture_manager):
        self.texture_manager = texture_manager
        self.animations = {}  # Dictionary to hold animations
        self.current_animation = None
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = 40
        self.playing = False
        self.one_shot_playing = False
        super().__init__(None)  # No initial texture

    def switch_animation(self, animation_name):
        # Only switch if the new animation is different from the current one
        if animation_name != self.current_animation and animation_name in self.animations:
            self.set_animation(animation_name)


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
            if self.current_animation != animation_name or (is_one_shot and not self.one_shot_playing):
                self.current_animation = animation_name
                self.current_frame = 0  # Reset to the first frame of the new animation
                self.playing = True
                self.one_shot_playing = is_one_shot  # Set flag if it's a one-shot animation






    def play_animation(self):
        if self.current_animation and self.playing:
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
                else:
                    self.current_frame += 1

                # Set the texture for the Sprite class to render
                self.texture = self.animations[self.current_animation]['frames'][self.current_frame]





    def render(self, screen, position, flip):
        # Update the current frame before rendering
        self.play_animation()
        super().render(screen, position, flip)