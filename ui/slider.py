# ui/slider.py
import pygame

class Slider:
    def __init__(self, position, width, initial_volume=0.5):
        self.x, self.y = position
        self.width = width
        self.height = 6          # track thickness
        self.handle_radius = 10
        self.volume = initial_volume
        self.dragging = False

    @property
    def handle_x(self):
        return int(self.x + self.volume * self.width)

    def handle_rect(self):
        return pygame.Rect(
            self.handle_x - self.handle_radius,
            self.y - self.handle_radius,
            self.handle_radius * 2,
            self.handle_radius * 2,
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect().collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # clamp handle within track bounds
            new_x = max(self.x, min(event.pos[0], self.x + self.width))
            self.volume = (new_x - self.x) / self.width
            pygame.mixer.music.set_volume(self.volume)

    def draw(self, surface):
        # track
        pygame.draw.rect(surface, (200, 200, 200),
                         (self.x, self.y - self.height // 2,
                          self.width, self.height), border_radius=3)
        # filled portion
        pygame.draw.rect(surface, (100, 100, 200),
                         (self.x, self.y - self.height // 2,
                          int(self.volume * self.width), self.height), border_radius=3)
        # handle
        pygame.draw.circle(surface, (80, 80, 180),
                           (self.handle_x, self.y), self.handle_radius)