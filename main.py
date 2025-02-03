import pygame
import sys
import os
from particles import  Particles, SimpleParticles


class OfficeCrusher:
    def __init__(self, player):
        pygame.init()

        self.screen = pygame.display.set_mode((1024, 700))
        self.size = self.width, self.height = self.screen.get_size()
        self.screen.fill("black")
        pygame.display.set_caption('Office Crusher')
        self.clock = pygame.time.Clock()

        self.score_sistem = None

        self.all_particles = []

        self.flag_game = False
        self.flag_main_menu = True
        self.flag_controls_menu = False
        self.bullets_group = pygame.sprite.Group()
        self.bullet = None
        self.board = Board(player)  # Инициализация класса Board
        self.player = player
        self.player.board = self.board
        self.player.screen = self.screen

    def run(self):
        while True:
            if self.flag_main_menu:
                self.main_menu()
            elif self.flag_controls_menu:
                self.controls_menu()
            self.handle_events()
            if self.flag_game:
                self.update()
                self.render()  # Отрисовка экрана
            self.clock.tick(60)  # Ограничение до 60 FPS

    def main_menu(self):
        self.screen.fill("black")

        # Отображение текста вместо логотипа
        font = pygame.font.SysFont(None, 48)
        text_surface = pygame.image.load("лого (1).png").convert_alpha()
        text_rect = text_surface.get_rect(center=(500, 100))  # Центрирование текста
        self.screen.blit(text_surface, text_rect)

        # Загрузка текстур кнопок
        self.button_start_texture = pygame.image.load("начать (1).png").convert_alpha()
        self.button_option_texture = pygame.image.load("Управление (1).png").convert_alpha()
        self.button_exit_texture = pygame.image.load("уровни (1).png").convert_alpha()

        # Создание и отображение кнопок
        self.button_start_rect = self.button_start_texture.get_rect(topleft=(20, 250))
        self.screen.blit(self.button_start_texture, self.button_start_rect.topleft)

        self.button_option_rect = self.button_option_texture.get_rect(topleft=(20, 402))
        self.screen.blit(self.button_option_texture, self.button_option_rect.topleft)

        self.button_exit_rect = self.button_exit_texture.get_rect(topleft=(20, 700))
        self.screen.blit(self.button_exit_texture, self.button_exit_rect.topleft)

        pygame.display.flip()

    def controls_menu(self):
        self.screen.fill("black")

        # Открытие изображения на весь экран
        controls_image = pygame.image.load("controls_image.png").convert_alpha()  # Замените на ваше изображение
        controls_image = pygame.transform.scale(controls_image, (1480, 1024))
        self.screen.blit(controls_image, (0, 0))

        # Кнопка выхода назад
        self.button_back_texture = pygame.image.load("кнопка_назад.png").convert_alpha()
        self.button_back_rect = self.button_back_texture.get_rect(topleft=(20, 700))
        self.screen.blit(self.button_back_texture, self.button_back_rect.topleft)

        pygame.display.flip()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if hasattr(self, 'button_start_rect'):
                if self.button_start_rect.collidepoint(pygame.mouse.get_pos()) and self.flag_main_menu and \
                        pygame.mouse.get_pressed()[0]:
                    self.flag_game = True
                    self.flag_main_menu = False

                    #  пересоздание игрока при входе
                    player = Player()
                    self.all_particles.clear()
                    self.board = Board(player)  # Инициализация класса Board
                    self.player = player
                    self.player.board = self.board
                    self.player.screen = self.screen

                    self.score_sistem = Timer(self.screen, 100, 20, pygame.font.Font('fonts/Patopian 1986.ttf', 30))
                elif self.button_option_rect.collidepoint(pygame.mouse.get_pos()) and self.flag_main_menu and \
                        pygame.mouse.get_pressed()[0]:
                    self.flag_controls_menu = True
                    self.flag_main_menu = False
                elif self.button_exit_rect.collidepoint(pygame.mouse.get_pos()) and self.flag_main_menu and \
                        pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    sys.exit()
            if hasattr(self, 'button_back_rect'):
                if self.flag_controls_menu and self.button_back_rect.collidepoint(pygame.mouse.get_pos()) and \
                        pygame.mouse.get_pressed()[0]:
                    self.flag_controls_menu = False
                    self.flag_main_menu = True
            if self.board.is_wined() and self.flag_game:
                #  игра после зачистки карты
                score = self.score_sistem.get_score()
                pygame.time.wait(1000)
                with open('best_score.txt', mode='r') as file:
                    old_best_score = int(file.read())
                if old_best_score > score:
                    with open('best_score.txt', mode='w') as file:
                        file.write(str(score))
                self.flag_game = False
                self.flag_main_menu = True

            if self.flag_game and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.player.mode == 1:
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    if self.player.napravlenie == "left":
                        if x > 0 and type(self.board.level_data[y][x - 1]) == Furniture:
                            self.player.num_sprite = 1
                            self.board.level_data[y][x - 1].protect -= 1

                            x_pos = 477 - int(max([len(i) for i in self.board.level_data]) / 2 * 50) + x * 50
                            y_pos = int(375 - len(self.board.level_data) / 2 * 50 + y * 50)

                            if self.board.level_data[y][x - 1].protect <= 0:
                                self.board.level_data[y][x - 1] = "."
                                # создание частиц
                                self.all_particles.append(Particles(self.screen,
                                                                ('box_particle_1.png', 'box_particle_2.png'),
                                                                15, (8, 15), (-9, 0),
                                                                pos=(x_pos, y_pos), spread_range=800))
                            else:
                                self.all_particles.append(SimpleParticles(self.screen, 15, (-6, 0),
                                                                          (207, 182, 142), (4, 10),
                                                                          pos=(x_pos, y_pos), spread_range=800))

                    elif self.player.napravlenie == "right":
                        if x + 1 < len(self.board.level_data[y]) and type(self.board.level_data[y][x + 1]) == Furniture:
                            self.player.num_sprite = 1
                            self.board.level_data[y][x + 1].protect -= 1

                            x_pos = 587 - int(max([len(i) for i in self.board.level_data]) / 2 * 50) + x * 50
                            y_pos = int(375 - len(self.board.level_data) / 2 * 50 + y * 50)

                            if self.board.level_data[y][x + 1].protect <= 0:
                                self.board.level_data[y][x + 1] = "."
                                # создание частиц
                                self.all_particles.append(Particles(self.screen,
                                                                ('box_particle_1.png', 'box_particle_2.png'),
                                                                15, (8, 15), (9, 0),
                                                                pos=(x_pos, y_pos), spread_range=800))
                            else:
                                self.all_particles.append(SimpleParticles(self.screen, 15, (6, 0),
                                                                          (207, 182, 142), (4, 10),
                                                                          pos=(x_pos, y_pos), spread_range=800))

                    elif self.player.napravlenie == "up":
                        if y > 0 and type(self.board.level_data[y - 1][x]) == Furniture:
                            self.player.num_sprite = 1
                            self.board.level_data[y - 1][x].protect -= 1

                            x_pos = 537 - int(max([len(i) for i in self.board.level_data]) / 2 * 50) + x * 50
                            y_pos = int(325 - len(self.board.level_data) / 2 * 50 + y * 50)

                            if self.board.level_data[y - 1][x].protect <= 0:
                                self.board.level_data[y - 1][x] = "."
                                # создание частиц
                                self.all_particles.append(Particles(self.screen,
                                                                ('box_particle_1.png', 'box_particle_2.png'),
                                                                15, (8, 15), (0, -9),
                                                                pos=(x_pos, y_pos), spread_range=800))
                            else:
                                self.all_particles.append(SimpleParticles(self.screen, 15, (0, -6),
                                                                          (207, 182, 142), (4, 10),
                                                                          pos=(x_pos, y_pos), spread_range=800))
                    elif self.player.napravlenie == "down":
                        if y + 1 < len(self.board.level_data) and type(self.board.level_data[y + 1][x]) == Furniture:
                            self.player.num_sprite = 1
                            self.board.level_data[y + 1][x].protect -= 1
                            x_pos = 537 - int(max([len(i) for i in self.board.level_data]) / 2 * 50) + x * 50
                            y_pos = int(425 - len(self.board.level_data) / 2 * 50 + y * 50)
                            if self.board.level_data[y + 1][x].protect <= 0:
                                self.board.level_data[y + 1][x] = "."
                                # создание частиц
                                self.all_particles.append(Particles(self.screen,
                                                                ('box_particle_1.png', 'box_particle_2.png'),
                                                                15, (8, 15), (0, 9),
                                                                pos=(x_pos, y_pos), spread_range=800))
                            else:
                                self.all_particles.append(SimpleParticles(self.screen, 15, (0, 6),
                                                                          (207, 182, 142), (4, 10),
                                                                          pos=(x_pos, y_pos), spread_range=800))
                elif self.player.mode == 2 and len(self.bullets_group) == 0:
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    if self.player.napravlenie == "right":
                        self.bullet = Bullet(x, y, self.board, "right", self.all_particles, self.screen)
                    elif self.player.napravlenie == "left":
                        self.bullet = Bullet(x, y, self.board, "left", self.all_particles, self.screen)
                    elif self.player.napravlenie == "up":
                        self.bullet = Bullet(x, y, self.board, "up", self.all_particles, self.screen)
                    elif self.player.napravlenie == "down":
                        self.bullet = Bullet(x, y, self.board, "down", self.all_particles, self.screen)
                    self.bullets_group.add(self.bullet.sprite_bullet)
                    self.bullets_group.draw(self.screen)
                    self.player.num_sprite = 2
                self.board.generate_level()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if self.player.mode == 1:
                    self.player.weapon_update(2)
                else:
                    self.player.weapon_update(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.flag_game = False
                    self.flag_main_menu = True
                elif self.flag_game:
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.player.napravlenie = "left"
                        if x > 0 and self.board.level_data[y][x - 1] == ".":
                            self.board.level_data[y][x - 1] = "@"
                            self.board.level_data[y][x] = "."
                            self.player.move(self.clock, self.bullets_group, self.bullet)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.player.napravlenie = "right"
                        if x + 1 < len(self.board.level_data[y]) and self.board.level_data[y][x + 1] == ".":
                            self.board.level_data[y][x + 1] = "@"
                            self.board.level_data[y][x] = "."
                            self.player.move(self.clock, self.bullets_group, self.bullet)
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        self.player.napravlenie = "up"
                        if y > 0 and self.board.level_data[y - 1][x] == ".":
                            self.board.level_data[y - 1][x] = "@"
                            self.board.level_data[y][x] = "."
                            self.player.move(self.clock, self.bullets_group, self.bullet)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.player.napravlenie = "down"
                        if y + 1 < len(self.board.level_data) and self.board.level_data[y + 1][x] == ".":
                            self.board.level_data[y + 1][x] = "@"
                            self.board.level_data[y][x] = "."
                            self.player.move(self.clock, self.bullets_group, self.bullet)

    def update(self):
        self.player.update()

        #  update частиц на поле
        count = 0
        while count < len(self.all_particles):
            kill = self.all_particles[count].update()
            if kill:
                del self.all_particles[count]
                count -= 1
            count += 1

        self.score_sistem.update()

        pygame.display.flip()

    def render(self):
        self.screen.fill((100, 100, 100))  # Очистка экрана
        self.board.render(self.screen)
        if len(self.bullets_group) > 0:
            self.bullet.update()
            self.bullets_group.draw(self.screen)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, list_level):
        super().__init__()
        num_x = 512 - int(max([len(i) for i in list_level]) / 2 * 50)
        num_y = 350 - len(list_level) / 2 * 50
        if tile_type == 'empty':
            self.image = pygame.image.load("тайл пол.png").convert_alpha()
        elif tile_type == "furniture":
            self.image = list_level[pos_y][pos_x].update().convert_alpha()
        self.rect = self.image.get_rect().move(
            50 * pos_x + num_x, 50 * pos_y + num_y)


