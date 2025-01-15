import pygame
import sys
import os


class OfficeCrusher:
    def __init__(self, player):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill("white")
        pygame.display.set_caption('Office Crusher')
        self.clock = pygame.time.Clock()

        self.flag_game = False
        self.flag_main_menu = True
        self.board = Board()  # Инициализация класса Board
        self.player = player

    def run(self):
        while True:
            if self.flag_main_menu:
                self.main_menu()
            self.handle_events()
            if self.flag_game:
                self.update()
                self.render()  # Отрисовка экрана

            self.clock.tick(60)  # Ограничение до 60 FPS

    def main_menu(self):
        self.screen.fill("white")
        label = pygame.font.Font("BlackOpsOne-Regular_RUS_by_alince.otf", 30)
        self.button_start = label.render("Начать игру", False, (0, 255, 0), (255, 255, 255))
        if self.button_start.get_rect(topleft=(300, 250)).collidepoint(pygame.mouse.get_pos()) and self.flag_main_menu:
            self.button_start = label.render("Начать игру", False, (0, 255, 0), (200, 255, 200))
        self.screen.blit(self.button_start, (300, 250))
        self.button_end = label.render("Выйти", False, (255, 25, 0), (255, 255, 255))
        if self.button_end.get_rect(topleft=(350, 400)).collidepoint(pygame.mouse.get_pos()) and self.flag_main_menu:
            self.button_end = label.render("Выйти", False, (255, 25, 0), (255, 200, 200))
        self.screen.blit(self.button_end, (350, 400))
        pygame.display.flip()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        label = pygame.font.Font("BlackOpsOne-Regular_RUS_by_alince.otf", 30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.button_start.get_rect(topleft=(300, 250)).collidepoint(
                    pygame.mouse.get_pos()) and self.flag_main_menu and pygame.mouse.get_pressed()[0]:
                self.flag_game = True
                self.flag_main_menu = False

            elif (self.button_start.get_rect(topleft=(350, 400)).collidepoint(pygame.mouse.get_pos()) and self.flag_main_menu
                  and pygame.mouse.get_pressed()[0]):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.flag_game = False
                self.flag_main_menu = True

        if self.flag_game:
            if keys[pygame.K_LCTRL]:
                self.player.speed_x = self.player.speed_y = 5
            else:
                self.player.speed_x = self.player.speed_y = 3
            if keys[pygame.K_LEFT]:
                if self.player.position[0] >= 0:
                    self.player.position[0] -= self.player.speed_x
            if keys[pygame.K_RIGHT]:
                if self.player.position[0] <= 700:
                    self.player.position[0] += self.player.speed_x
            if keys[pygame.K_UP]:
                if self.player.position[1] >= 0:
                    self.player.position[1] -= self.player.speed_y
            if keys[pygame.K_DOWN]:
                if self.player.position[1] <= 425:
                    self.player.position[1] += self.player.speed_y

    def update(self):
        self.board.update()  # Обновление состояния объекта Board
        self.player.update(self.screen)
        pygame.display.flip()

    def render(self):
        self.screen.fill((255, 255, 255))  # Очистка экрана
        # self.board.render(self.screen)  # Отрисовка уровня через метод Board
        # Обновление экрана


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


class Player:
    def __init__(self):
        self.position = [100, 100]  # Начальная позиция игрока
        self.speed_x = 3
        self.speed_y = 3

    def update(self, screen):
        screen.blit(pygame.image.load("men.png"), self.position)


if __name__ == "__main__":
    game = OfficeCrusher(Player())
    game.run()
