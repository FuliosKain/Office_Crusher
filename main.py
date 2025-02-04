import pygame
import sqlite3
import os
import sys
from screeninfo import get_monitors
from particles import Particles, SimpleParticles


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
        self.flag_end_screen = False
        self.flag_game = False
        self.flag_main_menu = True
        self.flag_controls_menu = False
        self.flag_levels = False
        self.flag_stop_menu = False
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

        self.old_best_score = None
        self.score = None

        self.all_particles = []

        self.level_num = 1

        self.mousePos = pygame.mouse.get_pos()
        self.is_clicked = pygame.mouse.get_pressed(num_buttons=5)[0]
        self.score_sistem = Timer(self.screen, width * 0.1, height * 0.0286,
                                  pygame.font.Font('BlackOpsOne-Regular_RUS_by_alince.otf', 30))

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

        self.button_stop_continue = Button(self.screen, width * 0.391, height * 0.37, width * 0.219, height * 0.092,
                                      self.label, "continue", "Продолжить")
        self.button_stop_exit = Button(self.screen, width * 0.391, height * 0.509, width * 0.219, height * 0.092,
                                      self.label, "exit", "Выйти")
        self.buttons_stop_menu = [self.button_stop_exit, self.button_stop_continue]

        self.button_end_exit = Button(self.screen, width * 0.13, height * 0.8, width * 0.338, height * 0.185,
                                       self.label, "exit", "Выйти в меню")
        self.button_end_return = Button(self.screen, width * 0.531, height * 0.8, width * 0.338, height * 0.185,
                                      self.label, "return", "Переиграть")
        self.buttons_end = [self.button_end_exit, self.button_end_return]
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
                self.screen.fill("black")
                self.main_menu(self.flag_main_menu)
                self.screen.blit(self.logo_surface, self.logo_rect)
            elif self.flag_controls_menu:
                self.controls_menu()
            elif self.flag_game:
                self.update()
                self.render()
            elif self.flag_levels:
                self.level_select(self.flag_levels)  # Отрисовка игрового поля только при flag_game = True
            elif self.flag_stop_menu:
                self.stop_menu()
            elif self.flag_end_screen:
                self.end_screen()
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
                        self.player.mode = self.player.num_sprite = 0
                        self.player.napravlenie = "down"
                        self.board.generate_level()
                        self.score_sistem = Timer(self.screen, width * 0.1, height * 0.0286,
                                                  pygame.font.Font('BlackOpsOne-Regular_RUS_by_alince.otf', 30))
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
                        self.level_num = 2
                    elif clicked_button == 'second':
                        self.board = Board(self.player)
                        self.board.load_level(level_name)
                        self.level_num = 2
                    elif clicked_button == 'third':
                        self.board = Board(self.player)
                        self.board.load_level(level_name)
                        self.level_num = 3
                    elif clicked_button == 'fourth':
                        self.board = Board(self.player)
                        self.board.load_level(level_name)
                        self.level_num = 4
                    elif clicked_button == 'fifth':
                        self.board = Board(self.player)
                        self.board.load_level(level_name)
                        self.level_num = 5

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
            if self.flag_game and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.flag_stop_menu = True
                if self.flag_controls_menu and self.button_back_rect.collidepoint(pygame.mouse.get_pos()) and \
                        pygame.mouse.get_pressed()[0]:
                    self.flag_controls_menu = False
                    self.flag_main_menu = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if self.player.mode == 1:
                    self.player.weapon_update(1)
                    self.player.mode = self.player.num_sprite = 0
                else:
                    self.player.weapon_update(2)
                    self.player.mode = self.player.num_sprite = 1
            if self.flag_game and self.board.is_wined():
                #  игра после зачистки карты
                score = self.score_sistem.get_score()
                pygame.time.wait(1000)
                print(score, "dcdssc")
                with open('best_score.txt', mode='r') as file:
                    old_best_score = int(file.read())
                self.old_best_score = old_best_score
                if old_best_score > score:
                    with open('best_score.txt', mode='w') as file:
                        file.write(str(score))
                    self.old_best_score = score
                self.score = score
                self.flag_game = False
                self.flag_end_screen = True
            if self.flag_game and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.player.mode == 0:
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    size = self.player.size
                    if self.player.napravlenie == "left":
                        if x > 0 and type(self.board.level_data[y][x - 1]) == Furniture:
                            self.player.num_sprite = 0
                            self.board.level_data[y][x - 1].protect -= 2
                            pygame.mixer.Sound("windshieldsmashes2.mp3").play()

                            x_pos = (width * 0.5 - int(max([len(i) for i in self.board.level_data]) / 2 * size)
                                     + x * size)
                            y_pos = int(height * 0.5 - len(self.board.level_data) / 2 * size + y * size) + size * 0.5
                            self.all_particles.append(Particles(self.screen,
                                                                ('textures/box_particle_1.png',
                                                                 'textures/box_particle_2.png'),
                                                                15, (8, 15), (-9, 0),
                                                                pos=(x_pos, y_pos), spread_range=800))
                            if self.board.level_data[y][x - 1].protect <= 0:
                                self.board.level_data[y][x - 1] = "."
                            else:
                                self.all_particles.append(SimpleParticles(self.screen, 15, (6, 0),
                                                                          (207, 182, 142), (4, 10),
                                                                          pos=(x_pos, y_pos), spread_range=800))
                    elif self.player.napravlenie == "right":
                        if x + 1 < len(self.board.level_data[y]) and type(self.board.level_data[y][x + 1]) == Furniture:
                            self.player.num_sprite = 0
                            self.board.level_data[y][x + 1].protect -= 2
                            pygame.mixer.Sound("windshieldsmashes2.mp3").play()
                            x_pos = (width * 0.5 - int(max([len(i) for i in self.board.level_data]) / 2 * size)
                                     + x * size) + size * 0.7
                            y_pos = int(height * 0.5 - len(self.board.level_data) / 2 * size + y * size) + size * 0.5

                            if self.board.level_data[y][x + 1].protect <= 0:
                                self.board.level_data[y][x + 1] = "."
                                # создание частиц
                                self.all_particles.append(Particles(self.screen,
                                                                ('textures/box_particle_1.png', 'textures/box_particle_2.png'),
                                                                15, (8, 15), (9, 0),
                                                                pos=(x_pos, y_pos), spread_range=800))
                            else:
                                self.all_particles.append(SimpleParticles(self.screen, 15, (6, 0),
                                                                          (207, 182, 142), (4, 10),
                                                                          pos=(x_pos, y_pos), spread_range=800))

                    elif self.player.napravlenie == "up":
                        if y > 0 and type(self.board.level_data[y - 1][x]) == Furniture:
                            self.player.num_sprite = 0
                            self.board.level_data[y - 1][x].protect -= 2
                            pygame.mixer.Sound("windshieldsmashes2.mp3").play()

                            x_pos = (width * 0.5 - int(max([len(i) for i in self.board.level_data]) / 2 * size)
                                     + x * size) + size * 0.5
                            y_pos = int(height * 0.5 - len(self.board.level_data) / 2 * size + y * size)

                            if self.board.level_data[y - 1][x].protect <= 0:
                                self.board.level_data[y - 1][x] = "."
                                # создание частиц
                                self.all_particles.append(Particles(self.screen,
                                                                ('textures/box_particle_1.png', 'textures/box_particle_2.png'),
                                                                15, (8, 15), (0, -9),
                                                                pos=(x_pos, y_pos), spread_range=800))
                            else:
                                self.all_particles.append(SimpleParticles(self.screen, 15, (0, -6),
                                                                          (207, 182, 142), (4, 10),
                                                                          pos=(x_pos, y_pos), spread_range=800))
                    elif self.player.napravlenie == "down":
                        if y + 1 < len(self.board.level_data) and type(self.board.level_data[y + 1][x]) == Furniture:
                            self.player.num_sprite = 0
                            self.board.level_data[y + 1][x].protect -= 2
                            pygame.mixer.Sound("windshieldsmashes2.mp3").play()
                            x_pos = (width * 0.5 - int(max([len(i) for i in self.board.level_data]) / 2 * size)
                                     + x * size) + size * 0.5
                            y_pos = int(height * 0.5 - len(self.board.level_data) / 2 * size + y * size) + size
                            if self.board.level_data[y + 1][x].protect <= 0:
                                self.board.level_data[y + 1][x] = "."
                                # создание частиц
                                self.all_particles.append(Particles(self.screen,
                                                                ('textures/box_particle_1.png',
                                                                 'textures/box_particle_2.png'),
                                                                15, (8, 15), (0, 9),
                                                                pos=(x_pos, y_pos), spread_range=800))
                            else:
                                self.all_particles.append(SimpleParticles(self.screen, 15, (0, 6),
                                                                          (207, 182, 142), (4, 10),
                                                                          pos=(x_pos, y_pos), spread_range=800))
                elif self.player.mode == 1 and len(self.bullets_group) == 0:
                    y = self.board.level_data.index([i for i in self.board.level_data if "@" in i][0])
                    x = [i for i in self.board.level_data if "@" in i][0].index("@")
                    if self.player.napravlenie == "right":
                        self.bullet = Bullet(x, y, self.board, "right", self.all_particles, self.player.size, self.screen)
                    elif self.player.napravlenie == "left":
                        self.bullet = Bullet(x, y, self.board, "left", self.all_particles, self.player.size, self.screen)
                    elif self.player.napravlenie == "up":
                        self.bullet = Bullet(x, y, self.board, "up", self.all_particles, self.player.size, self.screen)
                    elif self.player.napravlenie == "down":
                        self.bullet = Bullet(x, y, self.board, "down", self.all_particles, self.player.size, self.screen)
                    pygame.mixer.Sound("16557_1460656892.mp3").play()
                    self.bullets_group.add(self.bullet.sprite_bullet)
                    self.bullets_group.draw(self.screen)
                    self.player.num_sprite = 1
                self.board.generate_level()
            if event.type == pygame.KEYDOWN:
                print(pygame.K_ESCAPE)
                print(event.key)
                if event.key == pygame.K_ESCAPE:
                    if self.flag_game is True:
                        self.flag_game = False
                        self.flag_stop_menu = True
                        self.player.update(self.screen)
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

    def weapon_update(self, new_value):
        self.mode = new_value # mode = индекс оружия + 1
        self.weapon_box.update_weapon(self.mode - 1)  #  смена оружия в рамке

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

    def stop_menu(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (width * 0.365, height * 0.185,
                                                  width * 0.271,  height * 0.63))
        self.score_sistem.draw_timer()
        self.score_sistem.text_update()
        for button in self.buttons_stop_menu:
            clicked_button = button.update(self.mousePos, self.is_clicked)
            if clicked_button is not None:
                if self.flag_stop_menu:
                    if clicked_button == 'continue' and hasattr(self, 'board'):
                        self.flag_game = True
                        self.flag_stop_menu = False
                    elif clicked_button == 'exit':
                        self.flag_stop_menu = False
                        self.flag_main_menu = True
        pygame.display.flip()

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

    def end_screen(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (21, 140, 0), (width * 0.239, height * 0.1,
                                                                            width * 0.521, height * 0.185))
        font = pygame.font.Font('Inky-Thin-Pixels_0.ttf', 140)
        font_result = pygame.font.Font('Inky-Thin-Pixels_0.ttf', 75)
        self.screen.blit(font.render("Ваши результаты", True, (0, 0, 0)), (width * 0.25, height * 0.115,
                                                                            width * 0.521, height * 0.185))
        self.screen.blit(font_result.render(f"Ваш результат: {self.score}", True, (21, 140, 0)),
                         (width * 0.15, height * 0.45, width * 0.8, height * 0.15))
        self.screen.blit(font_result.render(f"Лучший результат: {self.old_best_score}", True,
                                            (21, 140, 0)), (width * 0.15, height * 0.65, width * 0.8, height * 0.15))
        for button in self.buttons_end:
            clicked_button = button.update(self.mousePos, self.is_clicked)
            if clicked_button is not None:
                if self.flag_end_screen:
                    if clicked_button == 'return' and hasattr(self, 'board'):
                        self.player.mode = self.player.num_sprite = 0
                        self.player.napravlenie = "down"
                        self.board.generate_level()
                        self.score_sistem = Timer(self.screen, width * 0.1, height * 0.0286,
                                                  pygame.font.Font('BlackOpsOne-Regular_RUS_by_alince.otf', 30))
                        self.board = Board(self.player)
                        self.board.load_level(f"{self.level_num}.txt")
                        self.board.generate_level()
                        self.flag_game = True
                        self.flag_end_screen = False
                    elif clicked_button == 'exit':
                        self.flag_end_screen = False
                        self.flag_main_menu = True
                        print("end")
        pygame.display.flip()


