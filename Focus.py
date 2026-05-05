import pygame
import sys

#initialize pygame
pygame.init()

#set window dimensions
screen = pygame.display.set_mode((500, 650))

#side menu
MENU_WIDTH = 169
MENU_HEIGHT = 650
MENU_SPEED = 20
menu_x = -MENU_WIDTH
menu_open = False

#images
logo_image = pygame.image.load('logo.png')
logo_image = pygame.transform.scale(logo_image, (241, 113))
menuline = pygame.image.load('sidemenuline.png')
menuline = pygame.transform.scale(menuline, (147, 1))


class ButtonExit(object):
    def __init__(self, position, size, filename):
        # load image
        self.normal_image = pygame.image.load(filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        # create hover image by darkening the button
        self.hover_image = self.normal_image.copy()
        self.hover_image.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGBA_SUB)
        # create collision
        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        if self.rect.collidepoint(position):
            pygame.quit()
            sys.exit()

class SelectPuzzleButton(object):
    def __init__(self, position, size, filename):
        # load image
        self.normal_image = pygame.image.load(filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        # create hover image by darkening the button
        self.hover_image = self.normal_image.copy()
        self.hover_image.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGBA_SUB)
        # create collision
        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

class MenuButton(object):
    def __init__(self, position, size, filename):
        # load image
        self.normal_image = pygame.image.load(filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        # create hover image by darkening the button
        self.hover_image = self.normal_image.copy()
        self.hover_image.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGBA_SUB)
        # create collision
        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

class AccountButton(object):
    def __init__(self, position, size, filename):
        # load image
        self.normal_image = pygame.image.load(filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        # create hover image by darkening the button
        self.hover_image = self.normal_image.copy()
        self.hover_image.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGBA_SUB)
        # create collision
        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

class HowtoPButton(object):
    def __init__(self, position, size, filename):
        # load image
        self.normal_image = pygame.image.load(filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        # create hover image by darkening the button
        self.hover_image = self.normal_image.copy()
        self.hover_image.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGBA_SUB)
        # create collision
        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

class backHomeButton(object):
    def __init__(self, position, size, filename):
        # load image
        self.normal_image = pygame.image.load(filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        # create hover image by darkening the button
        self.hover_image = self.normal_image.copy()
        self.hover_image.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGBA_SUB)
        # create collision
        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        if self.rect.collidepoint(position):
            return True
        return False
#buttons
ExitButton = ButtonExit((139, 424), (221, 65), 'exitButton.png')
SelectPuzzleButton = SelectPuzzleButton((139, 270), (221, 65), 'selectPuzzleButton.png')
MenuButton = MenuButton((18, 18), (24, 24), 'menu.png')
AccountButton = AccountButton((3, 88), (94, 24), 'account.png')
HowtoPButton = HowtoPButton((3, 163), (115, 20), 'howtoplay.png')
backHomeButton = backHomeButton((139, 14), (24, 24), 'backhome.png')
#screen state
current_screen = 'main_menu'

#main loop
running = True
while running:
    #handles events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            ExitButton.check_press(mouse_pos)
            
            if current_screen == 'main_menu':
                if SelectPuzzleButton.check_press(mouse_pos):
                    current_screen = 'select_puzzle'
                if AccountButton.check_press(mouse_pos):
                    current_screen = 'account_page'
            if HowtoPButton.check_press(mouse_pos):
                    pass  # Implement how to play screen later
            if backHomeButton.check_press(mouse_pos):
                current_screen = 'main_menu'
            if MenuButton.check_press(mouse_pos):
                menu_open = not menu_open
    mouse_pos = pygame.mouse.get_pos()
    ExitButton.update(mouse_pos)
    SelectPuzzleButton.update(mouse_pos)
    MenuButton.update(mouse_pos)
    AccountButton.update(mouse_pos)
    #draws screen
    screen.fill((255, 255, 255))

    if current_screen == 'main_menu':
        screen.blit(logo_image, (130, 45))
        ExitButton.draw(screen)
        SelectPuzzleButton.draw(screen)
        MenuButton.draw(screen)

    elif current_screen == 'select_puzzle':
        screen.fill((255, 255, 255))
        screen.blit(logo_image, (130, 45))
        ExitButton.draw(screen)

    elif current_screen == 'account_page':
        screen.fill((25, 255, 255))
        screen.blit(logo_image, (130, 45))
        ExitButton.draw(screen)

    # animate menu
    if menu_open and menu_x < 0:
        menu_x += MENU_SPEED
        if menu_x > 0:
            menu_x = 0
    elif not menu_open and menu_x > -MENU_WIDTH:
        menu_x -= MENU_SPEED
        if menu_x < -MENU_WIDTH:
            menu_x = -MENU_WIDTH

    # draw menu
    pygame.draw.rect(screen, (255, 255, 255), (menu_x, 0, MENU_WIDTH, MENU_HEIGHT))
    if menu_x > -MENU_WIDTH:
        font = pygame.font.SysFont(None, 24)
        MenuButton.draw(screen)
        screen.blit(menuline, (11, 52))
        AccountButton.draw(screen)
        HowtoPButton.draw(screen)
        backHomeButton.draw(screen)
        #MUSIC WILL BE ADDED LATER

    pygame.display.flip()

pygame.quit()
sys.exit()