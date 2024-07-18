import pygame, sys, queue, threading, math, time
from particle import Particle
from sim_utils import draw_ui, draw_full_particle, build_tree, update_particles
from uiButton import Button
from formations import gen_rand, plus, small_galaxy

pygame.init()
width = 1200
height = 1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Particle-Sim")


def main():
    font = pygame.font.Font(None, 20)
    node_button = Button(200, 5, 80, 20, (255, 255, 255), "Show nodes", font)
    particles = gen_rand(100, width, height)
    clock = pygame.time.Clock()
    running = True
    mouse_drag_start = None

    while running:
        quadtree = build_tree(particles, (0, 0, width, height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    if node_button.is_mouse_over():
                        node_button.toggle()
                    else:
                        mouse_drag_start = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    if not node_button.is_mouse_over():
                        mouse_pos = pygame.mouse.get_pos()
                        dx = mouse_pos[0] - mouse_drag_start[0]
                        dy = mouse_pos[1] - mouse_drag_start[1]
                        velocity = [dx * -1, dy * -1]
                        if event.button == 1:
                            new_particle = Particle(mouse_drag_start[0], mouse_drag_start[1], 1, 1, velocity, 0,
                                                    (255, 255, 255))
                        elif event.button == 3:
                            new_particle = Particle(mouse_drag_start[0], mouse_drag_start[1], 1, 10_000, velocity, 0,
                                                    (255, 255, 255))
                        particles.append(new_particle)
                elif event.button == 2:
                    mouse_pos = pygame.mouse.get_pos()
                    particles.append(Particle(mouse_pos[0], mouse_pos[1], 1, 10_000, [0, 0], 0, (255, 255, 255)))
                mouse_drag_start = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    particles.clear()
                    particles = gen_rand(1000, width, height)
                if event.key == pygame.K_EQUALS:
                    particles.clear()
                    particles = plus(width, height)
                elif event.key == pygame.K_s:
                    particles.clear()
                    particles = small_galaxy(200, width, height)

        window.fill(color=(0, 0, 0))

        if mouse_drag_start:
            mouse_pos = pygame.mouse.get_pos()
            dx = mouse_drag_start[0] - mouse_pos[0]
            dy = mouse_drag_start[1] - mouse_pos[1]
            position_difference = math.sqrt(dx ** 2 + dy ** 2)
            if position_difference > 255:
                position_difference = 255
            launch_color = (0 + position_difference, 0, 255 - position_difference)
            pygame.draw.line(window, launch_color, mouse_drag_start, mouse_pos, 2)

        if node_button.is_mouse_over():
            node_button.color = (100, 100, 100)
        else:
            node_button.color = (255, 255, 255)

        # update
        particles = update_particles(particles, quadtree, width, height, theta=10)
        draw_full_particle(particles, window)
        draw_ui(font, clock, particles, window)
        node_button.draw(window)


        if node_button.state:
            quadtree.visualize_tree(window)

        pygame.display.flip()


if __name__ == "__main__":
    main()
