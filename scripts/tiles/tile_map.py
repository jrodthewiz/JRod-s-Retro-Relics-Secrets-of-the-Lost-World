class TileMap:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = []
        self.space = pymunk.Space()  # physics space for pymunk
    
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
