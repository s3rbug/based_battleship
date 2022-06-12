import colors
import pygame
from stuff import left_margin, upper_margin, block_size, font, font_size, LETTERS


class Grid:
    """
    Class to draw the grids and add title, numbers and letters to them
    ----------
    Attributes:
        title (str): Players' name to be displayed on the top of his grid
        offset (int): Where the grid starts (in number of blocks)
                (typically 0 for computer and 15 for human)
        screen: Screen
    ----------
    Methods:
    __draw_grid(): Draws two grids for both players
    __add_nums_letters_to_grid(): Draws numbers 1-10 along vertical and adds letters below horizontal
        lines for both grids
    __sign_grid(): Puts players' names (titles) in the center above the grids
    """

    def __init__(self, title, offset, screen):
        """
        title(str): Players' name to be displayed on the top of his grid
        offset (int): Where the grid starts (in number of blocks)
        (typically 0 for computer and 15 for human)
        screen: Screen
        """
        self.title = title
        self.offset = offset
        self.__screen = screen
        self.__draw_grid()
        self.__add_nums_letters_to_grid()
        self.__sign_grid()

    def __draw_grid(self):
        """
        Draws two grids for both players
        """
        for i in range(11):
            # Horizontal lines
            pygame.draw.line(self.__screen, colors.BLACK,
                             (left_margin + self.offset * block_size, upper_margin + i * block_size),
                             (left_margin + (10 + self.offset) * block_size, upper_margin + i * block_size), 1)
            # Vertical lines
            pygame.draw.line(self.__screen, colors.BLACK,
                             (left_margin + (i + self.offset) * block_size, upper_margin),
                             (left_margin + (i + self.offset) * block_size, upper_margin + 10 * block_size), 1)

    def __add_nums_letters_to_grid(self):
        """
        Draws numbers 1-10 along vertical and adds letters below horizontal
        lines for both grids
        """
        for i in range(10):
            num_ver = font.render(str(i + 1), True, colors.BLACK)
            letters_hor = font.render(LETTERS[i], True, colors.BLACK)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            # Numbers (vertical)
            self.__screen.blit(num_ver,
                               (left_margin - (block_size // 2 + num_ver_width // 2) + self.offset * block_size,
                                upper_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
            # Letters (horizontal)
            self.__screen.blit(letters_hor, (left_margin + i * block_size +
                                             (block_size // 2 - letters_hor_width // 2) + self.offset * block_size,
                                             10 + upper_margin + 10 * block_size))

    def __sign_grid(self):
        """
        Puts players' names (titles) in the center above the grids
        """
        player = font.render(self.title, True, colors.BLACK)
        sign_width = player.get_width()
        self.__screen.blit(player, (left_margin + 5 * block_size - sign_width // 2 +
                                    self.offset * block_size, upper_margin - block_size // 2 - font_size))
