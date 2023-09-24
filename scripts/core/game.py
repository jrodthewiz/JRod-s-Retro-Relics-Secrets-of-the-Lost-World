import pygame
import pymunk

from scripts.core.input_handler   import InputHandler
from scripts.core.texture_manager import TextureManager
from scripts.core.camera.camera   import Camera
from scripts.sprites.player       import Player
from scripts.tiles.tile_map       import TileMap
import pymunk.pygame_util

pygame.init()
pygame.display.set_caption("Retro Relics")




# Game Class
class Game:
    def __init__(self):
        self.screen          = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.running         = True
        self.clock           = pygame.time.Clock()
        self.input_handler   = InputHandler() 
        self.texture_manager = TextureManager()
        self.camera          = Camera(*self.screen.get_size())  # Use screen dimensions for the camera
        self.space           = pymunk.Space()
        self.space.gravity   = (0, 900)  #90
        self.space.damping   = 0.9 
        self.debug           = False

        self.texture_manager.load_texture("data/images/tiles/gray/0.png", "tile_1" , (1, 1))

        player_scale_factor = (0.5, 0.5)

        idle_animation = self.texture_manager.load_animation("data/images/characters/player/idle", "idle", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/run", "run", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/jump A", "jump", ".png", player_scale_factor)

        self.texture_manager.load_animation("data/images/characters/player/jab double", "jab_double", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/jab high double", "jab_high", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/kick low", "kick_low", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/kick high", "kick_high", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/reverse kick", "reverse_kick", ".png", player_scale_factor)

        player_position = (self.screen.get_width()/2, self.screen.get_height()/2)

        first_frame = idle_animation[0]

        player_collision_shape = first_frame.get_size()
        #player_collision_shape = (player_collision_shape[0] * player_scale_factor[0], player_collision_shape[1] * player_scale_factor[1]) 

        self.player = Player(self, self.texture_manager, player_position, player_collision_shape, player_scale_factor)
        self.player.add_animation("idle", frame_duration=50, loop=True)
        self.player.add_animation("run", frame_duration=25, loop=True)
        self.player.add_animation("jab_double", frame_duration=25, loop=False)
        self.player.add_animation("jab_high", frame_duration=25, loop=False)
        self.player.add_animation("kick_low", frame_duration=25, loop=False)
        self.player.add_animation("kick_high", frame_duration=25, loop=False)
        self.player.add_animation("reverse_kick", frame_duration=25, loop=False)
        self.player.add_animation("jump", frame_duration=100, loop=False)


        self.player.set_collision_handler(self.space, self.player.shape.collision_type, 2) 
        self.player.add_to_space(self.space)
        
        self.mouse_dir = pymunk.Vec2d(0, 0)

        tile_size = 600
        self.tile_map = TileMap(tile_size, self.texture_manager, self.player, self)

        self.options = pymunk.pygame_util.DrawOptions(self.screen)


    def pymunk_to_pygame_simple(self, pymunk_coords):
        return (
            pymunk_coords[0],
            self.screen.get_height() - pymunk_coords[1]
        )

    def pygame_to_pymunk_simple(self, pygame_coords):
        return (
            pygame_coords[0],
            self.screen.get_height() - pygame_coords[1]
        )

    def handle_events(self):
        self.input_handler.poll()  

    def draw_line_to_mouse(self):
        pymunk_player_pos = self.player.body.position
        camera_adjusted_player_pos = self.camera.apply((int(pymunk_player_pos[0]), int(pymunk_player_pos[1])))
        pygame_mouse_pos = pygame.mouse.get_pos()
        pygame_player_pos = self.pymunk_to_pygame_simple(camera_adjusted_player_pos)
        if self.debug:
            pygame.draw.line(self.screen, (255, 0, 0), pygame_player_pos, pygame_mouse_pos, 2)
        self.mouse_dir = (pygame_mouse_pos[0] - pygame_player_pos[0], pygame_mouse_pos[1] - pygame_player_pos[1])

    def update(self):
        self.player.handle_input(self.input_handler)
        self.camera.update(self.player)
        self.player.update() 
        self.tile_map.update(self.player.body.position)

    def render(self):
        self.screen.fill((255, 255, 255))
        self.tile_map.render(self.screen, self.camera)
        self.player.render(self.screen, self.camera)  
        self.draw_line_to_mouse()
        pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), 10)
        #self.space.debug_draw(self.options)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.space.step(1/60.0)
            self.update()
            self.render()
            self.clock.tick(60) 

