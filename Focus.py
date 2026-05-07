import pygame
import sys

# initialize pygame
pygame.init()

WIDTH, HEIGHT = 500, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

MENU_WIDTH = 169
MENU_HEIGHT = HEIGHT
MENU_SPEED = 20

logo_image = pygame.image.load('logo.png')
logo_image = pygame.transform.scale(logo_image, (241, 113))
menuline = pygame.image.load('sidemenuline.png')
menuline = pygame.transform.scale(menuline, (147, 1))
welcomuser = pygame.image.load('welcome.png')
welcomuser = pygame.transform.scale(welcomuser, (255, 39))


class Button:
    def __init__(self, position, size, filename):
        self.normal_image = pygame.image.load(filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)

        self.hover_image = self.normal_image.copy()
        self.hover_image.fill(
            (40, 40, 40, 0),
            special_flags=pygame.BLEND_RGBA_SUB,
        )

        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        return self.rect.collidepoint(position)
class ExitButton(Button):
    def check_press(self, position):
        if super().check_press(position):
            pygame.quit()
            sys.exit()


def main():
    menu_x = -MENU_WIDTH
    menu_open = False
    current_screen = 'main_menu'

    exit_button = ExitButton((139, 424), (221, 65), 'exitButton.png')
    select_puzzle_button = Button((139, 270), (221, 65), 'selectPuzzleButton.png')
    menu_button = Button((18, 18), (24, 24), 'menu.png')
    account_button = Button((3, 88), (94, 24), 'account.png')
    howto_button = Button((3, 163), (115, 20), 'howtoplay.png')
    back_home_button = Button((139, 14), (24, 24), 'backhome.png')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                exit_button.check_press(mouse_pos)
                menu_button.check_press(mouse_pos)

                if current_screen == 'main_menu':
                    if select_puzzle_button.check_press(mouse_pos):
                        current_screen = 'select_puzzle'
                    if account_button.check_press(mouse_pos):
                        current_screen = 'account_page'
                if current_screen in ['select_puzzle', 'account_page']:
                    if account_button.check_press(mouse_pos):
                        current_screen = 'account_page'

                if howto_button.check_press(mouse_pos):
                    pass  # Implement how to play screen later

                if back_home_button.check_press(mouse_pos):
                    current_screen = 'main_menu'

                if menu_button.check_press(mouse_pos):
                    menu_open = not menu_open

        mouse_pos = pygame.mouse.get_pos()

        exit_button.update(mouse_pos)
        select_puzzle_button.update(mouse_pos)
        menu_button.update(mouse_pos)
        account_button.update(mouse_pos)
        howto_button.update(mouse_pos)
        back_home_button.update(mouse_pos)

        screen.fill((255, 255, 255))

        if current_screen == 'main_menu':
            screen.blit(logo_image, (130, 45))
            exit_button.draw(screen)
            select_puzzle_button.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'select_puzzle':
            screen.fill((255, 255, 255))
            screen.blit(logo_image, (130, 45))
            exit_button.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'account_page':
            screen.fill((255, 255, 255))
            screen.blit(welcomuser, (21, 61))
            exit_button.draw(screen)
            menu_button.draw(screen)

        if menu_open and menu_x < 0:
            menu_x += MENU_SPEED
            if menu_x > 0:
                menu_x = 0
        elif not menu_open and menu_x > -MENU_WIDTH:
            menu_x -= MENU_SPEED
            if menu_x < -MENU_WIDTH:
                menu_x = -MENU_WIDTH

        pygame.draw.rect(screen, (255, 255, 255), (menu_x, 0, MENU_WIDTH, MENU_HEIGHT))
        if menu_x > -MENU_WIDTH:
            font = pygame.font.SysFont(None, 24)
            menu_button.draw(screen)
            screen.blit(menuline, (11, 52))
            account_button.draw(screen)
            howto_button.draw(screen)
            back_home_button.draw(screen)
            # MUSIC WILL BE ADDED LATER

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
