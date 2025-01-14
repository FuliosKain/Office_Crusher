import pygame
import sys



class OfficeCrusher:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Office Crusher')
        self.clock = pygame.time.Clock()

        self.board = Board()  # Инициализация класса Board

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()  # Отрисовка экрана
            self.clock.tick(60)  # Ограничение до 60 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.board.update()  # Обновление состояния объекта Board

    def render(self):
        self.screen.fill((255, 255, 255))  # Очистка экрана
        self.board.render(self.screen)  # Отрисовка уровня через метод Board
        pygame.display.flip()  # Обновление экрана


class Board:
    def __init__(self):
        self.width = 'заглушка'  # позже напишем логику где многое будет импортированно из файла уровня
        self.height = 'заглушка'
        self.left = 'заглушка'
        self.top = 'заглушка'
        self.cell_size = 'заглушка'

    def update(self):
        self.player.update()  # Обновление состояния игрока

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, 'white', (self.left + self.cell_size * col,
                                                   self.top + self.cell_size * row,
                                                   self.cell_size, self.cell_size), width=1)


class Player:
    def __init__(self):
        self.position = [100, 100]  # Начальная позиция игрока

    def update(self):
        # Здесь будет логика движения игрока
        pass


if __name__ == "__main__":
    game = OfficeCrusher()
    game.run()
