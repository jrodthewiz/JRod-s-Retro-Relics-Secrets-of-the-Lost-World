import pygame
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)#pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    # def apply(self, entity):
    #     """ Translates the entity's position based on the camera's current position. """
    #     return entity.rect.move(self.camera.topleft)
    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        elif isinstance(entity, tuple):
            return (entity[0] - self.camera.topleft[0], entity[1] - self.camera.topleft[1])
        else:
            raise TypeError(f"Unsupported type {type(entity)} passed to Camera.apply")

    def apply_rect(self, rect):
        return pygame.Rect(
            rect.x - self.camera.x,
            rect.y - self.camera.y,
            rect.width,
            rect.height
        )

    def update(self, target):
        x = (target.body.position.x - int(self.width / 2))
        y = (target.body.position.y - int(self.height / 2))  # Changed sign from - to +
        self.camera = pygame.Rect(x, y, self.width, self.height)
