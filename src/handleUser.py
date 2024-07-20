import pygame, sys, math
from particle import Particle
from formations import gen_rand, plus, small_galaxy


def handle_user(width, height, particles, mouse_drag_start, node_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
                        particles.append(Particle(mouse_drag_start[0], mouse_drag_start[1], 1, 10, velocity,
                                                  (255, 255, 255)))
                    elif event.button == 3:
                        particles.append(Particle(mouse_drag_start[0], mouse_drag_start[1], 1, 10_000, velocity,
                                                  (255, 255, 255)))
            elif event.button == 2:
                mouse_pos = pygame.mouse.get_pos()
                particles.append(Particle(mouse_pos[0], mouse_pos[1], 1, 10_000, [0, 0], (255, 255, 255)))
            mouse_drag_start = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                particles.clear()
                particles = gen_rand(1000, width, height, rand=True)
            elif event.key == pygame.K_t:
                particles.clear()
                particles = gen_rand(1000, width, height, rand=True, center=True)
            elif event.key == pygame.K_EQUALS:
                particles.clear()
                particles = plus(width, height)
            elif event.key == pygame.K_s:
                particles.clear()
                particles = small_galaxy(200, width, height)
            elif event.key == pygame.K_g:
                particles.clear()
                particles = gen_rand(10000, width, height, center=True)
    return [particles, mouse_drag_start]


def show_mouse_launch(mouse_drag_start, window):
    if mouse_drag_start:
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_drag_start[0] - mouse_pos[0]
        dy = mouse_drag_start[1] - mouse_pos[1]
        position_difference = math.sqrt(dx ** 2 + dy ** 2)
        if position_difference > 255:
            position_difference = 255
        launch_color = (0 + position_difference, 0, 255 - position_difference)
        pygame.draw.line(window, launch_color, mouse_drag_start, mouse_pos, 2)


def handle_user_button(node_button):
    if node_button.is_mouse_over():
        node_button.color = (100, 100, 100)
    else:
        node_button.color = (255, 255, 255)
