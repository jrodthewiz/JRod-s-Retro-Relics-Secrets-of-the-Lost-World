import pygame
from pygame.locals import *



class Sprite:
    def __init__(self, texture_path):
        """Constructor for the Sprite class.

        Args:
        - texture_path (str): Path to the texture (image) for this sprite.
        """
        if texture_path is not None:
            self.texture = pygame.image.load(texture_path).convert_alpha()
        else:
            self.texture = None
        
    def render(self, screen, position):
        """Render the sprite on the screen at the given position.

        Args:
        - screen (pygame.Surface): The display surface to draw the sprite on.
        - position (tuple): A tuple containing the (x, y) position to draw the sprite.
        """

        if self.texture is not None:
            screen.blit(self.texture, position)

 