class Timer:
    def __init__(self, screen, x_pos, y_pos, font, fps=60):
        self.screen = screen
        self.time_started = pygame.time.get_ticks()
        self.fps = fps
        self.font = font
        self.text = '00000'
        self.text_now = font.render(self.text, True, (0, 0, 0))
        self.txt_w, self.txt_h = self.text_now.get_size()
        self.width = 10 #  ширина рамки
        self.frame_rect = pygame.Rect((x_pos, y_pos, self.txt_w + self.width + 25,
                                      self.txt_h + self.width + 25))
        self.text_rect = self.text_now.get_rect(center=self.frame_rect.center)
        self.delta = 0

    def delta_update(self):
        self.delta = (pygame.time.get_ticks() - self.time_started) * 50 // self.fps #  delta в два раза меньше прошедших миллисекунд

    def text_update(self):
        self.text = '0' * (5 - len(str(self.delta))) + str(self.delta)
        self.text_now = self.font.render(self.text, True, (0, 0, 0))

    def update(self):
        self.delta_update()
        self.text_update()
        pygame.draw.rect(self.screen, (255, 212, 133), self.frame_rect)
        pygame.draw.rect(self.screen, 'black', self.frame_rect, width=self.width)
        self.screen.blit(self.text_now, self.text_rect)

    def get_score(self):
        return self.delta

