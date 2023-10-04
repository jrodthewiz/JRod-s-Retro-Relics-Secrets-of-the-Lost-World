import pygame
from pygame.locals import *



class Sprite:
    def __init__(self, texture_path):
        if texture_path is not None:
            self.texture = pygame.image.load(texture_path).convert_alpha()
        else:
            self.texture = None
        
    def render(self, screen, position, flip):
        if self.texture is not None:
            texture_to_render = pygame.transform.flip(self.texture, flip, False) if flip else self.texture
            screen.blit(texture_to_render, position)
            texture_rect = pygame.Rect(position, texture_to_render.get_size())
            if self.game.debug:
                pygame.draw.rect(screen, (255, 0, 0), texture_rect, 2)
    