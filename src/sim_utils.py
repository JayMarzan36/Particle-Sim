import random, math
import pygame
import numpy as np

from particle import Particle
from QuadTree import QuadTree


def gen_rand(amount: int, width, height, velocity_range: list):
    particle_list = []
    for i in range(amount):
        x = random.randint(0, width)
        y = random.randint(0, height)
        particle_list.append(Particle(x, y, 2, 10, [0.5, 0.5], 0, (255, 255, 255)))
    return particle_list


def draw_ui(font, clock, particles, window):

    clock.tick(60)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f"Fps: {int(fps)}", True, (255, 255, 255))
    window.blit(fps_text, (10, 10))

    particles_stat = font.render(f"Particles: {int(len(particles))}", True, (255, 255, 255))
    window.blit(particles_stat, (80, 10))





def build_tree(particles, boundary, capacity=1):
    quad_tree = QuadTree(boundary, capacity)
    for particle in particles:
        quad_tree.insert(particle)
    return quad_tree


def compute_force(particle, quadtree, theta=0.5, G=1.0):
    def force_between(p1, p2):
        dx = p2.position[0] - p1.position[0]
        dy = p2.position[1] - p1.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            return [0, 0]
        force_magnitude = G * p1.mass * p2.mass / distance ** 2
        force_direction = [dx / distance, dy / distance]
        return [force_magnitude * force_direction[0], force_magnitude * force_direction[1]]

    def traverse(node):
        if node is None:
            return [0, 0]
        if not node.divided:
            force = [0, 0]
            for p in node.particles:
                if p is not particle:
                    calc_force = force_between(particle, p)
                    force[0] += calc_force[0]
                    force[1] += calc_force[1]
            return force

        dx = node.center_of_mass[0] - particle.position[0]
        dy = node.center_of_mass[1] - particle.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            return [0, 0]
        if (node.boundary[2] / distance) < theta:
            temp_particle = Particle(node.center_of_mass[0], node.center_of_mass[1], 0, node.total_mass, [0, 0], 0,
                                     (0, 0, 0))
            return force_between(particle, temp_particle)

        force = [0, 0]
        for child in node.children:
            calc_force = traverse(child)
            force[0] += calc_force[0]
            force[1] += calc_force[1]
        return force

    return traverse(quadtree)


def update_particles(particles, quadtree, width, height, theta=0.5, G=0.1, dt=0.01):
    particles_to_remove = []
    for particle in particles:
        if particle.position[0] > width or particle.position[0] < 0 or particle.position[1] > height or \
            particle.position[1] < 0:
            particles_to_remove.append(particle)

        force = compute_force(particle, quadtree, theta, G)
        particle.apply_force(force)
        particle.update(dt)
    particles = [particle for particle in particles if particle not in particles_to_remove]
    return particles


def draw_full_particle(particles, window):
    for particle in particles:
        particle.draw_trail(window)
        particle.draw_particle(window)
