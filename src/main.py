import pygame, sys, math, threading
from particle import Particle
from sim_utils import draw_ui, draw_full_particle, build_tree, update_particles, run_sim
from uiButton import Button
from formations import gen_rand
from handleUser import handle_user, show_mouse_launch, handle_user_button

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
    mouse_drag_start = None

    while True:
        quadtree = build_tree(particles, (0, 0, width, height))
        user_results = handle_user(width, height, particles, mouse_drag_start, node_button)
        mouse_drag_start = user_results[1]
        particles = user_results[0]
        window.fill(color=(0, 0, 0))
        show_mouse_launch(mouse_drag_start, window)
        handle_user_button(node_button)
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
