import pygame
import sys

class Button:
    def __init__(self, position, size, filename):
        self.normal_image = pygame.image.load(f"assets/images/{filename}")
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        self.hover_image = self.normal_image.copy()
        self.hover_image.fill((40, 40, 40, 0),special_flags=pygame.BLEND_RGBA_SUB  )
        self.rect = self.normal_image.get_rect(topleft=position )
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        image = (
            self.hover_image
            if self.hovered
            else self.normal_image)

        screen.blit(image, self.rect)

    def check_press(self, pos):
        return self.rect.collidepoint(pos)

class ExitButton(Button):
    def check_press(self, pos):
        if super().check_press(pos):
            pygame.quit()
            sys.exit()