class Timer:
    def __init__(self, screen, x_pos, y_pos, font, fps=60):
        self.screen = screen
        self.time_started = pygame.time.get_ticks()
        self.fps = fps
        self.font = font
        self.text = '00000'
        self.text_now = font.render(self.text, True, (0, 0, 0))
        self.txt_w, self.txt_h = self.text_now.get_size()
        self.width = 10  # ширина рамки
        self.frame_rect = pygame.Rect((x_pos, y_pos, self.txt_w + self.width + 25,
                                      self.txt_h + self.width + 25))
        self.text_rect = self.text_now.get_rect(center=self.frame_rect.center)
        self.delta = 0

    def delta_update(self):
        self.delta = (pygame.time.get_ticks() - self.time_started) * 50 // self.fps #  delta в два раза меньше прошедших миллисекунд

    def text_update(self):
        self.text = '0' * (5 - len(str(self.delta))) + str(self.delta)
        self.text_now = self.font.render(self.text, True, (0, 0, 0))

    def draw_timer(self):
        pygame.draw.rect(self.screen, (255, 212, 133), self.frame_rect)
        pygame.draw.rect(self.screen, 'black', self.frame_rect, width=self.width)
        self.screen.blit(self.text_now, self.text_rect)

    def update(self):
        self.delta_update()
        self.text_update()
        self.draw_timer()

    def get_score(self):
        return self.delta


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


