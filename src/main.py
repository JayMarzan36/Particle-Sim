import pygame, sys, random, math
from particle import Particle
import kdTree
pygame.init()
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Particle-Sim")
def draw_ui(font, clock, particles):
    clock.tick(60)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f"Fps: {int(fps)}", True, (255, 255, 255))
    window.blit(fps_text, (10, 10))
    particles_stat = font.render(f"Particles: {int(len(particles))}", True, (255, 255, 255))
    window.blit(particles_stat, (80, 10))
def main():
    G = 0.1
    font = pygame.font.Font(None, 20)
    particles = []
    for i in range(200):
        particles.append(
            Particle(random.randint(0, width), random.randint(0, height), 1, 1,
                     [math.sin(random.uniform(0, 30)), math.cos(random.uniform(0, 30))], 0,
                     (255, 255, 255)))
    running = True
    clock = pygame.time.Clock()
    mouse_drag_start = None
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_drag_start = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    dx = mouse_pos[0] - mouse_drag_start[0]
                    dy = mouse_pos[1] - mouse_drag_start[1]
                    velocity = [dx * -1, dy * -1]
                    particles.append(
                        Particle(mouse_drag_start[0], mouse_drag_start[1], 1, 1, velocity, 0,
                                 (255, 255, 255)))
                elif event.button == 2:
                    mouse_pos = pygame.mouse.get_pos()
                    particles.append(Particle(mouse_pos[0], mouse_pos[1], 5, 10_000, [0,0], 0, (255, 0, 0)))
                mouse_drag_start = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    particles.clear()
                    for i in range(400):
                        particles.append(
                            Particle(random.randint(0, width), random.randint(0, height), 1, random.uniform(100, 1000),
                                     [0, 0], 0,
                                     (255, 255, 255)))
        window.fill(color=(0, 0, 0))

        if mouse_drag_start:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(window, (255, 0, 0), mouse_drag_start, mouse_pos, 2)

        # calculating and applying new forces
        for particle in particles:
            total_force = [0, 0]
            for other in particles:
                if particle != other:
                    force = particle.calculate_gravity(other, G)
                    total_force[0] += force[0]
                    total_force[1] += force[1]
            particle.apply_force(total_force)

        particles_to_remove = []
        # Collision
        for i, particle in enumerate(particles):
            for j, other in enumerate(particles):
                if i != j and particle not in particles_to_remove and other not in particles_to_remove:
                    dx = other.position[0] - particle.position[0]
                    dy = other.position[1] - particle.position[1]
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance < particle.radius + other.radius:
                        particle.merge(other)
                        particles_to_remove.append(other)
        particles = [particle for particle in particles if particle not in particles_to_remove]

        for particle in particles:
            particle.update(0.01)
            particle.draw_trail(window)
            particle.draw_particle(window)

        draw_ui(font, clock, particles)

        pygame.display.flip()


if __name__ == "__main__":
    main()
