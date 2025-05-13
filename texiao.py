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

class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0  # 初始半径
        self.max_radius = random.randint(50, 100)  # 增大最大半径范围
        self.growth_speed = random.uniform(1.0, 3.0)  # 增加生长速度
        self.color = random.choice([(255, 182, 193), (255, 105, 180), (255, 20, 147)])  # 随机粉色系颜色
        self.alpha = 255  # 初始透明度

    def update(self):
        if self.radius < self.max_radius:
            self.radius += self.growth_speed
        else:
            self.alpha -= 5  # 绽放完成后逐渐消失
        return self.alpha > 0

    def draw(self, screen):
        if self.alpha > 0:
            flower_surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(flower_surface, (*self.color, self.alpha), (self.max_radius, self.max_radius), int(self.radius))
            screen.blit(flower_surface, (int(self.x - self.max_radius), int(self.y - self.max_radius)))

class FlowerEffect:
    def __init__(self):
        self.flowers = []

    def create_flower(self, x, y):
        self.flowers.append(Flower(x, y))

    def update(self):
        self.flowers = [flower for flower in self.flowers if flower.update()]

    def draw(self, screen):
        for flower in self.flowers:
            flower.draw(screen)