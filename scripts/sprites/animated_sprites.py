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
        self.frame_duration = 10
        super().__init__(None)  # No initial texture

    def add_animation(self, animation_name):
        animation_frames = self.texture_manager.get_animation(animation_name)
        if animation_frames:
            self.animations[animation_name] = animation_frames

    def set_animation(self, animation_name):
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.current_frame = 0  # Reset to the first frame of the new animation
        else:
            print(f"No animation found with name: {animation_name}")

    def play_animation(self):
        if self.current_animation:
            now = pygame.time.get_ticks()
            elapsed_time = now - self.last_update

            if elapsed_time > self.frame_duration:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
                # Set the texture for the Sprite class to render
                self.texture = self.animations[self.current_animation][self.current_frame]

    def render(self, screen, position):
        # Update the current frame before rendering
        self.play_animation()
        super().render(screen, position)