import random
import pygame
from PIL import Image


class Particles:
    def __init__(self, screen, paths_to_images, n, size_range, vector, pos=(0, 0), spread_range=1000):
        """n - количество частиц
        color - кортеж от (0, 0, 0) до (230, 230, 230), (R, G, B)
        size_range - кортеж, последовательность возможных сторон квадратов частиц
        pos - опорная позиция частиц
        vector - скорость движения частиц изначально
        spread_range - величина разброса частиц в разные стороны"""

        self.all_particles = pygame.sprite.Group()
        self.screen = screen
        self.default_images = tuple(map(lambda a: pygame.image.load(a).convert_alpha(), paths_to_images))
        self.size_of_img = self.width, self.height = self.default_images[0].get_size()
        self.spread = spread_range

        for i in range(n):
            temp_size = random.randint(*size_range)
            temp_number_of_image = random.randint(0, len(self.default_images) - 1)
            temp_rotation = random.randint(0, 359)
            temp_sprite = pygame.sprite.Sprite(self.all_particles)
            temp_sprite.image = pygame.transform.rotate(pygame.transform.scale(self.default_images[temp_number_of_image],
                                                       (temp_size, temp_size)), temp_rotation)

            #  Сверху происходит рандомное маштабирование и выбор картинки частицы из перечня, еще поворот картинки

            temp_sprite.rect = temp_sprite.image.get_rect(center=pos)

            k = 10
            r1 = (random.randint(0, spread_range) - spread_range / 2) / 1000
            r2 = (random.randint(0, spread_range) - spread_range / 2) / 1000
            temp_sprite.vector = [r1 * k + vector[0],
                                  r2 * k + vector[1]]
            temp_sprite.default_vector = temp_sprite.vector.copy()

            temp_sprite.vector_degree_x = temp_sprite.default_vector[0] / 30
            temp_sprite.vector_degree_y = temp_sprite.default_vector[1] / 30
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
            print('moment_2')
            return True


class SimpleParticles:
    def __init__(self, screen, n, vector, color, size_range, pos=(0, 0), spread_range=1000):
        """n - количество частиц
        color - кортеж от (0, 0, 0) до (230, 230, 230), (R, G, B)
        size_range - кортеж, последовательность возможных сторон квадратов частиц
        pos - опорная позиция частиц
        vector - скорость движения частиц изначально
        spread_range - величина разброса частиц в разные стороны"""

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
            r1 = (random.randint(0, spread_range) - spread_range / 2) / 1000
            r2 = (random.randint(0, spread_range) - spread_range / 2) / 1000
            temp_sprite.vector = [r1 * k + vector[0],
                                  r2 * k + vector[1]]
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
'''


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
                    particles.append(SimpleParticles(screen, 30, (5, 0), (200, 30, 40), (2, 6),
                                     pos=click_pos))
                elif event.button == 1:
                    click_pos = event.pos
                    particles.append(Particles(screen, ('box_particle_1.png', 'box_particle_2.png'),
                                               30, (4, 10), (7, 0), pos=click_pos))

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


'''