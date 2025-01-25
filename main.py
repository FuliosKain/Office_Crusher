import pygame
import sys


class OfficeCrusher:
    def __init__(self):
        pygame.init()

        self.size = self.weight, self.height = 1024, 700 # задаем размеры
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Office Crusher')

        self.clock = pygame.time.Clock()
        self.mouse_pos = pygame.mouse.get_pos()

        self.flag_game = False
        self.flag_main_menu = True
        self.flag_controls_menu = False

        self.in_process = True

        self.board = Board()  # Инициализация класса Board
        self.menu = MainMenu(self.screen)
        self.player = Player(*self.board.get_player_pos(), 5, 50)

    def run(self):
        while self.in_process:
            if self.flag_main_menu:
                self.menu.update()
            if self.flag_controls_menu:
                pass
            if self.flag_game:
                self.update() # обновление экрана помешено в одну функцию (это можно обсудить)
            self.handle_events()

            self.clock.tick(60)  # Ограничение до 60 FPS

    def handle_events(self):
        self.mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.in_process = False
                sys.exit()

        if self.menu.get_in_game() and not self.flag_game:
            self.flag_game = True
            self.flag_main_menu = False

        if self.menu.get_stop_process():
            self.in_process = False
            sys.exit()

        if keys[pygame.K_ESCAPE] and self.flag_game: #  переход из состояния игры в состояние меню
            self.flag_game = False
            self.flag_main_menu = True
            self.menu.change_in_game(False)
        if self.flag_game and not self.player.get_moving():
            x, y = self.board.get_player_board_pos()
            if keys[pygame.K_LEFT]:
                self.player.rotate(270)
                can_move = self.board.move_player(x - 1, y)
                if can_move:
                    self.player.do_move("x", -1)
            elif keys[pygame.K_RIGHT]:
                self.player.rotate(90)
                can_move = self.board.move_player(x + 1, y)
                if can_move:
                    self.player.do_move("x", 1)
            elif keys[pygame.K_UP]:
                self.player.rotate(180)
                can_move = self.board.move_player(x, y - 1)
                if can_move:
                    self.player.do_move("y", -1)
            elif keys[pygame.K_DOWN]:
                self.player.rotate(0)
                can_move = self.board.move_player(x, y + 1)
                if can_move:
                    self.player.do_move("y", 1)

        self.player.moving()

        '''for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            print(self.button_back_rect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.flag_game = False
                    self.flag_main_menu = True
                if self.flag_game:
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    if event.key == pygame.K_LEFT:
                        self.player.sprite_player.image = pygame.transform.rotate(
                            pygame.image.load("персонаж_вниз.png"), 270)
                        if x > 0 and self.board.level_data[y][x - 1] == ".":
                            self.board.level_data[y][x - 1] = "@"
                            self.board.level_data[y][x] = "."
                            self.move("x", -5)
                    if event.key == pygame.K_RIGHT:
                        self.player.sprite_player.image = pygame.transform.rotate(
                            pygame.image.load("персонаж_вниз.png"), 90)
                        if x < len(self.board.level_data[y]) and self.board.level_data[y][x + 1] == ".":
                            self.board.level_data[y][x + 1] = "@"
                            self.board.level_data[y][x] = "."
                            self.move("x", 5)
                    if event.key == pygame.K_UP:
                        self.player.sprite_player.image = \
                            pygame.transform.rotate(pygame.image.load("персонаж_вниз.png"), 180)
                        if x > 0 and self.board.level_data[y - 1][x] == ".":
                            self.board.level_data[y - 1][x] = "@"
                            self.board.level_data[y][x] = "."
                            self.move("y", -5)
                    if event.key == pygame.K_DOWN:
                        self.player.sprite_player.image = pygame.image.load("персонаж_вниз.png")
                        if y < len(self.board.leevl_data) and self.board.level_data[y + 1][x] == ".":
                            self.board.level_data[y + 1][x] = "@"
                            self.board.level_data[y][x] = "."
                            self.move("y", 5)'''

    def update(self):
        self.screen.fill((255, 255, 255))  # Очистка экрана

        self.board.render(self.screen)
        self.player.update(self.screen)

        pygame.display.flip()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    print(level_map)

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Board:
    def __init__(self):
        self.tiles = pygame.sprite.Group()  # Группа спрайтов для тайлов
        self.width = 0
        self.height = 0
        self.player_x, self.player_y = 0, 0
        self.player_board_x, self.player_board_y = 0, 0
        self.cell_size = 50  # Размер ячейки (50px)
        self.level_data = [list(i) for i in load_level("level.txt")]  # Пример имени файла
        self.load_level_data()  # Загрузка уровня (получите уровень через метод)

    def load_level_data(self):
        self.width, self.height = self.generate_level(self.level_data)

    def generate_level(self, level):
        x, y = 0, 0
        for y in range(len(level)):
            for x in range(len(level[y])):
                tile = Tile('empty', x, y, level)
                self.tiles.add(tile)  # Добавление тайла в группу
                if level[y][x] == '#':
                    tile = Tile('furniture', x, y, level)
                    self.tiles.add(tile)  # Добавление тайла в группу
                elif level[y][x] == '@':
                    self.player_x = \
                        512 - int(max([len(i) for i in level]) / 2 * 50) + x * 50
                    self.player_board_x = x
                    self.player_y = \
                        int(350 - len(level) / 2 * 50 + y * 50)
                    self.player_board_y = y
                    print(self.get_player_board_pos())
        return x, y

    def render(self, screen):
        self.tiles.draw(screen)  # Отображение всех спрайтов в группе

    def get_player_pos(self):
        return self.player_x, self.player_y #  возвращение координат игрока на экране

    def get_player_board_pos(self):
        return self.player_board_x, self.player_board_y #  возвращение координат игрока на доске

    def move_player(self, to_x, to_y):
        condition = 0 <= to_x <= self.width and 0 <= to_y <= self.height #  задание условия для передвижения игрока по вектору
        if condition and self.level_data[to_y][to_x] == '.':
            self.level_data[self.player_board_y][self.player_board_x] = '.'
            self.player_board_x = to_x
            self.player_board_y = to_y
            self.level_data[to_y][to_x] = '@'
            print('\n'.join(map(str, self.level_data)))
            return True
        return False


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, list_level):
        super().__init__()
        num_x = 512 - int(max([len(i) for i in list_level]) / 2 * 50)
        num_y = 350 - len(list_level) / 2 * 50

        self.type = tile_type

        if tile_type == 'empty':
            self.image = pygame.image.load("тайл пол.png").convert_alpha()
        elif tile_type == "furniture":
            self.image = pygame.image.load("мебель_тайл_1.png").convert_alpha()
        self.rect = self.image.get_rect().move(
            50 * pos_x + num_x, 50 * pos_y + num_y)


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.mousePos = pygame.mouse.get_pos()
        self.is_clicked = pygame.mouse.get_pressed(num_buttons=3)[0]

        self.in_game = False
        self.stop_process = False

        self.logo_surface = pygame.image.load("лого (1).png").convert_alpha()
        self.logo_rect = self.logo_surface.get_rect(center=(512, 140))  # Центрирование текста

        self.label = pygame.font.Font("BlackOpsOne-Regular_RUS_by_alince.otf", 30)
        self.start_button = Button(self.screen, 362, 270, 300, 100, self.label, 'startButton',
                                   'Начать игру', 'green')
        self.exit_button = Button(self.screen, 362, 390, 300, 100, self.label, 'exitButton',
                                   'Выйти из игры', 'red')
        self.edit_button = Button(self.screen, 362, 510, 300, 100, self.label, 'settings_button',
                                  'Настройки', 'blue')
        self.buttons = [self.start_button, self.exit_button, self.edit_button]

    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        self.is_clicked = pygame.mouse.get_pressed(num_buttons=3)[0]

        self.screen.fill('white')

        self.screen.blit(self.logo_surface, self.logo_rect)

        for button in self.buttons:
            clicked_button = button.update(self.mousePos, self.is_clicked)
            if clicked_button is not None:
                if clicked_button == 'startButton':
                    print('start button pressed!')
                    self.in_game = True
                elif clicked_button == 'exitButton':
                    print('exit button pressed!')
                    self.stop_process = True

        pygame.display.flip()

    def get_stop_process(self):
        return self.stop_process

    def get_in_game(self):
        return self.in_game

    def change_in_game(self, value):
        self.in_game = value


