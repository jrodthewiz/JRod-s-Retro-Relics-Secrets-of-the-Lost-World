import pygame
import pymunk
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
        #print(f"Player position: {player_position}")

        player_tile_x = int(player_position[0] / self.tile_size)


        if self.player_previous_tile_x != player_tile_x:
            self.generate_tiles(player_tile_x)
            self.player_previous_tile_x = player_tile_x

        self.remove_offscreen_tiles(self.game.camera)

    def generate_tiles(self, player_tile_x):
        tile_range = 10
        start_x = player_tile_x - tile_range   
        end_x   = player_tile_x + tile_range    

        image = self.texture_manager.get_texture("tile_1")

        # Generate new tiles within the horizontal range
        for x in range(start_x, end_x + 1):
            noise_value = noise.pnoise2(x / 10.0, 0, octaves=4, persistence=0.5, lacunarity=2.0, repeatx=1024, base=42)
            # Convert noise value to a useful y-coordinate value
            tile_y = int((noise_value + 1) * 2050 + self.initial_y)  # adjust as needed
            #print("Perlin Y-Coordinate: ", tile_y)
            
            tile_key = (x, tile_y // self.tile_size)
            
            if tile_key not in self.tiles:
                position = (x * self.tile_size, tile_y)
                tile = Tile(image, True, position, self.game)
                self.tiles[tile_key] = tile
        
    def generate_flat_tiles(self, player_tile_x):
        tile_range = 10
        start_x = player_tile_x - tile_range   
        end_x   = player_tile_x + tile_range    

        #print(f"Tile generation range: start_x: {start_x}, end_x: {end_x}")

        tile_y = self.initial_y + 300  # Assuming y=0 represents ground level, adjust as necessary

        image = self.texture_manager.get_texture("tile_1")

        # Generate new tiles within the horizontal range
        for x in range(start_x, end_x + 1):
            tile_key = (x, tile_y // self.tile_size)
            
            if tile_key not in self.tiles:
                #print("Tile key: ", tile_key)
                position = (x * self.tile_size, tile_y)
                tile_position = position#self.game.pymunk_to_pygame(, self.game.camera)  #position  #self.game.pymunk_to_pygame(position, self.game.camera)
                #print("Tile position: ", tile_position)
                tile = Tile(image, True, tile_position, self.game)
                self.tiles[tile_key] = tile

    def render(self, screen, camera):
        for tile in self.tiles.values():
            tile.render(screen, camera)
            #print(f"Rendering tile at position: {tile.position}")

    def remove_offscreen_tiles(self, camera):
        buffer = 4  # Number of tiles to keep around the screen, adjust as needed
        
        # Convert camera rectangle to world coordinates
        start_x_world = camera.camera.x - buffer * self.tile_size  # Added buffer here
        end_x_world = camera.camera.x + camera.camera.width + buffer * self.tile_size  # Added buffer here
        
        start_y_world = camera.camera.y - buffer * self.tile_size  # Added buffer here
        end_y_world = camera.camera.y + camera.camera.height + buffer * self.tile_size  # Added buffer here
        
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
            #print("Removed: ", key)
            del self.tiles[key]


