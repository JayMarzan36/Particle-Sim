import pygame


class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.particles = []
        self.divided = False
        self.center_of_mass = [0, 0]
        self.total_mass = 0.0
        self.children = []

    def subdivide(self):
        x, y, w, h = self.boundary
        hw, hh = w / 2, h / 2
        self.children = [
            QuadTree((x, y, hw, hh), self.capacity),
            QuadTree((x + hw, y, hw, hh), self.capacity),
            QuadTree((x, y + hh, hw, hh), self.capacity),
            QuadTree((x + hw, y + hh, hw, hh), self.capacity),
        ]
        self.divided = True

    def insert(self, particle):
        if not self.contains(particle.position):
            return False
        if len(self.particles) < self.capacity:
            self.particles.append(particle)
            self.total_mass += particle.mass
            if self.total_mass != particle.mass:
                self.center_of_mass[0] = (self.center_of_mass[0] * (self.total_mass - particle.mass) + particle.position[0]) / self.total_mass
                self.center_of_mass[1] = (self.center_of_mass[1] * (self.total_mass - particle.mass) + particle.position[1]) / self.total_mass
            else:
                self.center_of_mass = particle.position[:]
            return True
        else:
            if not self.divided:
                self.subdivide()
            for child in self.children:
                if child.insert(particle):
                    self.total_mass += particle.mass
                    if self.total_mass != particle.mass:
                        self.center_of_mass[0] = (self.center_of_mass[0] * (self.total_mass - particle.mass) + particle.position[0] * particle.mass) / self.total_mass
                        self.center_of_mass[1] = (self.center_of_mass[1] * (self.total_mass - particle.mass) + particle.position[1] * particle.mass) / self.total_mass
                    else:
                        self.center_of_mass = particle.position[:]
                    return True
        return False

    def contains(self, position):
        x, y, w, h = self.boundary
        px, py = position
        return x <= px < x + w and y <= py < y + h

    def visualize_tree(self, window):
        x, y, w, h = self.boundary
        pygame.draw.rect(window, (0, 255, 0), pygame.Rect(x, y, w, h), 1)
        if self.divided:
            for child in self.children:
                child.visualize_tree(window)