class Player(pygame.sprite.Sprite):
    def __init__(self, x_c, y_x, speed, distance):
        super().__init__()

        self.sprite_player_group = pygame.sprite.Group()
        self.sprite_player = pygame.sprite.Sprite()
        self.sprite_player.image = pygame.image.load("персонаж_вниз.png")
        self.default_image = self.sprite_player.image.copy()
        self.sprite_player.rect = self.sprite_player.image.get_rect()
        self.sprite_player_group.add(self.sprite_player)
        self.sprite_player.rect.x = x_c  # Начальная позиция игрока
        self.sprite_player.rect.y = y_x

        self.speed = speed

        self.rotation = 0
        self.need_iters = distance // speed
        self.direction = None
        self.mode = None
        self.iters_of_move = 0

        self.is_moving = False

    def update(self, screen):
        self.sprite_player_group.draw(screen)

    def do_move(self, mode, direction):
        """mode - ось движения ("x", "y"), direction - направление движения (1 - вперед, -1 - назад)"""

        if not self.is_moving: #  записываем параметры движения
            self.mode = mode
            self.direction = direction
            self.is_moving = True

    def moving(self):
        if self.is_moving:
            if self.mode == "x":
                self.sprite_player.rect.x += self.speed * self.direction
            elif self.mode == "y":
                self.sprite_player.rect.y += self.speed * self.direction
            self.iters_of_move += 1
        if self.iters_of_move >= self.need_iters:
            self.iters_of_move = 0
            self.is_moving = False

    def rotate(self, angle):
        if self.rotation != angle:
            self.rotation = angle
            self.sprite_player.image = pygame.transform.rotate(
                self.default_image, self.rotation)

    def get_moving(self):
        return self.is_moving


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
            'normal': (30, 30, 30),
            'hover': (100, 100, 100),
            'clicked': (200, 200, 200)
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_image_rect.center = self.width / 2, self.height / 2

        self.is_pressed = False

    def update(self, mouse_pos, is_clicked):
        res = False

        if self.button_rect.collidepoint(mouse_pos) and is_clicked:
            self.button_surface.fill(self.back_colors['clicked'])
            self.is_pressed = True # состояние зажатия кнопки
        elif self.button_rect.collidepoint(mouse_pos):
            if self.is_pressed: # если кнопку кликнули (зажали и отпустили)
                res = True
                self.is_pressed = False
            else:
                self.button_surface.fill(self.back_colors['hover'])
        else:
            self.is_pressed = False
            self.button_surface.fill(self.back_colors['normal'])

        self.button_surface.blit(self.text_image, self.text_image_rect) # отображение текста на поверхности кнопки
        self.screen.blit(self.button_surface, self.button_rect) # отображение поверхности кнопки на экране

        if res:
            return self.name


if __name__ == "__main__":
    game = OfficeCrusher()
    game.run()