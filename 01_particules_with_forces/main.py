import pygame
import sys
import random
import numpy as np
import math
from math import pi

        # Constants
WIDTH, HEIGHT = int(800), int(600)
FPS = 60
NEW_PARTICLE_INTERVAL = 100000
GRAVITY_CONSTANT = 0.00000001
GRAVITY_VECTOR = 1
COLORS = ['red', 'blue', 'green']
RADIUS=30
COLLISION_RADIUS=5
PARTICLE_SIZE = (COLLISION_RADIUS,COLLISION_RADIUS)
PI=pi
RANDOM_VECTOR = 2.5
PARTICLES=100

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Initialize the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Particle Simulation")
        self.clock = pygame.time.Clock()

        # Create a group to hold all particles
        self.all_particules = pygame.sprite.Group()

        # Font for displaying FPS
        self.font = pygame.font.SysFont(None, 30)
        
        # Time variables for particle spawning
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_particle_interval = NEW_PARTICLE_INTERVAL

        self.init_spawn_particles()
            
    def init_spawn_particles(self):
        for i in range(PARTICLES):
            self.spawn_particle() 
        pass

    def spawn_particle(self):
        particle = Particle(x=random.randint(0, WIDTH), 
                            y=random.randint(0, HEIGHT))
        self.all_particules.add(particle)

    def has_collided(self, particle1, particle2):
        distance = math.sqrt((particle1.rect.center[0] - particle2.rect.center[0]) ** 2 +
                             (particle1.rect.center[1] - particle2.rect.center[1]) ** 2)
        return distance < 10

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()

            # Refresh the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(FPS)

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def update(self):
        # Check for spawning a new particle
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_particle_interval:
            self.spawn_particle()
            self.last_spawn_time = current_time  # Reset the last spawn time

        # Update
        for particle in self.all_particules:
            particle.update(self.all_particules)

        # Check for collisions between particles
        for particle1 in self.all_particules:
            for particle2 in self.all_particules:
                if particle1 != particle2 and self.has_collided(particle1, particle2):
                    #print("Collision!")
                    pass

    def draw(self):
        # Draw
        self.screen.fill('white')        
        self.all_particules.draw(self.screen)
        
        # Draw paths
        for particle in self.all_particules:
            pygame.draw.lines(surface=self.screen, 
                              color='grey', closed=False, 
                              points=particle.path)
            pygame.draw.circle(self.screen, 
                               color=(0,0,0), 
                               center=pygame.Vector2(particle.rect.x, particle.rect.y), 
                               radius=int(RADIUS/2), 
                               width=1)
            self.draw_arrow(surface=self.screen, 
                            start=pygame.Vector2(particle.rect.x, particle.rect.y), 
                            end=pygame.Vector2(particle.rect.x  + math.cos(particle.gravity_direction) * RADIUS, 
                                               particle.rect.y  + math.sin(particle.gravity_direction) * RADIUS), 
                            color=particle.color, 
                            body_width=1,
                            head_height=5, 
                            head_width=5)
            self.draw_arrow(surface=self.screen, 
                            start=pygame.Vector2(particle.rect.x, particle.rect.y), 
                            end=pygame.Vector2(particle.rect.x  + math.cos(particle.random_direction)*RADIUS, 
                                               particle.rect.y  + math.sin(particle.random_direction)*RADIUS), 
                            color='grey', 
                            body_width=1,
                            head_height=5, 
                            head_width=5)
            self.draw_arrow(surface=self.screen, 
                            start=pygame.Vector2(particle.rect.x, particle.rect.y), 
                            end=pygame.Vector2(particle.rect.x  + math.cos(particle.repulsion_direction)*RADIUS, 
                                               particle.rect.y  + math.sin(particle.repulsion_direction)*RADIUS), 
                            color=particle.color, 
                            body_width=1,
                            head_height=5, 
                            head_width=5)
            pass

        # Display FPS
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())} P:{int(len(self.all_particules))}", True, (0, 0, 0))
        self.screen.blit(fps_text, (WIDTH - 150, 10))
        
    def draw_arrow(
        self,
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 2,
        head_width: int = 4,
        head_height: int = 2,
    ):
        """Draw an arrow between start and end with the arrow head at the end.

        Args:
            surface (pygame.Surface): The surface to draw on
            start (pygame.Vector2): Start position
            end (pygame.Vector2): End position
            color (pygame.Color): Color of the arrow
            body_width (int, optional): Defaults to 2.
            head_width (int, optional): Defaults to 4.
            head_height (float, optional): Defaults to 2.
        """
        arrow = start - end
        angle = arrow.angle_to(pygame.Vector2(0, -1))
        body_length = arrow.length() - head_height

        # Create the triangle head around the origin
        head_verts = [
            pygame.Vector2(0, head_height / 2),  # Center
            pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
            pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
        ]
        # Rotate and translate the head into place
        translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
        for i in range(len(head_verts)):
            head_verts[i].rotate_ip(-angle)
            head_verts[i] += translation
            head_verts[i] += start

        pygame.draw.polygon(surface, color, head_verts)

        # Stop weird shapes when the arrow is shorter than arrow head
        if arrow.length() >= head_height:
            # Calculate the body rect, rotate and translate into place
            body_verts = [
                pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
                pygame.Vector2(body_width / 2, body_length / 2),  # Topright
                pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
                pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
            ]
            translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
            for i in range(len(body_verts)):
                body_verts[i].rotate_ip(-angle)
                body_verts[i] += translation
                body_verts[i] += start

            pygame.draw.polygon(surface, color, body_verts)