class WeaponFrame:
    def __init__(self, imgs_pathes, size, x, y):
        print(size)
        self.size = size
        self.rect = pygame.Rect(x - size[0] / 2, y - size[1] / 2, *size)
        self.x, self.y = x, y
        self.color_in = pygame.color.Color((100, 80, 80))
        self.weapon = 0  # 0 - лом, 1 - пистолет
        self.weapon_images = [pygame.transform.scale(pygame.image.load('textures/crowbar_icon.png'), size),
                              pygame.transform.scale(pygame.image.load('textures/pistol_icon.png'), size)]
        self.weapon_img_now = self.weapon_images[self.weapon]

    def update_weapon(self, weapon_number):
        self.weapon_img_now = self.weapon_images[weapon_number]
        self.weapon = weapon_number

    def update(self, screen):
        screen.blit(self.weapon_img_now, (self.x - 25, self.y - 25))


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
        self.weapon_box = WeaponFrame(('textures/crowbar_icon.png', 'textures/pistol_icon.png'),
                                      (height * 0.1, height * 0.1), height * 0.05, height * 0.05)
        self.napravlenie = "down"
        self.dictenary_napr = {"down": [0, "y", self.size], "right": [90, "x", self.size], "up": [180, "y", -self.size],
                               "left": [270, "x", -self.size]}
        self.dictenary_sprite = [pygame.transform.scale(pygame.image.load("textures/crowbar.png"),
                                                        (self.size, self.size)),
                                 pygame.transform.scale(pygame.image.load("textures/pistol.png"),
                                                        (self.size, self.size))]

    def update(self, screen):
        self.sprite_player.image = pygame.transform.rotate(self.dictenary_sprite[self.num_sprite],
                                                           self.dictenary_napr[self.napravlenie][0])
        self.sprite_player_group.draw(screen)
        self.weapon_box.update(screen)

    def weapon_update(self, new_value):
        self.mode = new_value  # mode = индекс оружия + 1
        self.weapon_box.update_weapon(self.mode - 1)  # смена оружия в рамке

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
        self.cell_size = 50  # Размер ячейки (50px)
        self.level_data = None

    def load_level_data(self):
        self.width, self.height = self.generate_level()

    def load_level(self, filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))
        self.level_data = [list(i) for i in list(map(lambda x: x.ljust(max_width, '.'), level_map))]  # Пример имени файла
        for y in range(len(self.level_data)):
            for x in range(len(self.level_data[y])):
                if self.level_data[y][x] in "12":
                    self.level_data[y][x] = Furniture(self.level_data[y][x])

    def generate_level(self):
        if self.level_data == None:
            self.load_level("1.txt")
        x, y = 0, 0
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
        self.size = 50
        self.num = int(number)
        self.protect = 2
        self.rect = None

    def update(self):
        if self.protect == 2:
            return pygame.transform.scale(pygame.image.load(f"textures/furniture_tile_{self.num}.png"),
                                          (self.size, self.size))
        return pygame.transform.scale(pygame.image.load(f"textures/furniture_tile_breakung_{self.num}.png"),
                                      (self.size, self.size))

    def __class__(self):
        return Furniture


