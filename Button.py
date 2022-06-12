import pygame
from stuff import font, block_size, upper_margin
import colors


class Button:
    """
    Creates buttons and prints explanatory message for them
    ----------
    Attributes:
        __title (str): Button's name (title)
        __message (str): explanatory message to print on screen
        __x_start (int): horizontal offset where to start drawing button
        __y_start (int): vertical offset where to start drawing button
        rect_for_draw (tuple of four ints): button's rectangle to be drawn
        rect (pygame Rect): pygame Rect object
        __rect_for_button_title (tuple of two ints): rectangle within button to print text in it
        __color (tuple): color of button (Default is BLACK, hovered is GREEN_BLUE, disabled is LIGHT_GRAY)
    ----------
    Methods:
    draw_button(): Draws button as a rectangle of color (default is BLACK)
    change_color_on_hover(): Draws button as a rectangle of GREEN_BLUE color
    print_message_for_button(): Prints explanatory message next to button
    """

    def __init__(self, x_offset, button_title, message_to_show, screen):
        self.__title = button_title
        self.__title_width, self.__title_height = font.size(self.__title)
        self.__message = message_to_show
        self.__button_width = self.__title_width + block_size
        self.__button_height = self.__title_height + block_size
        self.__x_start = x_offset
        self.__y_start = upper_margin + 10 * block_size + self.__button_height
        self.rect_for_draw = self.__x_start, self.__y_start, self.__button_width, self.__button_height
        self.rect = pygame.Rect(self.rect_for_draw)
        self.__rect_for_button_title = (self.__x_start + self.__button_width / 2 -
                                        self.__title_width / 2, self.__y_start +
                                        self.__button_height / 2 - self.__title_height / 2)
        self.__color = colors.BLACK
        self.__screen = screen

    def draw_button(self, color=None):
        """
        Draws button as a rectangle of color (default is BLACK)
        Args:
            color (tuple, optional): Button's color. Defaults to None (BLACK).
        """
        if not color:
            color = self.__color
        pygame.draw.rect(self.__screen, color, self.rect_for_draw)
        text_to_blit = font.render(self.__title, True, colors.WHITE)
        self.__screen.blit(text_to_blit, self.__rect_for_button_title)

    def change_color_on_hover(self):
        """
        Draws button as a rectangle of GREEN_BLUE color
        """
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.draw_button(colors.GREEN_BLUE)

    def print_message_for_button(self):
        """
        Prints explanatory message next to button
        """
        message_width, message_height = font.size(self.__message)
        x = self.__x_start / 2 - message_width / 2
        y = self.__y_start + self.__button_height / 2 - message_height / 2
        rect_for_message = (x, y)
        text = font.render(self.__message, True, colors.BLACK)
        obj = pygame.Rect((x, y), (message_width, message_height))
        pygame.draw.rect(self.__screen, colors.WHITE, obj)
        self.__screen.blit(text, rect_for_message)
