from particle import Particle
import random


def gen_rand(amount: int, width, height):
    particle_list = []
    for i in range(amount):
        x = random.randint((width / 4), width - (width / 4))
        y = random.randint((height / 4), height - (height / 4))
        particle_list.append(Particle(x, y, 1, 10, [0.0, 0.0], (255, 255, 255)))
    return particle_list


def plus(width, height):
    particle_list = [Particle((width // 2), (height // 2), 2, 10000, [0, 0], (255, 255, 255)),
                     Particle((width // 2 + 150), (height // 2), 1, 1, [0, 2], (255, 255, 255)),
                     Particle((width // 2 - 150), (height // 2), 1, 1, [0, -2], (255, 255, 255)),
                     Particle((width // 2), (height // 2 + 150), 1, 1, [-2, 0], (255, 255, 255)),
                     Particle((width // 2), (height // 2 - 150), 1, 1, [2, 0], (255, 255, 255))]
    return particle_list


def small_galaxy(amount, width, height):
    particle_list = [Particle((width // 2), (height // 2), 4, 100000, [0, 0], (255, 255, 255))]
    for i in range(amount):
        new_particle = Particle(random.randint(0, width), random.randint(0, height), 1, random.randint(1, 100),
                                [random.randint(-30, 30), random.randint(-30, 30)], (255, 255, 255))
        particle_list.append(new_particle)
    return particle_list
