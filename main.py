import pygame
import sys
import os


class OfficeCrusher:
    def __init__(self, player):
        pygame.init()

        self.size = self.weight, self.height = 800, 600 # задаем размеры
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Office Crusher')

        self.clock = pygame.time.Clock()

        self.flag_game = False
        self.flag_main_menu = True

        self.in_process = True

        self.board = Board()  # Инициализация класса Board
        self.menu = MainMenu(self.screen)
        self.player = player

    def run(self):
        while self.in_process:
            if self.flag_main_menu:
                self.menu.update()
            if self.flag_game:
                self.update() # обновление экрана помешено в одну функцию (это можно обсудить)
            self.handle_events()

            self.clock.tick(60)  # Ограничение до 60 FPS

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.in_process = False
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.flag_game = False
                self.flag_main_menu = True

        if self.menu.get_in_game():
            self.flag_game = True
            self.flag_main_menu = False
        if self.menu.get_stop_process():
            self.in_process = False
            sys.exit()

        if self.flag_game:
            if keys[pygame.K_LCTRL]:
                self.player.speed_x = self.player.speed_y = 5
            else:
                self.player.speed_x = self.player.speed_y = 3
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
                if self.player.position[1] <= 425:
                    self.player.position[1] += self.player.speed_y
                    self.player.sprite_player.rect.y += self.player.speed_y

    def update(self):
        self.screen.fill((255, 255, 255))
        self.board.update()  # Обновление состояния объекта Board
        self.player.update(self.screen)  # Очистка экрана
        # self.board.render(self.screen)
        pygame.display.flip()


class Board:
    def __init__(self):
        self.width = "заглушка"  # позже напишем логику где многое будет импортированно из файла уровня
        self.height = "заглушка"
        self.left = "заглушка"
        self.top = "заглушка"
        self.cell_size = "заглушка"

    def update(self):
        pass

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, 'white', (self.left + self.cell_size * col,
                                                   self.top + self.cell_size * row,
                                                   self.cell_size, self.cell_size), width=1)


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.mousePos = pygame.mouse.get_pos()
        self.is_clicked = pygame.mouse.get_pressed(num_buttons=3)[0]

        self.in_game = False
        self.stop_process = False

        self.label = pygame.font.Font("BlackOpsOne-Regular_RUS_by_alince.otf", 30)
        self.start_button = Button(self.screen, 30, 30, 300, 100, self.label, 'startButton',
                                   'Начать игру', 'green')
        self.exit_button = Button(self.screen, 30, 200, 300, 100, self.label, 'exitButton',
                                   'Выйти из игры', 'red')
        self.buttons = [self.start_button, self.exit_button]

    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        self.is_clicked = pygame.mouse.get_pressed(num_buttons=3)[0]

        self.screen.fill('black')

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


class Player:
    def __init__(self):
        self.position = [100, 100]  # Начальная позиция игрока
        self.speed_x = 3
        self.speed_y = 3
        self.sprite_player_group = pygame.sprite.Group()
        self.sprite_player = pygame.sprite.Sprite(self.sprite_player_group)
        self.sprite_player.image = pygame.image.load("men.png")
        self.sprite_player.rect = self.sprite_player.image.get_rect()
        self.sprite_player.rect.x = 100
        self.sprite_player.rect.y = 100

    def update(self, screen):
        self.sprite_player_group.draw(screen)


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
    game = OfficeCrusher(Player())
    game.run()