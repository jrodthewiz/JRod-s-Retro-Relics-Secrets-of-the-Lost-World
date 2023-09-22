import pygame
from scripts.sprites import sprite

class AnimatedSprite(sprite):
    def __init__(self, folder_path, frame_duration):
        # Start with the first frame
        self.current_frame = 0
        self.frames = []
        self.load_from_folder(folder_path)

        # Duration each frame is shown for
        self.frame_duration = frame_duration
        self.last_update = pygame.time.get_ticks()

        # Initialize the parent class with the first frame
        super().__init__(self.frames[0])

    def load_from_folder(self, folder_path):
        # Assuming filenames are in the format: "walk_1.png", "walk_2.png", ...
        filenames = sorted(os.listdir(folder_path))
        for filename in filenames:
            path = os.path.join(folder_path, filename)
            self.frames.append(pygame.image.load(path))

    def play_animation(self):
        # Calculate the time since the last update
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update

        # If enough time has passed, go to the next frame
        if elapsed_time > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.texture = self.frames[self.current_frame]

    def render(self, screen, position):
        # Update the current frame before rendering
        self.play_animation()
        super().render(screen, position)