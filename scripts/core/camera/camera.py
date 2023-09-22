import pygame
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """ Translates the entity's position based on the camera's current position. """
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """ Translates a rectangle's position based on the camera's current position. """
        return rect.move(self.camera.topleft)

    def update(self, target):
        # Center the target in the camera view
        x = -target.body.position.x + int(self.width / 2)
        y = target.body.position.y - int(self.height / 2)  # Here, remove the negation

        self.camera = pygame.Rect(x, y, self.width, self.height)