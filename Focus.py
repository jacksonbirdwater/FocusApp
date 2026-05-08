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
bgdoodles = pygame.image.load('bgdoodles.png')
bgdoodles = pygame.transform.scale(bgdoodles, (WIDTH, HEIGHT))
difftitle = pygame.image.load('difftitle.png')
difftitle = pygame.transform.scale(difftitle, (456, 150))
difficultybg = pygame.image.load('difficultybg.png')
difficultybg = pygame.transform.scale(difficultybg, (WIDTH, HEIGHT))


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
    diff_button = Button((145, 229), (221, 65), 'differences.png')
    patt_button = Button((145, 361), (221, 65), 'patterns.png')
    seq_button = Button((145, 493), (221, 65), 'sequences.png')
    homebutton = Button((455, 18), (24, 24), 'backhome.png')
    easydiffbutton = Button((129, 253), (221, 65), 'easy.png')
    meddiffbutton = Button((129, 384), (221, 65), 'med.png')
    harddiffbutton = Button((129, 515), (221, 65), 'hard.png')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Menu button is always available
                if menu_button.check_press(mouse_pos):
                    menu_open = not menu_open

                # Check buttons based on current screen
                if current_screen == 'main_menu':
                    if select_puzzle_button.check_press(mouse_pos):
                        current_screen = 'select_puzzle'
                    elif exit_button.check_press(mouse_pos):
                        pass  # Exit handled by ExitButton class
                
                elif current_screen == 'select_puzzle':
                    if diff_button.check_press(mouse_pos):
                        current_screen = 'diff_difficulty'  # We'll add this screen
                    elif patt_button.check_press(mouse_pos):
                        pass  # Implement patterns later
                    elif seq_button.check_press(mouse_pos):
                        pass  # Implement sequences later
                    elif homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'
                
                elif current_screen == 'account_page':
                    if exit_button.check_press(mouse_pos):
                        pass  # Exit handled by ExitButton class

                # Menu buttons when menu is open
                if menu_open and menu_x > -MENU_WIDTH:
                    if account_button.check_press(mouse_pos):
                        current_screen = 'account_page'
                        menu_open = False
                    elif howto_button.check_press(mouse_pos):
                        pass  # Implement how to play screen later
                    elif back_home_button.check_press(mouse_pos):
                        current_screen = 'main_menu'
                        menu_open = False

        mouse_pos = pygame.mouse.get_pos()

        # Only update buttons that are visible on current screen
        if current_screen == 'main_menu':
            exit_button.update(mouse_pos)
            select_puzzle_button.update(mouse_pos)
        elif current_screen == 'select_puzzle':
            diff_button.update(mouse_pos)
            patt_button.update(mouse_pos)
            seq_button.update(mouse_pos)
        elif current_screen == 'account_page':
            exit_button.update(mouse_pos)
        elif current_screen == 'diff_difficulty':
            easydiffbutton.update(mouse_pos)
            meddiffbutton.update(mouse_pos)
            harddiffbutton.update(mouse_pos)
        
        # Menu button is always available
        menu_button.update(mouse_pos)
        
        # Menu buttons when menu is open
        if menu_open and menu_x > -MENU_WIDTH:
            account_button.update(mouse_pos)
            howto_button.update(mouse_pos)
            back_home_button.update(mouse_pos)

        screen.fill((255, 255, 255))

        if current_screen == 'main_menu':
            screen.blit(logo_image, (130, 45))
            screen.blit(bgdoodles, (0, 0))
            exit_button.draw(screen)
            select_puzzle_button.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'select_puzzle':
            screen.fill((255, 255, 255))
            screen.blit(bgdoodles, (0, 0))
            screen.blit(logo_image, (130, 45))
            menu_button.draw(screen)
            diff_button.draw(screen)
            patt_button.draw(screen)
            seq_button.draw(screen)
            homebutton.draw(screen)

        elif current_screen == 'account_page':
            screen.fill((255, 255, 255))
            screen.blit(welcomuser, (21, 61))
            exit_button.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'diff_difficulty':
            screen.fill((255, 255, 255))
            screen.blit(difftitle, (22, 73))
            menu_button.draw(screen)
            easydiffbutton.draw(screen)
            meddiffbutton.draw(screen)
            harddiffbutton.draw(screen)
            

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
