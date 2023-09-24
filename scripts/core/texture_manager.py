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

    def load_texture(self, file_path, name, scale_factor):
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

        if name is None:
            name = file_path.split("/")[-1].split(".")[0]

        scaled_texture = pygame.transform.scale(texture, (int(texture.get_width() * scale_factor[0]), int(texture.get_height() * scale_factor[1])))
        self.textures[name] = scaled_texture
        return scaled_texture
    
    def load_animation(self, folder_path, animation_name, frame_extension, scale_factor):
        """
        Load a collection of frames from the given folder path and store it under animation_name.

        Parameters:
        - folder_path (str): Path to the folder containing the frames.
        - animation_name (str): Name to store the animation under.
        - frame_extension (str): Extension of the frame files (assuming all frames have the same extension).
        - scale_factor (tuple): A tuple containing the scaling factor for the width and height of the frames.
        
        Returns:
        - list: A list of pygame.Surface objects representing the frames of the animation.
        """
        # List the files in the folder and filter by the specified extension
        filenames = [f for f in os.listdir(folder_path) if f.endswith(frame_extension)]

        frames = []
        for filename in filenames:
            # Construct the full path to the file
            full_path = os.path.join(folder_path, filename)
            
            # Load the image once
            image = pygame.image.load(full_path)
            
            # Scale the image
            width, height = image.get_size()
            scaled_image = pygame.transform.scale(
                image, 
                (int(width * scale_factor[0]), int(height * scale_factor[1]))
            )
            
            # Append the scaled image to the frames list
            frames.append(scaled_image)
        
        # Store the frames list in the animations dictionary
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
