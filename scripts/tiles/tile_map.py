import pygame
import pymunk
from scripts.tiles.tile       import Tile

# {
#     "tiles": [
#         {
#             "texture_name": "grass",
#             "is_solid": true,
#             "x": 0,
#             "y": 0
#         },
#         {
#             "texture_name": "water",
#             "is_solid": false,
#             "x": 1,
#             "y": 0
#         }
#     ]
# }

class TileMap:
    def __init__(self, width, height, tile_size, texture_manager):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = []
        self.space = pymunk.Space()  # physics space for pymunk
        self.player_previous_tile_x = None
        self.texture_manager = texture_manager

    def update(self, player_position):
        # Assuming player_position is a tuple of (x, y)
        player_tile_x = int(player_position[0] / self.tile_size)

        # Check if the player has moved to a new tile along the x-axis
        if self.player_previous_tile_x != player_tile_x:
            self.generate_tiles(player_tile_x)
            self.player_previous_tile_x = player_tile_x

    def generate_tiles(self, player_tile_x):
        # Define a range of tiles to generate based on player position
        start_x = player_tile_x - 10  # Generate 10 tiles behind player
        end_x = player_tile_x + 10  # Generate 10 tiles ahead of player

        # Remove or reuse tiles outside this range
        self.tiles = [tile for tile in self.tiles if start_x <= tile.x <= end_x]

        existing_tile_x_positions = {tile.x for tile in self.tiles}
        
        image = self.texture_manager.get_texture("tile_1")
        print(image)
        # Generate new tiles within the range
        for x in range(start_x, end_x + 1):
            if x not in existing_tile_x_positions:
                position = (x * self.tile_size, 0)  # Assuming ground level is at y=0
                # Assuming grass texture for simplicity, and all tiles are solid
                tile = Tile(image, True, position)
                self.tiles.append(tile)
                # Add to pymunk space if needed
                if tile.body and tile.shape:
                    self.space.add(tile.body, tile.shape)
    
    def load_from_json(self, file_path, texture_manager):
        import json

        with open(file_path, 'r') as f:
            data = json.load(f)
        
        for tile_data in data["tiles"]:
            texture = texture_manager.get_texture(tile_data["texture_name"])
            is_solid = tile_data["is_solid"]
            position = (tile_data["x"] * self.tile_size, tile_data["y"] * self.tile_size)
            tile = Tile(texture, is_solid, position)
            self.tiles.append(tile)
            
            # If tile has a physics object, add to pymunk space
            if tile.body and tile.shape:
                self.space.add(tile.body, tile.shape)
                
    def render(self, screen, camera_offset):
        for tile in self.tiles:
            tile.render(screen, camera_offset)