class WeaponFrame:
    def __init__(self, imgs_pathes, size, x, y):
        self.size = size
        self.rect = pygame.Rect(x - size[0] / 2, y - size[1] / 2, *size)
        self.x, self.y = x, y
        self.color_in = pygame.color.Color((100, 80, 80))
        self.weapon = 0 #  0 - лом, 1 - пистолет
        self.weapon_images = [pygame.image.load(i) for i in imgs_pathes]
        self.weapon_img_now = self.weapon_images[self.weapon]

    def update_weapon(self, weapon_number):
        self.weapon_img_now = self.weapon_images[weapon_number]
        self.weapon = weapon_number

    def update(self, screen):
        pygame.draw.rect(screen, self.color_in, self.rect)
        pygame.draw.rect(screen, 'black', self.rect, width=10)
        screen.blit(self.weapon_img_now, (self.x - 25, self.y - 25))


class Player:
    def __init__(self):
        self.num_sprite = 0
        self.mode = 1
        self.sprite_player_group = pygame.sprite.Group()
        self.sprite_player = pygame.sprite.Sprite()
        self.sprite_player.image = pygame.image.load("персонаж_вниз.png")
        self.sprite_player.rect = self.sprite_player.image.get_rect()
        self.sprite_player_group.add(self.sprite_player)
        self.screen = None
        self.board = None
        self.weapon_box = WeaponFrame(('textures/crowbar_icon.png', 'textures/pistol_icon.png'),
                                      (70, 70), 50, 50)
        self.napravlenie = "down"
        self.dictenary_napr = {"down": [0, "y", 5], "right": [90, "x", 5], "up": [180, "y", -5], "left": [270, "x", -5]}
        self.dictenary_sprite = [pygame.image.load("персонаж_вниз.png"), pygame.image.load("crowbar.png"),
                               pygame.image.load("pistol.png")]

    def update(self):
        self.sprite_player.image = pygame.transform.rotate(self.dictenary_sprite[self.num_sprite],
                                                           self.dictenary_napr[self.napravlenie][0])
        self.weapon_box.update(self.screen)
        self.sprite_player_group.draw(self.screen)

    def weapon_update(self, new_value):
        self.mode = new_value # mode = индекс оружия + 1
        self.weapon_box.update_weapon(self.mode - 1) #  смена оружия в рамке

    def move(self, clock, bullets_group, bullet):
        for i in range(10):
            if self.dictenary_napr[self.napravlenie][1] == "x":
                self.sprite_player.rect.x += self.dictenary_napr[self.napravlenie][2]
            elif self.dictenary_napr[self.napravlenie][1] == "y":
                self.sprite_player.rect.y += self.dictenary_napr[self.napravlenie][2]
            self.screen.fill((100, 100, 100))
            self.board.render(self.screen)
            if len(bullets_group) > 0:
                bullet.update()
                bullets_group.draw(self.screen)
            self.num_sprite = 0
            self.update()
            pygame.display.flip()
            clock.tick(60)


