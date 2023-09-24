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
        
    def render(self, screen, position, flip):
        """Render the sprite on the screen at the given position.

        Args:
        - screen (pygame.Surface): The display surface to draw the sprite on.
        - position (tuple): A tuple containing the (x, y) position to draw the sprite.
        """

        if self.texture is not None:
            # Flip the texture horizontally if flip is True
            texture_to_render = pygame.transform.flip(self.texture, flip, False) if flip else self.texture
            #print("Rendering size: ", texture_to_render.get_size())
            screen.blit(texture_to_render, position)
            texture_rect = pygame.Rect(position, texture_to_render.get_size())
            #pygame.draw.rect(screen, (255, 0, 0), texture_rect, 2)
    