import pygame

from .constants import (
    BLACK,
    WIDTH,
    HEIGHT
)


class Button:
    """Model a button (Can be used for creating labels)"""

    def __init__(
            self,
            text: str,
            x: float | str,
            y: float | str,
            padding: int = 5,
            font_size: int = 18,
            bold: bool = False,
            outline: bool = False,
            foreground_color: pygame.Color = pygame.Color(0, 0, 0),
            background_color: pygame.Color = pygame.Color(255, 255, 255)
    ) -> None:

        self.text = text
        self.padding = padding
        self.outline = outline
        self.foreground_color = foreground_color
        self.background_color = background_color

        # Render text
        if bold:
            font = pygame.font.Font("fonts/Montserrat-Bold.ttf", font_size)
        else:
            font = pygame.font.Font("fonts/Montserrat-Regular.ttf", font_size)
            
        self.text_surf = font.render(
            self.text, True, foreground_color
        )

        # Get Rect object out of the text surface
        self.text_rect = self.text_surf.get_rect()

        # Translate params: x and y if they are strings
        self.width = self.text_rect.width + padding * 2
        self.height = self.text_rect.height + padding * 2

        if x == "center":
            x = (WIDTH - self.width) / 2

        if y == "center":
            y = (HEIGHT - self.height) / 2

        # Create the actual button
        self.rect = pygame.Rect(
            float(x),
            float(y),
            self.text_rect.width + padding * 2,
            self.text_rect.height + padding * 2
        )

        self.text_rect.topleft = self.rect.x + padding, self.rect.y + padding

    def draw(self, surf: pygame.surface.Surface):
        """Draw the button (or label)

        Args:
            surf (pygame.surface.Surface): Window surface

        Returns:
            bool: Whether this button was clicked
        """

        # Whether button is clicked or not
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        action = self.rect.collidepoint(pos) \
            and pygame.mouse.get_pressed()[0] == 1

        # Draw button
        pygame.draw.rect(surf, self.background_color, self.rect)

        if self.outline:
            pygame.draw.rect(surf, BLACK, self.rect, width=self.outline)

        text_x, text_y = self.rect.x + self.padding, self.rect.y + self.padding
        surf.blit(self.text_surf, (text_x, text_y))

        return action

    def __repr__(self) -> str:
        return f"Button{tuple(vars(self).values())!r}"
