import pygame
import sys
import os


class OfficeCrusher:
    def __init__(self, player):
        pygame.init()

        self.screen = pygame.display.set_mode((1024, 700))
        self.screen.fill("black")
        pygame.display.set_caption('Office Crusher')
        self.clock = pygame.time.Clock()

        self.flag_game = False
        self.flag_main_menu = True
        self.flag_controls_menu = False
        self.board = Board(player)  # Инициализация класса Board
        self.player = player

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
                        self.player.sprite_player.image =\
                            pygame.transform.rotate(pygame.image.load("персонаж_вниз.png"), 180)
                        if x > 0 and self.board.level_data[y - 1][x] == ".":
                            self.board.level_data[y - 1][x] = "@"
                            self.board.level_data[y][x] = "."
                            self.move("y", -5)
                    if event.key == pygame.K_DOWN:
                        self.player.sprite_player.image = pygame.image.load("персонаж_вниз.png")
                        if y < len(self.board.level_data) and self.board.level_data[y + 1][x] == ".":
                            self.board.level_data[y + 1][x] = "@"
                            self.board.level_data[y][x] = "."
                            self.move("y", 5)

    def update(self):
        self.player.update(self.screen)
        pygame.display.flip()

    def render(self):
        self.screen.fill((255, 255, 255))  # Очистка экрана
        self.board.render(self.screen)

    def move(self, mode, speed):
        for i in range(10):
            if mode == "x":
                self.player.sprite_player.rect.x += speed
            elif mode == "y":
                self.player.sprite_player.rect.y += speed
            self.render()
            self.player.sprite_player_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, list_level):
        super().__init__()
        num_x = 512 - int(max([len(i) for i in list_level]) / 2 * 50)
        num_y = 350 - len(list_level) / 2 * 50
        if tile_type == 'empty':
            self.image = pygame.image.load("тайл пол.png").convert_alpha()
        elif tile_type == "furniture":
            self.image = pygame.image.load("мебель_тайл_1.png").convert_alpha()
        self.rect = self.image.get_rect().move(
            50 * pos_x + num_x, 50 * pos_y + num_y)


class Player:
    def __init__(self, x_c, y_x):
        self.sprite_player_group = pygame.sprite.Group()
        self.sprite_player = pygame.sprite.Sprite()
        self.sprite_player.image = pygame.image.load("персонаж_вниз.png")
        self.sprite_player.rect = self.sprite_player.image.get_rect()
        self.sprite_player_group.add(self.sprite_player)
        print(x_c, " sd")
        self.sprite_player.rect.x = x_c  # Начальная позиция игрока
        self.sprite_player.rect.y = y_x

    def update(self, screen):
        self.sprite_player_group.draw(screen)


class Board:
    def __init__(self, player):
        self.tiles = pygame.sprite.Group()  # Группа спрайтов для тайлов
        self.width = 0
        self.height = 0
        self.player = player
        self.cell_size = 50  # Размер ячейки (50px)
        self.level_data = [list(i) for i in self.load_level("level.txt")]  # Пример имени файла
        self.load_level_data()  # Загрузка уровня (получите уровень через метод)

    def load_level_data(self):
        self.width, self.height = self.generate_level(self.level_data)

    def load_level(self, filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

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
                    self.player.sprite_player.rect.x = \
                        512 - int(max([len(i) for i in level]) / 2 * 50) + x * 50
                    self.player.sprite_player.rect.y = \
                        350 - len(level) / 2 * 50 + y * 50
        return x, y

    def render(self, screen):
        self.tiles.draw(screen)  # Отображение всех спрайтов в группе


if __name__ == "__main__":
    game = OfficeCrusher(Player(0, 0))
    game.run()
