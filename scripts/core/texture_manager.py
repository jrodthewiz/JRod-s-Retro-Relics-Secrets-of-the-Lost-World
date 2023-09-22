import pygame
from pygame.locals import *


# texture_manager = TextureManager()

# # Load a texture.
# texture_manager.load_texture("path_to_file/image.png", "player_sprite")

# # Retrieve the loaded texture.
# player_texture = texture_manager.get_texture("player_sprite")

class TextureManager:
    def __init__(self):
        """Constructor for the TextureManager."""
        self.textures = {}  # Dictionary to store textures by name.

    def load_texture(self, file_path, name=None):
        """
        Load a texture from the given file path and store it by its name.
        
        Parameters:
        - file_path (str): Path to the texture file.
        - name (str): Name to store the texture under. If None, uses the filename without the extension.
        
        Returns:
        - pygame.Surface: The loaded texture.
        """
        # Load the texture into a pygame.Surface object.
        try:
            texture = pygame.image.load(file_path)
        except pygame.error as e:
            print(f"Error loading texture from {file_path}: {e}")
            return None

        # If name isn't given, use the filename without extension as the name.
        if name is None:
            name = file_path.split("/")[-1].split(".")[0]

        # Store the loaded texture in the dictionary.
        self.textures[name] = texture
        return texture

    def get_texture(self, name):
        """
        Retrieve a loaded texture by its name.
        
        Parameters:
        - name (str): The name of the texture to retrieve.
        
        Returns:
        - pygame.Surface: The texture associated with the given name or None if not found.
        """
        return self.textures.get(name, None)
