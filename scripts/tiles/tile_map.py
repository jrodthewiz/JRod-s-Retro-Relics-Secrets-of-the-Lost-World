import pygame
import pymunk
import random
from scripts.tiles.tile import Tile
import noise


class TileMap:
    def __init__(self, tile_size, texture_manager, player, game):
        self.tile_size = tile_size
        self.tiles = {}
        self.texture_manager = texture_manager
        self.player = player
        self.game = game
        self.player_previous_tile_x = None
        self.initial_y = self.player.body.position[1]

    def update(self, player_position):

        player_tile_x = int(player_position[0] / self.tile_size)

        if self.player_previous_tile_x != player_tile_x:
            self.generate_tiles(player_tile_x)
            self.player_previous_tile_x = player_tile_x

        self.remove_offscreen_tiles(self.game.camera)

    def should_place_decoration(self, x, bottom_tile_coordinate):
        if self.is_tile_occupied(x, bottom_tile_coordinate // self.tile_size - 1):
            return False
        return x % 1 == 0

    def should_place_house(self, x, bottom_tile_coordinate):
        if self.is_tile_occupied(x, bottom_tile_coordinate // self.tile_size - 1):
            return False
        return x % 3 == 0
    
    def is_tile_occupied(self, x, y):
        return (x, y) in self.tiles
    
    def generate_house(self, x, tile_key, position):
        house_position = (position[0], position[1] - self.tile_size)
        house_key = (x, tile_key[1] - 1)
        
        house_image = self.texture_manager.get_texture("house_1")
        house_image_red = self.texture_manager.get_texture("house_2")
        house_image_3 = self.texture_manager.get_texture("house_3")
        house_image_4 = self.texture_manager.get_texture("house_4")
        selected_house_image = random.choice([house_image, house_image_red, house_image_3, house_image_4])

        house_tile = Tile(selected_house_image, False, house_position, self.game)
        self.tiles[house_key] = house_tile
    
    def generate_decoration(self, x, tile_key, position):
        decoration_position = (position[0], position[1] - self.tile_size)
        decoration_key = (x, tile_key[1] - 1)
        
        lamp = self.texture_manager.get_texture("lamp_1")
        bench = self.texture_manager.get_texture("bench_1")
        flowers1 = self.texture_manager.get_texture("flowers_1")
        flowers2 = self.texture_manager.get_texture("flowers_2")
        selected_decoration = random.choice([lamp, bench, flowers1, flowers2])

        decoration_tile = Tile(selected_decoration, False, decoration_position, self.game)
        self.tiles[decoration_key] = decoration_tile

    def generate_tiles(self, player_tile_x):
        tile_range = 5
        start_x = player_tile_x - tile_range   
        end_x   = player_tile_x + tile_range    

        image = self.texture_manager.get_texture("tile_1")

        # Generate new tiles within the horizontal range
        for x in range(start_x, end_x + 1):
            noise_value = noise.pnoise2(x / 10.0, 0, octaves=8, persistence=0.5, lacunarity=2.0, repeatx=1024, base=42)
            # Convert noise value to a useful y-coordinate value
            tile_y = int((noise_value + 1) * 1050 + self.initial_y)  # adjust as needed
            #print("Perlin Y-Coordinate: ", tile_y)
            
            tile_key = (x, tile_y // self.tile_size)
            
            if tile_key not in self.tiles:
                position = (x * self.tile_size, tile_y)
                tile = Tile(image, True, position, self.game)
                self.tiles[tile_key] = tile

                if self.should_place_house(x, tile_y):
                    self.generate_house(x, tile_key, position)

                if self.should_place_decoration(x, tile_y):
                    self.generate_decoration(x, tile_key, position)

        
    def generate_flat_tiles(self, player_tile_x):
        tile_range = 10
        start_x = player_tile_x - tile_range   
        end_x   = player_tile_x + tile_range    

        tile_y = self.initial_y + 300  
        image = self.texture_manager.get_texture("tile_1")

        for x in range(start_x, end_x + 1):
            tile_key = (x, tile_y // self.tile_size)
            
            if tile_key not in self.tiles:
                position = (x * self.tile_size, tile_y)
                tile_position = position
                tile = Tile(image, True, tile_position, self.game)
                self.tiles[tile_key] = tile

    def remove_offscreen_tiles(self, camera):
        buffer = 4  # Number of tiles to keep around the screen, adjust as needed
        
        # Convert camera rectangle to world coordinates
        start_x_world = camera.camera.x - buffer * self.tile_size  
        end_x_world = camera.camera.x + camera.camera.width + buffer * self.tile_size  
        start_y_world = camera.camera.y - buffer * self.tile_size  
        end_y_world = camera.camera.y + camera.camera.height + buffer * self.tile_size  
        
        # Convert world coordinates to tile coordinates
        start_tile_x = start_x_world // self.tile_size
        end_tile_x = end_x_world // self.tile_size
        
        start_tile_y = start_y_world // self.tile_size
        end_tile_y = end_y_world // self.tile_size
        
        # Identify keys of offscreen tiles
        keys_to_remove = [
            key for key in self.tiles 
            if not (start_tile_x <= key[0] <= end_tile_x and start_tile_y <= key[1] <= end_tile_y)
        ]
        
        # Remove offscreen tiles from the dictionary
        for key in keys_to_remove:
            if self.tiles[key].body and self.tiles[key].shape:  # Check if the tile has associated pymunk objects
                self.game.space.remove(self.tiles[key].body, self.tiles[key].shape) 
            del self.tiles[key]

    def render(self, screen, camera):
        for tile in self.tiles.values():
            tile.render(screen, camera)