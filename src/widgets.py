import pygame

from .constants import (
    BLACK,
    DARK_BLUE,
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
            font = pygame.font.Font(
                "assets/fonts/Montserrat-Bold.ttf", font_size)
        else:
            font = pygame.font.Font(
                "assets/fonts/Montserrat-Regular.ttf", font_size)

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


class Label(Button):
    def draw(self, surf: pygame.surface.Surface) -> None:
        """Draw label

        Args:
            surf (pygame.surface.Surface): Destination surface
        """
        # Draw label rectangle
        pygame.draw.rect(surf, self.background_color, self.rect)

        # Draw outline
        if self.outline:
            pygame.draw.rect(surf, BLACK, self.rect, width=self.outline)

        # Render text
        text_x, text_y = self.rect.x + self.padding, self.rect.y + self.padding
        surf.blit(self.text_surf, (text_x, text_y))


class Menu:
    def __init__(self, button: Button, children: list[Button | Label]) -> None:
        self.button = button
        self.children = children
        self.clicked = False
        self.selected: Button | Label | None = None

        self.height = sum(child.rect.height for child in children)
        self.width = max(child.rect.width for child in children)

        self.x = self.button.rect.x - 20
        if self.width < self.button.width:
            self.width = self.button.width + 40
            self.x = self.button.rect.x

        children[0].rect.x = self.x
        children[0].rect.y = self.button.rect.bottom

        for i, child in enumerate(children, 1):
            prev = children[i - 1]
            child.rect.x = self.x
            child.rect.y = prev.rect.y

    def draw(self, surf: pygame.surface.Surface) -> bool:
        """Draw the menu

        Args:
            surf (pygame.surface.Surface): Window surface

        Returns:
            bool: Whether any button in this menu is clicked
        """

        clicked = self.button.draw(surf)
        self.selected = None

        if clicked:
            self.clicked = True

        if not self.clicked:
            return False

        # Whether button is clicked or not
        action = False

        pygame.draw.rect(
            surf,
            DARK_BLUE,
            (self.x - 20,
                self.button.rect.y + self.button.height,
                self.width + 40,
                self.height),
            border_radius=10
        )

        # Handle selection
        for child in self.children:
            if child.draw(surf):
                self.selected = child
                self.clicked = False
                action = True

        return action
