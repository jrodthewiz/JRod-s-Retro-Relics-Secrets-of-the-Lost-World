import pygame
import pymunk

from scripts.core.input_handler   import InputHandler
from scripts.core.texture_manager import TextureManager
from scripts.core.camera.camera   import Camera
from scripts.sprites.player       import Player
from scripts.tiles.tile_map       import TileMap

pygame.init()
pygame.display.set_caption("Retro Relics")

space = pymunk.Space()
space.gravity = (0, -10) 


# Game Class
class Game:
    def __init__(self):
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.running = True
        self.clock           = pygame.time.Clock()
        self.input_handler   = InputHandler() 
        self.texture_manager = TextureManager()
        self.camera = Camera(*pygame.display.get_surface().get_size())  # Use screen dimensions for the camera

        
        # Load a texture.
        self.texture_manager.load_texture("data/images/tiles/gray/0.png", "tile_1")

        self.texture_manager.load_animation("data/images/characters/player/", "idle")
        # texture_manager.load_animation("path_to_textures/player_walk_right", "walk_right")
        # texture_manager.load_animation("path_to_textures/player_jump", "jump")
        # texture_manager.load_animation("path_to_textures/player_idle", "idle")

        player_position = (50, 50)
        player_collision_shape = (50, 100)
        self.player = Player(self.texture_manager, player_position, player_collision_shape)

        self.player.add_to_space(space)

        self.player.add_animation('idle')

        # Assuming each tile is 32x32 pixels and you want a 20x20 grid.
        tile_size = 32
        map_width = 20
        map_height = 20

        self.tile_map = TileMap(map_width, map_height, tile_size, self.texture_manager)
        # player.add_animation('walk_left')
        # player.add_animation('walk_right')
        # player.add_animation('jump')


    def handle_events(self):
        self.input_handler.poll()  

    def update(self):
        self.player.handle_input(self.input_handler)
        self.tile_map.update(self.player.body.position)
        self.player.update()
        self.camera.update(self.player)

    def render(self):
        self.screen.fill((255, 255, 255))
        self.player.render(self.screen, self.camera)  # Pass camera to player's render method
        self.tile_map.render(self.screen, self.camera.camera.topleft)  
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            space.step(1/60.0)
            self.update()
            self.render()
            self.clock.tick(60) 

