import pygame
from pygame.locals import *
import os as os

# texture_manager = TextureManager()

# # Load a texture.
# texture_manager.load_texture("path_to_file/image.png", "player_sprite")

# # Retrieve the loaded texture.
# player_texture = texture_manager.get_texture("player_sprite")

class TextureManager:
    def __init__(self):
        """Constructor for the TextureManager."""
        self.textures = {}  # Dictionary to store single textures by name.
        self.animations = {}  # Dictionary to store collections of frames by animation name.

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
    
    def load_animation(self, folder_path, animation_name, frame_extension=".png"):
        """
        Load a collection of frames from the given folder path and store it by animation name.

        Parameters:
        - folder_path (str): Path to the folder containing the frames.
        - animation_name (str): Name to store the animation under.
        - frame_extension (str): Extension of the frame files (assuming all frames have the same extension).

        Returns:
        - list: A list of pygame.Surface objects representing the frames of the animation.
        """
        filenames = sorted([f for f in os.listdir(folder_path) if f.endswith(frame_extension)])
        for file in filenames:
            print(file)
        frames = [pygame.image.load(os.path.join(folder_path, filename)) for filename in filenames]
        self.animations[animation_name] = frames
        return frames

    def get_animation(self, animation_name):
        """
        Retrieve a loaded animation by its name.

        Parameters:
        - animation_name (str): The name of the animation to retrieve.

        Returns:
        - list: A list of pygame.Surface objects representing the frames of the animation or None if not found.
        """
        return self.animations.get(animation_name, None)
    

    def get_texture(self, name):
        """
        Retrieve a loaded texture by its name.
        
        Parameters:
        - name (str): The name of the texture to retrieve.
        
        Returns:
        - pygame.Surface: The texture associated with the given name or None if not found.
        """
        return self.textures.get(name, None)
