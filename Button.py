import pygame
from stuff import font, block_size, upper_margin
from computer_stuff import screen
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

    def __init__(self, x_offset, button_title, message_to_show):
        self.__title = button_title
        self.__title_width, self.__title_height = font.size(self.__title)
        self.__message = message_to_show
        self.__button_width = self.__title_width + block_size
        self.__button_height = self.__title_height + block_size
        self.__x_start = x_offset
        self.__y_start = upper_margin + 10 * block_size + self.__button_height
        self.rect_for_draw = self.__x_start, self.__y_start, self.__button_width, self.__button_height
        self.rect = pygame.Rect(self.rect_for_draw)
        self.__rect_for_button_title = self.__x_start + self.__button_width / 2 - \
            self.__title_width / 2, self.__y_start + \
            self.__button_height / 2 - self.__title_height / 2
        self.__color = colors.BLACK

    def draw_button(self, color=None):
        """
        Draws button as a rectangle of color (default is BLACK)
        Args:
            color (tuple, optional): Button's color. Defaults to None (BLACK).
        """
        if not color:
            color = self.__color
        pygame.draw.rect(screen, color, self.rect_for_draw)
        text_to_blit = font.render(self.__title, True, colors.WHITE)
        screen.blit(text_to_blit, self.__rect_for_button_title)

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
        rect_for_message = self.__x_start / 2 - message_width / \
            2, self.__y_start + self.__button_height / 2 - message_height / 2
        text = font.render(self.__message, True, colors.BLACK)
        screen.blit(text, rect_for_message)
