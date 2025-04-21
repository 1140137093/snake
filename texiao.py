import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        # Random angle and speed for particle movement
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 8)
        self.life = 100  # Particle lifetime
        self.alpha = 255  # Particle transparency
        
    def update(self):
        # Move particle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        # Slow down
        self.speed *= 0.95
        # Fade out
        self.life -= 2
        self.alpha = int((self.life / 100) * 255)
        return self.life > 0

    def draw(self, screen):
        if self.alpha > 0:
            # Create a surface with alpha channel
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            # Draw particle with current alpha
            pygame.draw.circle(particle_surface, (*self.color, self.alpha), (2, 2), 2)
            screen.blit(particle_surface, (int(self.x), int(self.y)))

class Firework:
    def __init__(self):
        self.particles = []
        self.active = False

    def create_explosion(self, x, y):
        self.active = True
        # Create multiple particles with different colors
        colors = [(255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 255, 255)]
        for _ in range(50):  # Create 50 particles
            color = random.choice(colors)
            self.particles.append(Particle(x, y, color))

    def update(self):
        if not self.active:
            return
        
        # Update all particles and remove dead ones
        self.particles = [p for p in self.particles if p.update()]
        if not self.particles:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
        
        for particle in self.particles:
            particle.draw(screen) 