class Bullet:
    def __init__(self, x, y, board, napravlenie, particles, size, screen):
        self.size = size
        self.sprite_bullet = pygame.sprite.Sprite()
        self.screen = screen
        self.particles = particles
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
            self.sprite_bullet.image = pygame.transform.rotate(self.list_sprites[self.num_sprite[0]], 0)
            self.sprite_bullet.rect.x += self.size * 0.2
            if self.sprite_bullet.rect.x >= width * 0.5 + int(max([len(i) for i in board]) / 2 * self.size):
                self.sprite_bullet.kill()
            elif (len([i for i in board[self.y][self.x:] if type(i) == Furniture]) > 0
                  and self.sprite_bullet.rect.x >= width * 0.5 - 12 - int(max([len(i) for i in board]) / 2 * self.size) + board[
                      self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0]) * self.size + 12):
                board[self.y][
                    board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])].protect -= 1
                pygame.mixer.Sound("windshieldsmashes2.mp3").play()
                if board[self.y][
                    board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])].protect == 0:
                    board[self.y][
                        board[self.y].index([i for i in board[self.y][self.x:] if type(i) == Furniture][0])] = "."
                    self.particles.append(Particles(self.screen,
                                                    ('textures/box_particle_1.png', 'textures/box_particle_2.png'),
                                                    15, (8, 15), (7, 0),
                                                    pos=self.sprite_bullet.rect.center, spread_range=700))
                else:
                    self.particles.append(SimpleParticles(self.screen, 10, (4, 0),
                                                              (207, 182, 142), (2, 8),
                                                              pos=self.sprite_bullet.rect.center, spread_range=600))
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
                pygame.mixer.Sound("windshieldsmashes2.mp3").play()
                if board[self.y][board[self.y].index(
                        [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])].protect == 0:
                    board[self.y][board[self.y].index(
                        [i for i in reversed(board[self.y][:self.x]) if type(i) == Furniture][0])] = "."
                    self.particles.append(Particles(self.screen,
                                                    ('textures/box_particle_1.png', 'textures/box_particle_2.png'),
                                                    15, (8, 15), (-7, 0),
                                                    pos=self.sprite_bullet.rect.center, spread_range=700))
                else:
                    self.particles.append(SimpleParticles(self.screen, 10, (-4, 0),
                                                          (207, 182, 142), (2, 8),
                                                          pos=self.sprite_bullet.rect.center, spread_range=600))
                self.board.generate_level()
                self.sprite_bullet.kill()
        elif self.napr == "up":
            self.sprite_bullet.image = pygame.transform.rotate(self.list_sprites[self.num_sprite[0]], 90)
            self.sprite_bullet.rect.y -= self.size * 0.2
            if self.sprite_bullet.rect.y <= height * 0.5 - len(board) / 2 * self.size:
                self.sprite_bullet.kill()
            if len([i for i in reversed(board[:self.y]) if
                    type(i[self.x]) == Furniture]) > 0 and self.sprite_bullet.rect.y <= height * 0.5 - int(
                max([len(i) for i in board]) / 2 * self.size) + board.index(
                [i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0]) * self.size + self.size * 0.5:
                board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                    self.x].protect -= 1
                pygame.mixer.Sound("windshieldsmashes2.mp3").play()
                self.sprite_bullet.kill()
                if board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                    self.x].protect == 0:
                    board[board.index([i for i in reversed(board[:self.y]) if type(i[self.x]) == Furniture][0])][
                        self.x] = "."
                    self.particles.append(Particles(self.screen,
                                                    ('textures/box_particle_1.png', 'textures/box_particle_2.png'),
                                                    15, (8, 15), (0, -7),
                                                    pos=self.sprite_bullet.rect.center, spread_range=700))
                else:
                    self.particles.append(SimpleParticles(self.screen, 10, (0, -4),
                                                          (207, 182, 142), (2, 8),
                                                          pos=self.sprite_bullet.rect.center, spread_range=600))
                self.board.generate_level()
                self.sprite_bullet.kill()
        elif self.napr == "down":
            self.sprite_bullet.image = pygame.transform.rotate(self.list_sprites[self.num_sprite[0]], 270)
            self.sprite_bullet.rect.y += self.size * 0.2
            if self.sprite_bullet.rect.y >= height * 0.5 + len(board) / 2 * self.size - self.size * 0.5:
                self.sprite_bullet.kill()
            if len([i for i in board[self.y:] if
                    type(i[self.x]) == Furniture]) > 0 and self.sprite_bullet.rect.y >= height * 0.5 - int(
                max([len(i) for i in board]) / 2 * self.size) + board.index(
                [i for i in board[self.y:] if
                 type(i[self.x]) == Furniture][0]) * self.size + 12:
                board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][self.x].protect -= 1
                pygame.mixer.Sound("windshieldsmashes2.mp3").play()
                if board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][
                    self.x].protect == 0:
                    board[board.index([i for i in board[self.y:] if type(i[self.x]) == Furniture][0])][
                        self.x] = "."
                    self.particles.append(Particles(self.screen,
                                                ('textures/box_particle_1.png', 'textures/box_particle_2.png'),
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
