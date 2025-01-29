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
        self.bullets_group = pygame.sprite.Group()
        pygame.display.set_caption('Office Crusher')

        self.clock = pygame.time.Clock()
        self.flag_game = False
        self.flag_main_menu = True
        self.flag_controls_menu = False
        self.flag_levels = False
        self.player = player
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
        self.start_button = Button(self.screen, 20, 300, 450, 150, self.label, 'startButton',
                                   'Начать игру', 'black')
        self.exit_button = Button(self.screen, 20, 640, 450, 150, self.label, 'exitButton',
                                  'Выйти из игры', 'black')
        self.edit_button = Button(self.screen, 20, 470, 450, 150, self.label, 'settings_button',
                                  'Настройки', 'black')
        self.level_select_button = Button(self.screen, 20, 810, 450, 150, self.label, 'level_select',
                                          'Уровни', 'black')
        self.buttons_menu = [self.start_button, self.exit_button, self.edit_button, self.level_select_button]
        try:
            self.first_level = Button(self.screen, 50, 30, 450, 150, self.label, 'first',
                                      f'"{level_names[0][:-4]}"', 'black')
            self.second_level = Button(self.screen, 50, 230, 450, 150, self.label, 'second',
                                       f'"{level_names[1][:-4]}"', 'black')
            self.third_level = Button(self.screen, 50, 430, 450, 150, self.label, 'third',
                                      f'"{level_names[2][:-4]}"', 'black')
            self.fourth_level = Button(self.screen, 50, 630, 450, 150, self.label, 'fourth',
                                       f'"{level_names[3][:-4]}"', 'black')
            self.fifth_level = Button(self.screen, 50, 830, 450, 150, self.label, 'fifth',
                                      f'"{level_names[4][:-4]}"', 'black')
        except:
            sys.exit('Ошибка уровней: недостаточное количество уровней')

        self.buttons_levels = [self.first_level, self.second_level, self.third_level, self.fourth_level,
                               self.fifth_level]

    def move(self, dir, len):
        self.player.move(dir, len)

    def run(self):
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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.player.mode = 2 if self.player.mode == 1 else 1

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
    def __init__(self, tile_type, pos_x, pos_y, list_level):
        super().__init__()
        num_x = 512 - int(max([len(i) for i in list_level]) / 2 * 50)
        num_y = 350 - len(list_level) / 2 * 50
        if tile_type == 'empty':
            self.image = pygame.image.load("textures/floor_tile.png").convert_alpha()
        elif tile_type == "furniture":
            self.image = list_level[pos_y][pos_x].update().convert_alpha()
        self.rect = self.image.get_rect().move(
            50 * pos_x + num_x, 50 * pos_y + num_y)


class Player:
    def __init__(self):
        self.num_sprite = 0
        self.mode = 1
        self.sprite_player_group = pygame.sprite.Group()
        self.sprite_player = pygame.sprite.Sprite()
        self.sprite_player.image = pygame.image.load("textures/crowbar.png")
        self.sprite_player.rect = self.sprite_player.image.get_rect()
        self.sprite_player_group.add(self.sprite_player)
        self.position = [100, 100]
        self.screen = None
        self.board = None
        self.napravlenie = "down"
        self.dictenary_napr = {"down": [0, "y", 5], "right": [90, "x", 5], "up": [180, "y", -5], "left": [270, "x", -5]}
        self.dictenary_sprite = [pygame.image.load("textures/crowbar.png"),
                                 pygame.image.load("textures/pistol.png")]

    def update(self, screen):
        self.sprite_player.image = pygame.transform.rotate(self.dictenary_sprite[self.num_sprite],
                                                           self.dictenary_napr[self.napravlenie][0])
        self.sprite_player_group.draw(screen)

    def move(self, mode, speed):
        if mode == "x":
            self.sprite_player.rect.x += speed
        elif mode == "y":
            self.sprite_player.rect.y += speed
        pygame.display.flip()


class Board:
    def __init__(self, player):
        self.tiles = pygame.sprite.Group()  # Группа спрайтов для тайлов
        self.width = 0
        self.height = 0
        self.player = player
        self.cell_size = 50  # Размер ячейки (50px)

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

    def render(self, screen):
        screen.fill("black")
        self.tiles.draw(screen)  # Отображение всех спрайтов в группе

    def level_check(self):
        if hasattr(self, 'level_data'):
            return True
        else:
            return False


class Furniture:
    def __init__(self, number):
        self.num = int(number)
        self.protect = 2
        self.rect = None

    def update(self):
        if self.protect == 2:
            return pygame.image.load(f"textures/furniture_tile_{self.num}.png")
        return pygame.image.load(f"textures/furniture_tile_breakung_{self.num}.png")

    def __class__(self):
        return Furniture


class Bullet:
    def __init__(self, x, y, board, napravlenie):
        print(board)
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
            elif (len([i for i in board[self.y][self.x:] if type(i) == Furniture]) > 0
                  and self.sprite_bullet.rect.x >= 512 - 12 - int(max([len(i) for i in board]) / 2 * 50) + board[
                      self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0]) * 50 + 12):
                board[self.y][
                    board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])].protect -= 1
                if board[self.y][
                    board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])].protect == 0:
                    board[self.y][
                        board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])] = "."
                self.board.generate_level()
                self.sprite_bullet.kill()
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
                        [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])].protect == 0:
                    board[self.y][board[self.y].index(
                        [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])] = "."
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
                    self.x].protect -= 1
                self.sprite_bullet.kill()
                if board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                    self.x].protect == 0:
                    board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                        self.x] = "."
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
                    self.x].protect == 0:
                    board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][
                        self.x] = "."
                self.board.generate_level()
                self.sprite_bullet.kill()


if __name__ == "__main__":
    game = OfficeCrusher(Player())
    game.run()
