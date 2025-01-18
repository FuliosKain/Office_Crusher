import pygame
import sys

size = width, height = 700, 700
screen = pygame.display.set_mode(size)


class OfficeCrusher:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Office Crusher')
        self.clock = pygame.time.Clock()
        self.state = 'menu'  # Состояние игры: menu или game
        self.menu = Menu(self)

    def run(self):
        while True:
            self.handle_events()
            if self.state == 'menu':
                self.menu.update()
                self.menu.render(self.screen)
            elif self.state == 'game':
                self.update()
                self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.state == 'menu':
                self.menu.handle_event(event)

    def update(self):
        self.board.update()

    def render(self):
        self.screen.fill((255, 255, 255))
        self.board.render(self.screen)
        pygame.display.flip()


class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Menu:
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.create_buttons()

    def create_buttons(self):
        start_button = Button("начать (1).png", (300, 200))
        management_button = Button("Управление (1).png", (300, 270))
        level_select_button = Button("уровни (1).png", (300, 340))
        self.buttons.add(start_button, management_button, level_select_button)

    def update(self):
        pass  # Можно добавить интерактивность, если нужно

    def render(self, screenchik):
        self.buttons.draw(screenchik)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
            mouse_pos = event.pos
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.image.get_rect(topleft=(300, 200)).collidepoint(mouse_pos):  # Кнопка "Начать"
                        game = OfficeCrusher()
                        game.run()
                    elif button.image.get_rect(topleft=(300, 270)).collidepoint(mouse_pos):  # Кнопка "Настройки"
                        print("Настройки")
                    elif button.image.get_rect(topleft=(300, 340)).collidepoint(mouse_pos):  # Кнопка "Выход"
                        pygame.quit()
                        sys.exit()


class Board:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.left = 50
        self.top = 50
        self.cell_size = 40

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
        self.position = [100, 100]

    def update(self):
        pass


if __name__ == "__main__":
    menu = Menu()
    menu.render(screen)