# Particle class
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(PARTICLE_SIZE, pygame.SRCALPHA)
        self.color = random.choice(COLORS)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.path = [self.rect.center]
        self.speed = 1
        
        self.gravity_direction = 0
        self.random_direction = 0
        self.repulsion_direction =0

    def update(self, all_particles):
        
        self.edge_limit()
        self.gravity_force(all_particles)
        self.repulsion_force(all_particles)
        self.random_force()
        
        self.path.pop(0) if len(self.path) > 100 else self.path.append(self.rect.center)
            
    def edge_limit(self):
        if self.rect.left < 0:
            self.rect.x += 2 
            self.random_direction += random.random() * PI * 2
        if self.rect.right > WIDTH:
            self.rect.x -= 2 
            self.random_direction += random.random() * PI * 2
        if self.rect.top < 0:
            self.rect.y += 2 
            self.random_direction += random.random() * PI * 2
        if self.rect.bottom > HEIGHT:
            self.rect.y -= 2 
            self.random_direction += random.random() * PI * 2
            
    def gravity_force(self, all_particles):
        for particle in all_particles:
            if particle != self and particle.color == self.color:
                dx = particle.rect.centerx - self.rect.centerx
                dy = particle.rect.centery - self.rect.centery
                distance_squared = max(dx ** 2 + dy ** 2, 1)
                #gravity_force = GRAVITY_CONSTANT/distance_squared
                angle = math.atan2(dy, dx)
                #self.gravity_speed += gravity_force
                self.gravity_direction = angle
                
        self.rect.x += self.speed * math.cos(self.gravity_direction) * GRAVITY_VECTOR
        self.rect.y += self.speed * math.sin(self.gravity_direction) * GRAVITY_VECTOR
        
    def repulsion_force(self, all_particles):
        for particle in all_particles:
            if particle != self and particle.color != self.color:
                dx = particle.rect.centerx - self.rect.centerx
                dy = particle.rect.centery - self.rect.centery
                distance_squared = max(dx ** 2 + dy ** 2, 1)
                #gravity_force = GRAVITY_CONSTANT/distance_squared
                angle = math.atan2(dy, dx)
                #self.speed += gravity_force
                self.repulsion_direction = angle + PI

        self.rect.x += self.speed * math.cos(self.repulsion_direction)
        self.rect.y += self.speed * math.sin(self.repulsion_direction)
        
    def random_force(self):
        self.random_direction += random.uniform(-1,1) / 10
        self.rect.x += self.speed * math.cos(self.random_direction) * RANDOM_VECTOR
        self.rect.y += self.speed * math.sin(self.random_direction) * RANDOM_VECTOR

if __name__ == "__main__":
    game = Game()
    game.run()