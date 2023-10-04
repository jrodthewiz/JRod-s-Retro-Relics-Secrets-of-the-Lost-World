import pygame

import pymunk
import pymunk.pygame_util
import os
from OpenGL.GL import *
from OpenGL.GLU import *

from scripts.core.input_handler   import InputHandler
from scripts.core.texture_manager import AssetManager
from scripts.core.camera.camera   import Camera
from scripts.sprites.player       import Player
from scripts.sprites.enemy        import Enemy
from scripts.tiles.tile_map       import TileMap

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Retro Relics")

class Game:
    def __init__(self):
        self.screen           = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF, 8)
        self.running          = 1
        self.clock            = pygame.time.Clock()
        self.input_handler    = InputHandler(self) 
        self.texture_manager  = AssetManager()
        self.camera           = Camera(*self.screen.get_size())
        self.space            = pymunk.Space()
        self.shape_to_object_map = {}
        self.space.gravity    = (0, 1050) 
        self.space.damping    = 0.5 
        self.debug            = False
        self.font             = pygame.font.Font(None, 36)  
        self.bg_layers        = self.texture_manager.load_parallax_backgrounds('data/images/background/Parallax Forest Background - Blue')
        self.scroll_speeds    = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  
        self.scroll_positions = [0 for _ in range(len(self.bg_layers))] 
        self.options          = pymunk.pygame_util.DrawOptions(self.screen)
        self.mouse_dir        = pymunk.Vec2d(0, 0)
        player_scale_factor   = (0.5, 0.5)

        player_animation = self.texture_manager.load_animation("data/images/characters/player/idle", "idle", ".png", player_scale_factor)

         
        self.texture_manager.load_texture("data/images/tiles/gray/dirt.png", "tile_1" , (1, 1))
        self.texture_manager.load_texture("data/images/tiles/houses/house_1.png", "house_1" , (1, 1))
        self.texture_manager.load_texture("data/images/tiles/houses/house_2.png", "house_2" , (1, 1))
        self.texture_manager.load_texture("data/images/tiles/houses/house_3.png", "house_3" , (1, 1))
        self.texture_manager.load_texture("data/images/tiles/houses/house_4.png", "house_4" , (1, 1))
        self.texture_manager.load_texture("data/images/tiles/decorations/lamp_1.png", "lamp_1" , (1, 1))
        self.texture_manager.load_texture("data/images/tiles/decorations/bench_1.png", "bench_1" , (1, 1))
        self.texture_manager.load_texture("data/images/tiles/decorations/flowers_1.png", "flowers_1" , (1, 1))
        self.texture_manager.load_texture("data/images/tiles/decorations/flowers_2.png", "flowers_2" , (1, 1))


        self.texture_manager.load_animation("data/images/characters/player/run", "run", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/jump A", "jump_A", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/jump B", "jump_B", ".png", player_scale_factor)

        self.texture_manager.load_animation("data/images/characters/player/jab double", "jab_double", ".png", player_scale_factor)
        self.texture_manager.load_audio("data/sounds/punch/punch.wav", "jab_double_sound")

        self.texture_manager.load_animation("data/images/characters/player/jab high double", "jab_high", ".png", player_scale_factor)
        self.texture_manager.load_audio("data/sounds/punch/punch.wav", "jab_high_sound")

        self.texture_manager.load_animation("data/images/characters/player/kick low", "kick_low", ".png", player_scale_factor)
        self.texture_manager.load_audio("data/sounds/punch/punch.wav", "kick_low_sound")

        self.texture_manager.load_animation("data/images/characters/player/kick high", "kick_high", ".png", player_scale_factor)
        self.texture_manager.load_audio("data/sounds/punch/punch.wav", "kick_high_sound")

        self.texture_manager.load_animation("data/images/characters/player/reverse kick", "reverse_kick", ".png", player_scale_factor)
        self.texture_manager.load_audio("data/sounds/punch/punch.wav", "reverse_kick_sound")


        self.texture_manager.load_animation("data/images/characters/player/1_Sword/run", "sword_run", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/1_Sword/jump A", "sword_jump_A", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/1_Sword/jump B", "sword_jump_B", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/1_Sword/idle", "sword_idle", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/1_Sword/run stop", "sword_run_stop", ".png", player_scale_factor)
        self.texture_manager.load_audio("data/sounds/running_stop.wav", "sword_run_stop_sound")
        
        self.texture_manager.load_animation("data/images/characters/player/1_Sword/slash", "sword_slash", ".png", player_scale_factor)
        self.texture_manager.load_audio("data/sounds/weapons/slash.wav", "sword_slash_sound")

        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/run", "pistol_run", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/jump A", "pistol_jump_A", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/jump B", "pistol_jump_B", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/idle", "pistol_idle", ".png", player_scale_factor)

        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/run shoot", "pistol_run_shoot", ".png", player_scale_factor)

        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/run stop", "pistol_run_stop", ".png", player_scale_factor)
        self.texture_manager.load_audio("data/sounds/running_stop.wav", "pistol_run_stop_sound")

        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/shoot", "pistol_shoot", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/walk normal", "pistol_walk_normal", ".png", player_scale_factor)
        self.texture_manager.load_animation("data/images/characters/player/2_Pistol/walk shoot", "pistol_walk_shoot", ".png", player_scale_factor)


        player_position = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        player_collision_shape = player_animation[0].get_size()




        self.player = Player(self, self.texture_manager, player_position, player_collision_shape, player_scale_factor)
        
        
        self.player.add_animation("idle", frame_duration=50, loop=True)
        self.player.add_animation("run", frame_duration=25, loop=True)
        self.player.add_animation("jab_double", frame_duration=25, loop=True)
        self.player.add_animation("jab_high", frame_duration=25, loop=True)
        self.player.add_animation("kick_low", frame_duration=25, loop=False)
        self.player.add_animation("kick_high", frame_duration=25, loop=False)
        self.player.add_animation("reverse_kick", frame_duration=25, loop=False)
        self.player.add_animation("jump_A", frame_duration=25, loop=False)
        self.player.add_animation("jump_B", frame_duration=25, loop=False)
        
        
        self.player.add_animation("sword_jump_A", frame_duration=25, loop=False)
        self.player.add_animation("sword_jump_B", frame_duration=25, loop=False)
        self.player.add_animation("sword_run", frame_duration=25, loop=True)
        self.player.add_animation("sword_idle", frame_duration=25, loop=True)
        self.player.add_animation("sword_run_stop", frame_duration=25, loop=False)
        self.player.add_animation("sword_slash", frame_duration=25, loop=False)

        self.player.add_animation("pistol_run", frame_duration=25, loop=True)
        self.player.add_animation("pistol_jump_A", frame_duration=25, loop=False)
        self.player.add_animation("pistol_jump_B", frame_duration=25, loop=False)
        self.player.add_animation("pistol_idle", frame_duration=25, loop=True)
        self.player.add_animation("pistol_run_shoot", frame_duration=25, loop=True)
        self.player.add_animation("pistol_run_stop", frame_duration=25, loop=False)
        self.player.add_animation("pistol_shoot", frame_duration=25, loop=True)
        self.player.add_animation("pistol_walk_normal", frame_duration=25, loop=True)
        self.player.add_animation("pistol_walk_shoot", frame_duration=25, loop=True)

        self.player.set_collision_handler(self.space, self.player.shape.collision_type, 2) 
        self.player.add_to_space(self.space)

        enemy_position = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        enemy_collision_shape = player_animation[0].get_size()
        self.enemy = Enemy(self, self.texture_manager, enemy_position, enemy_collision_shape, (0.5, 0.5))
        self.enemy.add_animation("idle", frame_duration=50,  loop=True)
        self.enemy.add_animation("run",  frame_duration=25,  loop=True)
        self.enemy.set_collision_handler(self.space, self.enemy.shape.collision_type, 2) 
        self.enemy.add_to_space(self.space)

        tile_size = 600
        self.tile_map = TileMap(tile_size, self.texture_manager, self.player, self)
       
     

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

    def mouse_vector_crosshair(self):
        pymunk_player_pos = self.player.body.position
        camera_adjusted_player_pos = self.camera.apply((int(pymunk_player_pos[0]), int(pymunk_player_pos[1])))
        pygame_mouse_pos = pygame.mouse.get_pos()
        pygame_player_pos = self.pymunk_to_pygame_simple(camera_adjusted_player_pos)
        if self.debug:
            pygame.draw.line(self.screen, (255, 0, 0), pygame_player_pos, pygame_mouse_pos, 2)
        self.mouse_dir = (pygame_mouse_pos[0] - pygame_player_pos[0], pygame_mouse_pos[1] - pygame_player_pos[1])
        pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), 10)

    def update(self):
        #self.player.handle_input(self.input_handler)
        self.camera.update(self.player)
        self.player.update()
        self.enemy.update()
        self.tile_map.update(self.player.body.position)
        
        # Get the player's velocity
        player_velocity_x = self.player.body.velocity.x
        
        for i in range(len(self.scroll_positions)):
            # Use a scaling factor to control the relative speed of each layer
            scaling_factor = (i + 1) * 0.0005
            self.scroll_positions[i] -= player_velocity_x * scaling_factor

        # Ensure scroll positions loop back around once they go off screen
        self.scroll_positions = [
            pos % layer.get_width()
            for pos, layer in zip(self.scroll_positions, self.bg_layers)
        ]

    def render(self):
        #self.screen.fill((255, 255, 255))
        
        cam_x, cam_y = self.camera.camera.topleft
        
        for i, layer in enumerate(self.bg_layers):
            offset_x = cam_x * (i + 1) * 0.05
            effective_scroll_position = self.scroll_positions[i] - offset_x
            effective_scroll_position %= layer.get_width()

            self.screen.blit(layer, (effective_scroll_position - layer.get_width(), 0))
            self.screen.blit(layer, (effective_scroll_position, 0))

        self.tile_map.render(self.screen, self.camera)
        self.player.render(self.screen, self.camera)
        self.enemy.render(self.screen, self.camera)
        self.mouse_vector_crosshair()
        
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {int(fps)}", True, (255, 0, 0))
        self.screen.blit(fps_text, (10, 10))
        
        # self.space.debug_draw(self.options)
        pygame.display.flip()

    def run(self):
        while self.running:

             

            self.handle_events()
            self.space.step(1/60.0)
            self.update()
            self.render()
            self.clock.tick(60) 

            

