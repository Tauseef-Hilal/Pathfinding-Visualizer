"""
    button.py
    Contains Button class
"""

import pygame

from src.constants import BLACK, HEIGHT, WIDTH


class Button:
    """Model a button"""

    def __init__(
            self,
            text: str,
            x: float | str,
            y: float | str,
            padding: float = 5,
            font_size: int = 20,
            bold: bool = False,
            outline: bool = False,
            foreground_color: pygame.Color = pygame.Color(0, 0, 0),
            background_color: pygame.Color = pygame.Color(255, 255, 255)
    ):
        self.text = text
        self.padding = padding
        self.background_color = background_color
        self.outline = outline

        font = pygame.font.SysFont("Verdana", font_size, bold)

        self.text_surf = font.render(
            self.text, True, foreground_color
        )
        self.text_rect = self.text_surf.get_rect()

        if x == "center":
            x = (WIDTH - self.text_surf.get_width()) / 2

        if y == "center":
            y = (HEIGHT - self.text_surf.get_height()) / 2

        self.rect = pygame.Rect(
            float(x), float(y), self.text_rect.width +
            padding * 2, self.text_rect.height + padding * 2
        )

        self.text_rect.topleft = self.rect.x + padding, self.rect.y + padding

    def draw(self, surf: pygame.surface.Surface):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # Draw button
        pygame.draw.rect(surf, self.background_color, self.rect)
        if self.outline:
            pygame.draw.rect(surf, BLACK, self.rect, width=self.outline)

        text_x, text_y = self.rect.x + self.padding, self.rect.y + self.padding
        surf.blit(self.text_surf, (text_x, text_y))

        return action
