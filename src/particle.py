import math
import pygame


class Particle:
    def __init__(self, x, y, radius, mass, velocity, color):
        self.x = x
        self.y = y
        self.position = [self.x, self.y]
        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        self.color = color
        self.trail = []

    def draw_particle(self, window):
        # pygame.draw.circle(window, self.color, (self.position[0], self.position[1]), self.radius)
        window.set_at((int(self.position[0]), int(self.position[1])), self.color)

    def draw_trail(self, window):
        for i, pos in enumerate(self.trail):
            sample_velocity = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2) * 2
            sample_velocity = min(max(sample_velocity, 0), 255)
            if sample_velocity > 255:
                sample_velocity = 255
            elif sample_velocity <= 0:
                sample_velocity = 0
            trail_color = (int(0 + sample_velocity), 1, int(255 - sample_velocity))
            trail_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (self.radius, self.radius), self.radius)
            window.blit(trail_surface, (pos[0] - self.radius, pos[1] - self.radius))

    def update(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.trail.append((self.position[0], self.position[1]))
        if len(self.trail) > 25:
            self.trail.pop(0)

    def apply_force(self, force):
        self.velocity[0] += force[0] / self.mass
        self.velocity[1] += force[1] / self.mass

    def merge(self, other):
        new_mass = self.mass + other.mass
        new_velocity = [(self.velocity[0] * self.mass + other.velocity[0] * other.mass) / new_mass,
                        (self.velocity[1] * self.mass + other.velocity[1] * other.mass) / new_mass]
        self.velocity = new_velocity
        self.mass = new_mass
        self.radius = int(math.sqrt(self.radius ** 2 + other.radius ** 2))
