import pygame
import sqlite3
import os
import sys


class OfficeCrusher:
    def __init__(self, player):
        pygame.init()
        self.screen_size = (1480, 1024)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill("black")
        print(self.screen)

        pygame.display.set_caption('Office Crusher')
        self.clock = pygame.time.Clock()
        self.flag_game = False
        self.flag_main_menu = True
        self.flag_controls_menu = False
        self.flag_levels = False
        self.board = Board()  # Инициализация класса Board
        self.player = player
        self.level_dict = dict()

        self.mousePos = pygame.mouse.get_pos()
        self.is_clicked = pygame.mouse.get_pressed(num_buttons=5)[0]

        self.label = pygame.font.Font("Inky-Thin-Pixels_0.ttf", 45)
        self.start_button = Button(self.screen, 20, 300, 450, 150, self.label, 'startButton',
                                   'Начать игру', 'black')
        self.exit_button = Button(self.screen, 20, 640, 450, 150, self.label, 'exitButton',
                                  'Выйти из игры', 'black')
        self.edit_button = Button(self.screen, 20, 470, 450, 150, self.label, 'settings_button',
                                  'Настройки', 'black')
        self.level_select_button = Button(self.screen, 20, 810, 450, 150, self.label, 'level_select',
                                          'Уровни', 'black')
        self.buttons_menu = [self.start_button, self.exit_button, self.edit_button, self.level_select_button]

        self.first_level = Button(self.screen, 50, 30, 450, 150, self.label, 'first',
                                  f'1', 'black')
        self.second_level = Button(self.screen, 50, 230, 450, 150, self.label, 'second',
                                   f'2 игру', 'black')
        self.third_level = Button(self.screen, 50, 430, 450, 150, self.label, 'third',
                                  f'3 игру', 'black')
        self.fourth_level = Button(self.screen, 50, 630, 450, 150, self.label, 'fourth',
                                   f'4 игру', 'black')
        self.fifth_level = Button(self.screen, 50, 830, 450, 150, self.label, 'fifth',
                                  f'5 игру', 'black')

        self.buttons_levels = [self.first_level, self.second_level, self.third_level, self.fourth_level, self.fifth_level]

    def move(self, dir, len):
        self.player.move(dir, len)

    def run(self):
        directory_path = 'data'
        database_name = 'levels'
        self.find_files_in_directory(directory_path, database_name)
        while True:
            self.handle_events()
            self.mousePos = pygame.mouse.get_pos()
            self.is_clicked = pygame.mouse.get_pressed(num_buttons=5)[0]
            print(self.flag_game, self.flag_main_menu, self.flag_controls_menu, self.flag_levels)
            if self.flag_main_menu:
                self.screen.fill((0, 0, 0))
                self.main_menu(self.flag_main_menu)
                self.screen.blit(self.logo_surface, self.logo_rect)
            elif self.flag_controls_menu:
                self.controls_menu()
            elif self.flag_game:
                self.update()
                self.render()
            elif self.flag_levels:
                self.level_select(self.flag_levels)  # Отрисовка игрового поля только при flag_game = True

            self.clock.tick(60)  # Ограничение до 60 FPS # Ограничение до 60 FPS

    def main_menu(self, flag):
        self.logo_surface = pygame.image.load("textures/logo.png").convert_alpha()
        self.logo_rect = self.logo_surface.get_rect(center=(740, 150))  # Центрирование текста
        self.screen.blit(self.logo_surface, self.logo_rect)
        for button in self.buttons_menu:
            clicked_button = button.update(self.mousePos, self.is_clicked)
            if clicked_button is not None:
                if flag:
                    if clicked_button == 'startButton':
                        print('start button pressed!')
                        self.flag_game = True
                        self.flag_main_menu = False
                    elif clicked_button == 'exitButton':
                        print('exit button pressed!')
                        sys.exit()
                    elif clicked_button == 'settings_button':
                        self.flag_controls_menu = True
                        self.flag_main_menu = False
                    elif clicked_button == 'level_select':
                        self.flag_main_menu = False
                        self.flag_levels = True

        pygame.display.flip()

    def level_select(self, flag):
        self.screen.fill("black")
        print('ПРОВЕРКА')
        for button in self.buttons_levels:
            button.name = 0
            clicked_button = button.update(self.mousePos, self.is_clicked)
            if clicked_button is not None:
                if flag:
                    if clicked_button == 'first':
                        print('first level selected')
                        self.flag_game = True
                        self.flag_main_menu = False
                    elif clicked_button == 'second':
                        print('exit button pressed!')
                        sys.exit()
                    elif clicked_button == 'settings_button':
                        self.flag_controls_menu = True
                        self.flag_main_menu = False
                    elif clicked_button == 'level_select':
                        self.flag_main_menu = False
                        self.flag_levels = True
        pygame.display.flip()



    def controls_menu(self):
        self.screen.fill("black")

        # Открытие изображения на весь экран
        controls_image = pygame.image.load(
            "textures/controls_image.png").convert_alpha()  # Замените на ваше изображение
        controls_image = pygame.transform.scale(controls_image, (1480, 1024))
        self.screen.blit(controls_image, (0, 0))

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
                if self.button_option_rect.collidepoint(pygame.mouse.get_pos()) and self.flag_main_menu and \
                        pygame.mouse.get_pressed()[0]:
                    self.flag_controls_menu = True
                    self.flag_main_menu = False
                if self.button_exit_rect.collidepoint(pygame.mouse.get_pos()) and self.flag_main_menu and \
                        pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    sys.exit()
            if hasattr(self, 'button_back_rect'):
                print(self.button_back_rect)
                if self.flag_controls_menu and self.button_back_rect.collidepoint(pygame.mouse.get_pos()) and \
                        pygame.mouse.get_pressed()[0]:
                    self.flag_controls_menu = False
                    self.flag_main_menu = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.flag_game is True:
                        self.flag_game = False
                        self.flag_main_menu = True
                    if self.flag_controls_menu is True:
                        self.flag_controls_menu = False
                        self.flag_main_menu = True
                    if self.flag_levels is True:
                        self.flag_levels = False
                        self.flag_main_menu = True
                if self.flag_game:
                    self.player.speed_x = self.player.speed_y = 1
                    if keys[pygame.K_LEFT]:
                        if self.player.position[0] >= 0:
                            self.player.position[0] -= self.player.speed_x
                            self.player.sprite_player.rect.x -= self.player.speed_x
                    if keys[pygame.K_RIGHT]:
                        if self.player.position[0] <= 700:
                            self.player.position[0] += self.player.speed_x
                            self.player.sprite_player.rect.x += self.player.speed_x
                    if keys[pygame.K_UP]:
                        if self.player.position[1] >= 0:
                            self.player.position[1] -= self.player.speed_y
                            self.player.sprite_player.rect.y -= self.player.speed_y
                    if keys[pygame.K_DOWN]:
                        if self.player.position[1] <= 450:
                            self.player.position[1] += self.player.speed_y
                            self.player.sprite_player.rect.y += self.player.speed_y
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.flag_game = False
                            self.flag_main_menu = True
                        if self.flag_game:
                            if event.key == pygame.K_LEFT:
                                self.player.sprite_player.image = pygame.transform.rotate(
                                    pygame.image.load("textures/crowbar.png"), 270)
                                if self.player.sprite_player.rect.x > 25:
                                    self.move("x", -50)
                            if event.key == pygame.K_RIGHT:
                                self.player.sprite_player.image = pygame.transform.rotate(
                                    pygame.image.load("textures/crowbar.png"), 90)
                                if self.player.sprite_player.rect.x < self.screen.get_rect()[2] - 75:
                                    self.move("x", 50)
                            if event.key == pygame.K_UP:
                                self.player.sprite_player.image = pygame.transform.rotate(
                                    pygame.image.load("textures/crowbar.png"), 180)
                                if self.player.sprite_player.rect.y > 25:
                                    self.move("y", -50)
                            if event.key == pygame.K_DOWN:
                                self.player.sprite_player.image = pygame.image.load("textures/crowbar.png")
                                if self.player.sprite_player.rect.y < self.screen.get_rect()[3] - 75:
                                    self.move("y", 50)

    def update(self):
        self.player.update(self.screen)
        pygame.display.flip()

    def render(self):
        self.screen.fill("black")
        self.board.render(self.screen)

    def update_db(self, db_name, file_info, id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Удаляем все данные из таблицы levels
        cursor.execute('''
            DELETE FROM levels
        ''')

        # Вставляем новые данные
        cursor.execute('''
            INSERT INTO levels (name, path, id) VALUES (?, ?, ?)
        ''', (file_info['name'], file_info['path'], id))

        conn.commit()
        conn.close()

    def find_files_in_directory(self, directory, db_name):
        counter = 0
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_info = {
                    'name': filename,
                    'path': file_path
                }
                print(db_name, file_info)
                self.update_db(db_name, file_info, counter)
                self.level_dict[file_info['name']] = file_info['path']
                counter += 1
                if counter >= 6:
                    break


class Button:
    def __init__(self, screen, x, y, width, height, label, name, text='Button', text_color='black'):
        self.screen = screen
        self.label = label
        self.name = name
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text_image = self.label.render(text, True, text_color)
        self.text_image_rect = self.text_image.get_rect()

        self.back_colors = {
            'normal': (21, 140, 0),
            'hover': (255, 255, 255),
            'clicked': (0, 100, 0)
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_image_rect.center = self.width / 2, self.height / 2

        self.is_pressed = False

    def update(self, mouse_pos, is_clicked):
        res = False

        if self.button_rect.collidepoint(mouse_pos) and is_clicked:
            self.button_surface.fill(self.back_colors['clicked'])
            self.is_pressed = True  # состояние зажатия кнопки
        elif self.button_rect.collidepoint(mouse_pos):
            if self.is_pressed:  # если кнопку кликнули (зажали и отпустили)
                res = True
                self.is_pressed = False
            else:
                self.button_surface.fill(self.back_colors['hover'])
        else:
            self.is_pressed = False
            self.button_surface.fill(self.back_colors['normal'])

        self.button_surface.blit(self.text_image, self.text_image_rect)  # отображение текста на поверхности кнопки
        self.screen.blit(self.button_surface, self.button_rect)  # отображение поверхности кнопки на экране

        if res:
            return self.name


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        if tile_type == 'empty':
            self.image = pygame.image.load("textures/floor_tile.png").convert_alpha()
        elif tile_type == "furniture":
            self.image = pygame.image.load("textures/floor_tile.png").convert_alpha()
        self.rect = self.image.get_rect().move(
            50 * pos_x, 50 * pos_y)


class Player:
    def __init__(self):
        self.position = [100, 100]  # Начальная позиция игрока
        self.speed_x = 3
        self.speed_y = 3

    def __init__(self, x_c, y_x):
        self.position = [x_c, y_x]  # Начальная позиция игрока
        self.sprite_player_group = pygame.sprite.Group()
        self.sprite_player = pygame.sprite.Sprite()
        self.sprite_player.image = pygame.image.load("textures/crowbar.png")
        self.sprite_player.rect = self.sprite_player.image.get_rect()
        self.sprite_player_group.add(self.sprite_player)
        self.sprite_player.rect.x = x_c
        self.sprite_player.rect.y = y_x

    def update(self, screen):
        self.sprite_player_group.draw(screen)

    def move(self, mode, speed):
        if mode == "x":
            self.sprite_player.rect.x += speed
        elif mode == "y":
            self.sprite_player.rect.y += speed
        pygame.display.flip()


class Board:
    def __init__(self):
        self.tiles = pygame.sprite.Group()  # Группа спрайтов для тайлов
        self.width = 0
        self.height = 0
        self.cell_size = 50  # Размер ячейки (50px)
        self.load_level_data()  # Загрузка уровня (получите уровень через метод)

    def load_level_data(self):
        self.level_data = self.load_level("mario.txt")  # Пример имени файла
        print(self.level_data)
        self.new_player, self.width, self.height = self.generate_level(self.level_data)

    def load_level(self, filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))
        level_matrix = [list(row.ljust(max_width, '.')) for row in level_map]  # Преобразование в матрицу
        return level_matrix

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    tile = Tile('empty', x, y)
                    self.tiles.add(tile)  # Добавление тайла в группу
                elif level[y][x] == '#':
                    tile = Tile('furniture', x, y)
                    self.tiles.add(tile)  # Добавление тайла в группу
                elif level[y][x] == '@':
                    tile = Tile('empty', x, y)
                    self.tiles.add(tile)  # Добавление тайла в группу
                    new_player = Player(x, y)
        return new_player, x, y

    def render(self, screen):
        screen.fill("black")
        self.tiles.draw(screen)  # Отображение всех спрайтов в группе


if __name__ == "__main__":
    game = OfficeCrusher(Player(0, 0))
    game.run()
