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
        """ Adjust camera position based on the target (usually the player). """

        # Center the target in the camera view
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Bound the camera to the level size
        x = min(0, x)                            # Left
        y = min(0, y)                            # Top
        x = max(-(target.level.width - self.width), x)    # Right
        y = max(-(target.level.height - self.height), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)
