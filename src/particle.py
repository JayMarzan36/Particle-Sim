import pygame, math
class Particle:
    def __init__(self, x, y, radius, mass, velocity, acceleration, color):
        self.x = x
        self.y = y

        self.position = [self.x, self.y]

        self.radius = radius

        self.mass = mass
        self.velocity = velocity
        self.acceleration = [acceleration]

        self.color = color
        self.trail = []

    def move(self):
        pass

    def draw_particle(self, window):
        pygame.draw.circle(window, self.color, self.position, self.radius)

    def draw_trail(self, window):
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            trail_color = (*self.color[:3], alpha)
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

    def calculate_gravity(self, other, G):
        dx = other.position[0] - self.position[0]
        dy = other.position[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            return [0, 0]
        force_magnitude = G * self.mass * other.mass / distance ** 2
        force_direction = [dx / distance, dy / distance]
        return [force_magnitude * force_direction[0], force_magnitude * force_direction[1]]

    def merge(self, other):
        new_mass = self.mass + other.mass
        new_velocity = [(self.velocity[0] * self.mass + other.velocity[0] * other.mass) / new_mass, (self.velocity[1] * self.mass + other.velocity[1] * other.mass) / new_mass]
        self.velocity = new_velocity
        self.mass = new_mass
        self.radius = int(math.sqrt(self.radius ** 2 + other.radius ** 2))
        self.trail = []