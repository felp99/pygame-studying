import pygame
import sys

from Game import Game
from Object import Object

class Player(Object):
    def __init__(self, x, y, width, height, color=(0, 128, 255)):
        super().__init__(x, y, width, height, color)

    def handle_input(self, keys):
        # Example: Move the player with arrow keys
        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0

        if keys[pygame.K_UP]:
            self.velocity.y = -5
        elif keys[pygame.K_DOWN]:
            self.velocity.y = 5
        else:
            self.velocity.y = 0

class TestGame(Game):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        super().setup()
        # Create a player object
        self.player = Player(100, 100, 30, 30)
        self.player2 = Player(100, 200, 30, 30)

        # Create a group to hold all game objects
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player2)

    def handle_events(self):
        super().handle_events()

        # Handle additional events specific to the game
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player2.handle_input(keys)

    def update(self):
        # Update all game objects
        self.all_sprites.update()

    def draw(self):
        # Draw all game objects
        self.screen.fill((255, 255, 255))  # Clear the screen
        self.all_sprites.draw(self.screen)

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        super().run()

if __name__ == "__main__":
    game = TestGame(800, 600, "Game with Objects")
    game.run()