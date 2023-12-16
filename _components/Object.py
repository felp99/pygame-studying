import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        super().__init__()

        # Create a surface for the object
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # Set the initial position
        self.rect.x = x
        self.rect.y = y

        # Set initial velocity (can be modified during updates)
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        # Update the position based on velocity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

class Player(Object):
    def __init__(self, x, y, width, height, color=(0, 128, 255)):
        super().__init__(x, y, width, height, color)

    def handle_input(self, keys):
        # Override this method to handle player input
        pass