class Board:
    def __init__(self, player):
        self.tiles = pygame.sprite.Group()  # Группа спрайтов для тайлов
        self.width = 0
        self.height = 0
        self.player = player
        self.cell_size = 50  # Размер ячейки (50px)
        self.level_data = [list(i) for i in self.load_level("level3")]  # Пример имени файла
        for y in range(len(self.level_data)):
            for x in range(len(self.level_data[y])):
                if self.level_data[y][x] in "12":
                    self.level_data[y][x] = Furniture(self.level_data[y][x])
        self.load_level_data()  # Загрузка уровня (получите уровень через метод)

    def load_level_data(self):
        self.width, self.height = self.generate_level()

    def load_level(self, filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self):
        x, y = 0, 0
        level = self.level_data
        for i in self.tiles:
            i.kill()
        for y in range(len(level)):
            for x in range(len(level[y])):
                tile = Tile('empty', x, y, level)
                self.tiles.add(tile)  # Добавление тайла в группу
                if type(level[y][x]) is Furniture:
                    tile = Tile('furniture', x, y, level)
                    self.tiles.add(tile)  # Добавление тайла в группу
                elif level[y][x] == '@':
                    self.player.sprite_player.rect.x = \
                        512 - int(max([len(i) for i in level]) / 2 * 50) + x * 50
                    self.player.sprite_player.rect.y = \
                        int(350 - len(level) / 2 * 50 + y * 50)
        return x, y

    def render(self, screen):
        self.tiles.draw(screen)  # Отображение всех спрайтов в группе

    def is_wined(self):
        for i in self.level_data:
            for j in i:
                if j not in ('@', '.'):
                    return False
        return True

