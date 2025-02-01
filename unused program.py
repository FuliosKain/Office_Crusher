import pygame
import sqlite3
import os
import sys
from screeninfo import get_monitors


width, height = get_monitors()[0].width, get_monitors()[0].height
print(width, height)


class OfficeCrusher:
    def __init__(self, player):
        pygame.init()
        self.screen_size = (width, height)  # 1480 1024
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill("black")
        print(self.screen)
        self.bullets_group = pygame.sprite.Group()
        pygame.display.set_caption('Office Crusher')

        self.clock = pygame.time.Clock()
        self.flag_game = False
        self.flag_main_menu = True
        self.flag_controls_menu = False
        self.flag_levels = False
        self.board = Board(player)  # Инициализация класса Board
        self.player = player
        self.player.board = self.board
        self.level_dict = dict()
        directory_path = 'data'
        database_name = 'levels'
        self.find_files_in_directory(directory_path, database_name)
        level_names = []
        for name in self.level_dict:
            level_names.append(name)

        self.mousePos = pygame.mouse.get_pos()
        self.is_clicked = pygame.mouse.get_pressed(num_buttons=5)[0]

        self.label = pygame.font.Font("Inky-Thin-Pixels_0.ttf", 45)
        self.start_button = Button(self.screen, width * 0.0135, height * 0.293, width * 0.304, height * 0.146,
                                   self.label, 'startButton', 'Начать игру', 'black')
        self.exit_button = Button(self.screen, width * 0.0135, height * 0.625, width * 0.30, height * 0.146, self.label,
                                  'exitButton', 'Выйти из игры', 'black')
        self.edit_button = Button(self.screen, width * 0.0135, height * 0.458, width * 0.30, height * 0.146,
                                  self.label, 'settings_button', 'Настройки', 'black')
        self.level_select_button = Button(self.screen, width * 0.0135, height * 0.791, width * 0.30, height * 0.146,
                                          self.label, 'level_select', 'Уровни', 'black')
        self.buttons_menu = [self.start_button, self.exit_button, self.edit_button, self.level_select_button]
        try:
            self.first_level = Button(self.screen, width * 0.034, height * 0.03, width * 0.304, height * 0.146,
                                      self.label, 'first', f'"{level_names[0][:-4]}"', 'black')
            self.second_level = Button(self.screen, width * 0.034, height * 0.224, width * 0.304, height * 0.146,
                                       self.label, 'second', f'"{level_names[1][:-4]}"', 'black')
            self.third_level = Button(self.screen, width * 0.034, height * 0.419, width * 0.304, height * 0.146,
                                      self.label, 'third', f'"{level_names[2][:-4]}"', 'black')
            self.fourth_level = Button(self.screen, width * 0.034, height * 0.615, width * 0.304, height * 0.146,
                                       self.label, 'fourth', f'"{level_names[3][:-4]}"', 'black')
            self.fifth_level = Button(self.screen, width * 0.034, height * 0.81, width * 0.304, height * 0.146,
                                      self.label, 'fifth', f'"{level_names[4][:-4]}"', 'black')
        except:
            sys.exit('Ошибка уровней: недостаточное количество уровней')

        self.buttons_levels = [self.first_level, self.second_level, self.third_level, self.fourth_level,
                               self.fifth_level]

    def run(self):
        while True:
            self.handle_events()
            self.mousePos = pygame.mouse.get_pos()
            self.is_clicked = pygame.mouse.get_pressed(num_buttons=5)[0]
            # print(self.flag_game, self.flag_main_menu, self.flag_controls_menu, self.flag_levels)
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
        self.logo_rect = self.logo_surface.get_rect(center=(width * 0.5, height * 0.146))  # Центрирование текста
        self.screen.blit(self.logo_surface, self.logo_rect)
        for button in self.buttons_menu:
            clicked_button = button.update(self.mousePos, self.is_clicked)
            if clicked_button is not None:
                if flag:
                    if clicked_button == 'startButton' and hasattr(self, 'board'):
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
            level_name = f'{button.check_text()[1:-1]}.txt'
            clicked_button = button.update(self.mousePos, self.is_clicked)
            if clicked_button is not None:
                if flag:
                    if clicked_button == 'first':
                        print('')
                        print('FPFPF')
                        print()
                        self.board = Board(self.player)
                        self.board.load_level(level_name)
                    elif clicked_button == 'second':
                        self.board = Board(self.player)
                        self.board.load_level(level_name)
                    elif clicked_button == 'third':
                        self.board = Board(self.player)
                        self.board.load_level(level_name)
                    elif clicked_button == 'fourth':
                        self.board = Board(self.player)
                        self.board.load_level(level_name)
                    elif clicked_button == 'fifth':
                        self.board = Board(self.player)
                        self.board.load_level(level_name)

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if self.player.mode == 0:
                    self.player.mode = self.player.num_sprite = 1
                else:
                    self.player.mode = self.player.num_sprite = 0
            if self.flag_game and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.player.mode == 0:
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    if self.player.napravlenie == "left":
                        if x > 0 and type(self.board.level_data[y][x - 1]) == Furniture:
                            self.player.num_sprite = 0
                            self.board.level_data[y][x - 1].protect -= 2
                            if self.board.level_data[y][x - 1].protect <= 0:
                                self.board.level_data[y][x - 1] = "."
                    elif self.player.napravlenie == "right":
                        if x + 1 < len(self.board.level_data[y]) and type(self.board.level_data[y][x + 1]) == Furniture:
                            self.player.num_sprite = 0
                            self.board.level_data[y][x + 1].protect -= 2
                            if self.board.level_data[y][x + 1].protect <= 0:
                                self.board.level_data[y][x + 1] = "."
                    elif self.player.napravlenie == "up":
                        if y > 0 and type(self.board.level_data[y - 1][x]) == Furniture:
                            self.player.num_sprite = 0
                            self.board.level_data[y - 1][x].protect -= 2
                            if self.board.level_data[y - 1][x].protect <= 0:
                                self.board.level_data[y - 1][x] = "."
                    elif self.player.napravlenie == "down":
                        if y + 1 < len(self.board.level_data) and type(self.board.level_data[y + 1][x]) == Furniture:
                            self.player.num_sprite = 0
                            self.board.level_data[y + 1][x].protect -= 2
                            if self.board.level_data[y + 1][x].protect <= 0:
                                self.board.level_data[y + 1][x] = "."
                elif self.player.mode == 1 and len(self.bullets_group) == 0:
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    if self.player.napravlenie == "right":
                        self.bullet = Bullet(x, y, self.board, "right", self.player.size)
                    elif self.player.napravlenie == "left":
                        self.bullet = Bullet(x, y, self.board, "left", self.player.size)
                    elif self.player.napravlenie == "up":
                        self.bullet = Bullet(x, y, self.board, "up", self.player.size)
                    elif self.player.napravlenie == "down":
                        self.bullet = Bullet(x, y, self.board, "down", self.player.size)
                    self.bullets_group.add(self.bullet.sprite_bullet)
                    self.bullets_group.draw(self.screen)
                    self.player.num_sprite = 1
                self.board.generate_level()
            if event.type == pygame.KEYDOWN:
                print(pygame.K_ESCAPE)
                print(event.key)
                if event.key == pygame.K_ESCAPE:
                    print('pobeg')
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
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.player.napravlenie = "left"
                        if x > 0 and self.board.level_data[y][x - 1] == ".":
                            self.board.level_data[y][x - 1] = "@"
                            self.board.level_data[y][x] = "."
                            self.player.move()
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.player.napravlenie = "right"
                        if x + 1 < len(self.board.level_data[y]) and self.board.level_data[y][x + 1] == ".":
                            self.board.level_data[y][x + 1] = "@"
                            self.board.level_data[y][x] = "."
                            self.player.move()
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        self.player.napravlenie = "up"
                        if y > 0 and self.board.level_data[y - 1][x] == ".":
                            self.board.level_data[y - 1][x] = "@"
                            self.board.level_data[y][x] = "."
                            self.player.move()
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.player.napravlenie = "down"
                        if y + 1 < len(self.board.level_data) and self.board.level_data[y + 1][x] == ".":
                            self.board.level_data[y + 1][x] = "@"
                            self.board.level_data[y][x] = "."
                            self.player.move()

    def update(self):
        self.player.update(self.screen)
        pygame.display.flip()

    def render(self):
        self.screen.fill("black")
        self.board.render(self.screen)
        if len(self.bullets_group) > 0:
            self.bullet.update()
            self.bullets_group.draw(self.screen)

    def update_db(self, db_name, file_info, id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Удаляем все данные из таблицы levels

        # Вставляем новые данные
        cursor.execute('''
            INSERT INTO levels (name, path, id) VALUES (?, ?, ?)
        ''', (file_info['name'], file_info['path'], id))

        conn.commit()
        conn.close()

    def find_files_in_directory(self, directory, db_name):
        counter = 0
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM levels
        ''')
        conn.commit()
        conn.close()
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
        self.btn_text = text
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text_image = self.label.render(self.btn_text, True, text_color)
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

    def check_text(self):
        return self.btn_text

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
    def __init__(self, tile_type, pos_x, pos_y, list_level, size=50):
        super().__init__()
        num_x = width * 0.5 - int(max([len(i) for i in list_level]) / 2 * size)
        num_y = height * 0.5 - len(list_level) / 2 * size
        if tile_type == 'empty':
            self.image = pygame.transform.scale(pygame.image.load("textures/floor_tile.png"),
                                                (size, size)).convert_alpha()
        elif tile_type == "furniture":
            self.image = list_level[pos_y][pos_x].update().convert_alpha()
        self.rect = self.image.get_rect().move(
            size * pos_x + num_x, size * pos_y + num_y)


class Player:
    def __init__(self):
        self.num_sprite = 0
        self.mode = 0
        self.sprite_player_group = pygame.sprite.Group()
        self.sprite_player = pygame.sprite.Sprite()
        self.sprite_player.image = pygame.image.load("textures/crowbar.png")
        self.sprite_player.rect = self.sprite_player.image.get_rect()
        self.sprite_player_group.add(self.sprite_player)
        self.screen = None
        self.board = None
        self.size = 50
        self.napravlenie = "down"
        self.dictenary_napr = {"down": [0, "y", self.size], "right": [90, "x", self.size], "up": [180, "y", -self.size],
                               "left": [270, "x", -self.size]}
        self.dictenary_sprite = [pygame.transform.scale(pygame.image.load("textures/crowbar.png"),
                                                        (self.size, self.size)),
                                 pygame.image.load("textures/pistol.png")]

    def update(self, screen):
        self.sprite_player.image = pygame.transform.rotate(self.dictenary_sprite[self.num_sprite],
                                                           self.dictenary_napr[self.napravlenie][0])
        self.sprite_player_group.draw(screen)

    def move(self):
        if self.dictenary_napr[self.napravlenie][1] == "x":
            self.sprite_player.rect.x += self.dictenary_napr[self.napravlenie][2]
        elif self.dictenary_napr[self.napravlenie][1] == "y":
            self.sprite_player.rect.y += self.dictenary_napr[self.napravlenie][2]
        pygame.display.flip()

    def set_size(self, size):
        self.size = size
        self.dictenary_napr = {"down": [0, "y", self.size], "right": [90, "x", self.size], "up": [180, "y", -self.size],
                               "left": [270, "x", -self.size]}
        self.dictenary_sprite = [pygame.transform.scale(pygame.image.load("textures/crowbar.png"),
                                                        (self.size, self.size)),
                                 pygame.transform.scale(pygame.image.load("textures/pistol.png"),
                                                        (self.size, self.size))]


class Board:
    def __init__(self, player):
        self.tiles = pygame.sprite.Group()  # Группа спрайтов для тайлов
        self.width = 0
        self.height = 0
        self.player = player
        self.level_data = None
        self.cell_size = 100  # Размер ячейки (50px)

    def load_level(self, filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))
        filename = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        self.level_data = [list(i) for i in filename]  # Пример имени файла
        for y in range(len(self.level_data)):
            for x in range(len(self.level_data[y])):
                if self.level_data[y][x] in "12":
                    self.level_data[y][x] = Furniture(self.level_data[y][x])
        self.generate_level()  # Загрузка уровня (получите уровень через метод)

    def generate_level(self):
        size = height / len(self.level_data)
        if max(len(i) for i in self.level_data) * size > width:
            size = width / max(len(i) for i in self.level_data)
        size = int(size)
        level = self.level_data
        for i in self.tiles:
            i.kill()
        for y in range(len(level)):
            for x in range(len(level[y])):
                tile = Tile('empty', x, y, level, size)
                self.tiles.add(tile)  # Добавление тайла в группу
                if type(level[y][x]) is Furniture:
                    level[y][x].size = size
                    tile = Tile('furniture', x, y, level, size)
                    self.tiles.add(tile)  # Добавление тайла в группу
                elif level[y][x] == '@':
                    self.player.set_size(size)
                    self.player.sprite_player.rect.x = \
                        width * 0.5 - int(max([len(i) for i in level]) / 2 * size) + x * size
                    self.player.sprite_player.rect.y = \
                        int(height * 0.5 - len(level) / 2 * size + y * size)

    def render(self, screen):
        screen.fill("black")
        self.player.update(screen)
        self.tiles.draw(screen)  # Отображение всех спрайтов в группе

    def level_check(self):
        if hasattr(self, 'level_data'):
            return True
        else:
            return False


class Furniture:
    def __init__(self, number):
        self.size = 50
        self.num = int(number)
        self.protect = 2
        self.rect = None

    def update(self):
        if self.protect == 2:
            return pygame.transform.scale(pygame.image.load(f"textures/furniture_tile_{self.num}.png"), (self.size, self.size))
        return pygame.transform.scale(pygame.image.load(f"textures/furniture_tile_breakung_{self.num}.png"), (self.size, self.size))

    def __class__(self):
        return Furniture


class Bullet:
    def __init__(self, x, y, board, napravlenie, size):
        self.size = size
        self.sprite_bullet = pygame.sprite.Sprite()
        self.num_sprite = [0, 0]
        self.list_sprites = [pygame.transform.scale(pygame.image.load("textures/bullet_1.png"),
                                                    (size * 0.5, size * 0.5)),
                             pygame.transform.scale(pygame.image.load("textures/bullet_2.png"),
                                                    (size * 0.5, size * 0.5)),
                             pygame.transform.scale(pygame.image.load("textures/bullet_3.png"),
                                                    (size * 0.5, size * 0.5))]
        self.sprite_bullet.image = self.list_sprites[self.num_sprite[0]]
        self.sprite_bullet.rect = self.sprite_bullet.image.get_rect()
        self.sprite_bullet.rect.x = \
            width * 0.5 - int(max([len(i) for i in board.level_data]) / 2 * size) + x * size + size * 0.25
        self.sprite_bullet.rect.y = \
            int(height * 0.5 - len(board.level_data) / 2 * size + y * size) + size * 0.25
        self.x = x
        self.y = y
        self.napr = napravlenie
        self.board = board

    def update(self):
        self.num_sprite[1] += 1
        self.num_sprite[0] = int(self.num_sprite[1] / 5)
        if self.num_sprite[0] == 3:
            self.num_sprite = [0, 0]
        board = self.board.level_data
        if self.napr == "right":
            self.sprite_bullet.image = pygame.transform.rotate(self.list_sprites[self.num_sprite[0]], 180)
            self.sprite_bullet.rect.x += self.size * 0.2
            if self.sprite_bullet.rect.x >= width * 0.5 + int(max([len(i) for i in board]) / 2 * self.size):
                self.sprite_bullet.kill()
            elif (len([i for i in board[self.y][self.x:] if type(i) == Furniture]) > 0
                  and self.sprite_bullet.rect.x >= width * 0.5 - 12 - int(max([len(i) for i in board]) / 2 * self.size) + board[
                      self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0]) * self.size + 12):
                board[self.y][
                    board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])].protect -= 1
                if board[self.y][
                    board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])].protect == 0:
                    board[self.y][
                        board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])] = "."
                self.board.generate_level()
                self.sprite_bullet.kill()
        elif self.napr == "left":
            self.sprite_bullet.image = pygame.transform.rotate(self.list_sprites[self.num_sprite[0]], 180)
            self.sprite_bullet.rect.x -= self.size * 0.2
            if self.sprite_bullet.rect.x <= width * 0.5 - int(max([len(i) for i in board]) / 2 * self.size):
                self.sprite_bullet.kill()
            if (len([i for i in reversed(board[self.y][:self.x]) if
                     type(i) == Furniture]) > 0 and self.sprite_bullet.rect.x <= 25 + width * 0.5 - int(
                max([len(i) for i in board]) / 2 * self.size) +
                    board[self.y].index([i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0]) * self.size):
                board[self.y][board[self.y].index(
                    [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])].protect -= 1
                if board[self.y][board[self.y].index(
                        [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])].protect == 0:
                    board[self.y][board[self.y].index(
                        [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])] = "."
                self.board.generate_level()
                self.sprite_bullet.kill()
        elif self.napr == "up":
            self.sprite_bullet.image = pygame.transform.rotate(self.list_sprites[self.num_sprite[0]], 90)
            self.sprite_bullet.rect.y -= self.size * 0.2
            if self.sprite_bullet.rect.y <= height * 0.5 - int(max([len(i) for i in board]) / 2 * self.size):
                self.sprite_bullet.kill()
            if len([i for i in reversed(board[:self.y]) if
                    type(i[self.x]) == Furniture]) > 0 and self.sprite_bullet.rect.y <= height * 0.5 - int(
                max([len(i) for i in board]) / 2 * self.size) + board.index(
                [i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0]) * self.size + self.size * 0.5:
                board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                    self.x].protect -= 1
                self.sprite_bullet.kill()
                if board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                    self.x].protect == 0:
                    board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                        self.x] = "."
                self.board.generate_level()
                self.sprite_bullet.kill()
        elif self.napr == "down":
            self.sprite_bullet.image = pygame.transform.rotate(self.list_sprites[self.num_sprite[0]], 270)
            self.sprite_bullet.rect.y += self.size * 0.2
            if self.sprite_bullet.rect.y >= height * 0.5 + int(max([len(i) for i in board]) / 2 * self.size):
                self.sprite_bullet.kill()
            if len([i for i in board[self.y:] if
                    type(i[self.x]) == Furniture]) > 0 and self.sprite_bullet.rect.y >= height * 0.5 - int(
                max([len(i) for i in board]) / 2 * self.size) + board.index(
                [i for i in board[self.y:] if
                 type(i[self.x]) == Furniture][0]) * self.size + 12:
                board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][self.x].protect -= 1
                if board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][
                    self.x].protect == 0:
                    board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][
                        self.x] = "."
                self.board.generate_level()
                self.sprite_bullet.kill()


if __name__ == "__main__":
    game = OfficeCrusher(Player())
    game.run()
