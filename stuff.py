import pygame
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

pygame.font.init()
if screensize[0] / screensize[1] == 16 / 9 or screensize[0] / screensize[1] == 16 / 10:
    block_size = round(screensize[0] / 34)
else:
    block_size = 35
left_margin = 5 * block_size
upper_margin = round(3.5 * block_size)
# 30 = 2x10 blocks width in two grids + hard-coded 5*blocks gap after each grid!
size = (left_margin + 30 * block_size, upper_margin + 15 * block_size)
LETTERS = "ABCDEFGHIJ"
font_size = int(block_size / 1.5)
font = pygame.font.SysFont('notosans', font_size)
