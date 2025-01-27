import random
import pygame
from PIL import Image


class Particles:
    def __init__(self, screen, path_to_image, n, vector, pos=(0, 0)):
        """n - количество кусочков с каждой стороны (всего частиц - n * n)
        color - кортеж от (0, 0, 0) до (230, 230, 230), (R, G, B)
        size_range - кортеж, последовательность возможных сторон квадратов частиц
        pos - опорная позиция частиц
        vector - скорость движения частиц изначально"""

        self.all_particles = pygame.sprite.Group()
        self.screen = screen
        self.big_image = Image.open(path_to_image)
        self.size_of_img = self.width, self.height = self.big_image.size
        mode = self.big_image.mode

        for i in range(0, self.width, n):
            for j in range(0, self.height, n):
                    temp_data = self.big_image.crop((i, j, i + n, j + n)).tobytes('raw', 'RGBA')
                    temp_sprite = pygame.sprite.Sprite(self.all_particles)
                    temp_sprite.image = pygame.image.fromstring(temp_data, (n, n), 'RGBA')
                    temp_sprite.rect = pygame.Rect(pos[0] - n / 2, pos[1] - n / 2, n, n)
                    temp_sprite.center = list(temp_sprite.rect.center)
                    k = 10
                    r1 = random.random()
                    r2 = random.random()
                    temp_sprite.vector = [(r1 - 0.5) * k + vector[0],
                                          (r2 - 0.5) * k + vector[1]]
                    temp_sprite.default_vector = temp_sprite.vector.copy()

                    temp_sprite.vector_degree_x = temp_sprite.default_vector[0] / 30
                    temp_sprite.vector_degree_y = temp_sprite.default_vector[1] / 30
                    temp_sprite.vector_sign_x = temp_sprite.vector_degree_x > 0
                    temp_sprite.vector_sign_y = temp_sprite.vector_degree_y > 0

                    temp_sprite.rotation_speed = random.randint(-70, 70)

    def update(self):
        self.all_particles.draw(self.screen)

        for sprite in self.all_particles:
            sprite.center[0] += sprite.vector[0]
            sprite.center[1] += sprite.vector[1]
            print(sprite.vector)
            sprite.rect = sprite.rect.move(*sprite.vector)
            sprite.vector[0] -= sprite.vector_degree_x
            sprite.vector[1] -= sprite.vector_degree_y
            cond_1 = sprite.vector[0] <= sprite.vector_degree_x if sprite.vector_sign_x\
                else sprite.vector[0] >= sprite.vector_degree_x
            cond_2 = sprite.vector[1] <= sprite.vector_degree_y if sprite.vector_sign_y \
                else sprite.vector[1] >= sprite.vector_degree_y
            if cond_1 and cond_2:
                sprite.kill()

        if not self.all_particles.sprites():
            print('moment_2')
            return True


class SimpleParticles:
    def __init__(self, screen, n, vector, color, size_range, pos=(0, 0)):
        """n - количество частиц
        color - кортеж от (0, 0, 0) до (230, 230, 230), (R, G, B)
        size_range - кортеж, последовательность возможных сторон квадратов частиц
        pos - опорная позиция частиц
        vector - скорость движения частиц изначально"""

        self.all_particles = pygame.sprite.Group()
        self.screen = screen

        for i in range(n):
            temp_sprite = pygame.sprite.Sprite(self.all_particles)

            temp_color = tuple(map(lambda a: random.randint(a - 10, a + 10), color))
            print(temp_color)
            temp_size = random.randint(*size_range)

            temp_sprite.image = pygame.Surface((temp_size, temp_size))
            temp_sprite.image.fill(temp_color)
            temp_sprite.rect = temp_sprite.image.get_rect(center=pos)
            k = 10
            r1 = random.random()
            r2 = random.random()
            temp_sprite.vector = [(r1 - 0.5) * k + vector[0],
                                  (r2 - 0.5) * k + vector[1]]
            temp_sprite.default_vector = temp_sprite.vector.copy()

            temp_sprite.vector_degree_x = temp_sprite.default_vector[0] / 50
            temp_sprite.vector_degree_y = temp_sprite.default_vector[1] / 50
            temp_sprite.vector_sign_x = temp_sprite.vector_degree_x > 0
            temp_sprite.vector_sign_y = temp_sprite.vector_degree_y > 0


    def update(self):
        self.all_particles.draw(self.screen)

        for sprite in self.all_particles:
            sprite.rect = sprite.rect.move(*sprite.vector)
            sprite.vector[0] -= sprite.vector_degree_x
            sprite.vector[1] -= sprite.vector_degree_y
            cond_1 = sprite.vector[0] <= sprite.vector_degree_x if sprite.vector_sign_x\
                else sprite.vector[0] >= sprite.vector_degree_x
            cond_2 = sprite.vector[1] <= sprite.vector_degree_y if sprite.vector_sign_y \
                else sprite.vector[1] >= sprite.vector_degree_y
            if cond_1 and cond_2:
                sprite.kill()

        if not self.all_particles.sprites():
            print('moment_1')
            return True



def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    in_process = True

    click_pos = None
    particles = []

    while in_process:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_process = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    click_pos = event.pos
                    particles.append(SimpleParticles(screen, 15, (5, 0), (200, 30, 40), (2, 6),
                                     pos=click_pos))
                elif event.button == 1:
                    click_pos = event.pos
                    particles.append(Particles(screen, 'furniture_tile_2.png', 10, (10, 0),
                                               pos=click_pos))

        screen.fill('black')

        count = 0

        while count < len(particles):
            kill = particles[count].update()
            if kill:
                del particles[count]
                count -= 1
            count += 1

        pygame.display.flip()
        clock.tick(50)

    pygame.quit()


main()


