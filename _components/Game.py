import pygame
import sys

class Game:
    def __init__(self, width, height, title):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = width, height
        self.FPS = 60

        # Initialize the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        # Font for displaying FPS
        self.font = pygame.font.SysFont(None, 30)

        # Initialize game-specific attributes
        self.setup()

    def setup(self):
        # Override this method in your specific game class for setup
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def update(self):
        # Override this method in your specific game class for updating game logic
        pass

    def draw(self):
        # Override this method in your specific game class for drawing on the screen
        pass

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()

            # Refresh the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.FPS)
            
class SnakeGame(Game):
    def setup(self):
        # Game-specific setup code goes here
        pass

    def handle_events(self):
        super().handle_events()
        # Game-specific event handling code goes here
        pass

    def update(self):
        super().update()
        # Game-specific update logic goes here
        pass

    def draw(self):
        super().draw()
        # Game-specific drawing code goes here
        pass


if __name__ == "__main__":
    # Create and run the SnakeGame
    snake_game = SnakeGame(800, 600, "Snake Game")
    snake_game.run()
