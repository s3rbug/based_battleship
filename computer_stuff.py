import pygame
from stuff import size
from AutoShips import AutoShips
import copy

computer = AutoShips(0)
computer_ships_working = copy.deepcopy(computer.ships)
screen = pygame.display.set_mode(size)