class Furniture:
    def __init__(self, number):
        self.num = int(number)
        self.protect = 2
        self.rect = None

    def update(self):
        if self.protect == 2:
            return pygame.image.load(f"мебель_тайл_{self.num}.png")
        return pygame.image.load(f"furniture_tile_breakung_{self.num}.png")

    def __class__(self):
        return Furniture


class Bullet:
    def __init__(self, x, y, board, napravlenie, particles, screen):
        print(board)
        self.particles = particles
        self.screen = screen

        self.sprite_bullet = pygame.sprite.Sprite()
        self.sprite_bullet.image = pygame.image.load("bullet.png")
        self.sprite_bullet.rect = self.sprite_bullet.image.get_rect()
        self.sprite_bullet.rect.x = \
            512 - int(max([len(i) for i in board.level_data]) / 2 * 50) + x * 50 + 12
        self.sprite_bullet.rect.y = \
            int(350 - len(board.level_data) / 2 * 50 + y * 50) + 12
        self.x = x
        self.y = y
        self.napr = napravlenie
        self.board = board

    def update(self):
        board = self.board.level_data
        if self.napr == "right":
            self.sprite_bullet.rect.x += 10
            if self.sprite_bullet.rect.x >= 512 + int(max([len(i) for i in board]) / 2 * 50):
                self.sprite_bullet.kill()
                print('killed_by_background')
            elif (len([i for i in board[self.y][self.x:] if type(i) == Furniture]) > 0
                    and self.sprite_bullet.rect.x >= 512 - 12 - int(max([len(i) for i in board]) / 2 * 50) + board[
                self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0]) * 50 + 12):
                board[self.y][
                    board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])].protect -= 0.5
                if board[self.y][
                    board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])].protect <= 0:
                    board[self.y][
                        board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])] = "."
                    #  частицы при разрушении
                    self.particles.append(Particles(self.screen,
                                                    ('box_particle_1.png', 'box_particle_2.png'),
                                                    15, (8, 15), (7, 0),
                                                    pos=self.sprite_bullet.rect.center, spread_range=700))
                else:
                    self.particles.append(SimpleParticles(self.screen, 10, (4, 0),
                                                              (207, 182, 142), (2, 8),
                                                              pos=self.sprite_bullet.rect.center, spread_range=600))
                self.board.generate_level()
                self.sprite_bullet.kill()
                print('killed_by_colliding')
        elif self.napr == "left":
            self.sprite_bullet.image = pygame.transform.rotate(pygame.image.load("bullet.png"), 180)
            self.sprite_bullet.rect.x -= 10
            if self.sprite_bullet.rect.x <= 512 - int(max([len(i) for i in board]) / 2 * 50):
                self.sprite_bullet.kill()
            if (len([i for i in reversed(board[self.y][:self.x]) if
                     type(i) == Furniture]) > 0 and self.sprite_bullet.rect.x <= 25 + 512 - int(
                max([len(i) for i in board]) / 2 * 50) +
                    board[self.y].index([i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0]) * 50):
                board[self.y][board[self.y].index(
                    [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])].protect -= 1
                if board[self.y][board[self.y].index(
                        [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])].protect <= 0:
                    board[self.y][board[self.y].index(
                        [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])] = "."
                    #  частицы при разрушении
                    self.particles.append(Particles(self.screen,
                                                    ('box_particle_1.png', 'box_particle_2.png'),
                                                    15, (8, 15), (-7, 0),
                                                    pos=self.sprite_bullet.rect.center, spread_range=700))
                else:
                    self.particles.append(SimpleParticles(self.screen, 10, (-4, 0),
                                                              (207, 182, 142), (2, 8),
                                                              pos=self.sprite_bullet.rect.center, spread_range=600))
                self.board.generate_level()
                self.sprite_bullet.kill()
        elif self.napr == "up":
            self.sprite_bullet.image = pygame.transform.rotate(pygame.image.load("bullet.png"), 90)
            self.sprite_bullet.rect.y -= 10
            if self.sprite_bullet.rect.y <= 350 - int(max([len(i) for i in board]) / 2 * 50):
                self.sprite_bullet.kill()
            if len([i for i in reversed(board[:self.y]) if
                    type(i[self.x]) == Furniture]) > 0 and self.sprite_bullet.rect.y <= 350 - int(
                    max([len(i) for i in board]) / 2 * 50) + board.index(
                    [i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0]) * 50 + 25:
                board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                    self.x].protect -= 0.5
                self.sprite_bullet.kill()
                if board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                    self.x].protect <= 0:
                    board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                        self.x] = "."
                    #  частицы при разрушении
                    self.particles.append(Particles(self.screen,
                                                    ('box_particle_1.png', 'box_particle_2.png'),
                                                    15, (8, 15), (0, -7),
                                                    pos=self.sprite_bullet.rect.center, spread_range=700))
                else:
                    self.particles.append(SimpleParticles(self.screen, 10, (0, -4),
                                                              (207, 182, 142), (2, 8),
                                                              pos=self.sprite_bullet.rect.center, spread_range=600))
                self.board.generate_level()
                self.sprite_bullet.kill()
        elif self.napr == "down":
            self.sprite_bullet.image = pygame.transform.rotate(pygame.image.load("bullet.png"), 270)
            self.sprite_bullet.rect.y += 10
            if self.sprite_bullet.rect.y >= 350 + int(max([len(i) for i in board]) / 2 * 50):
                self.sprite_bullet.kill()
            if len([i for i in board[self.y:] if
                    type(i[self.x]) == Furniture]) > 0 and self.sprite_bullet.rect.y >= 350 - int(
                max([len(i) for i in board]) / 2 * 50) + board.index(
                [i for i in board[self.y:] if
                 type(i[self.x]) == Furniture][0]) * 50 + 12:
                board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][self.x].protect -= 1
                if board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][
                    self.x].protect <= 0:
                    board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][
                        self.x] = "."
                    #  частицы при разрушении
                    self.particles.append(Particles(self.screen,
                                                   ('box_particle_1.png', 'box_particle_2.png'),
                                                   15, (8, 15), (0, 7),
                                                   pos=self.sprite_bullet.rect.center, spread_range=700))
                else:
                    self.particles.append(SimpleParticles(self.screen, 10, (0, 4),
                                                              (207, 182, 142), (2, 8),
                                                              pos=self.sprite_bullet.rect.center, spread_range=600))
                self.board.generate_level()
                self.sprite_bullet.kill()


if __name__ == "__main__":
    game = OfficeCrusher(Player())
    game.run()
