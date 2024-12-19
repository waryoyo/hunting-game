import pygame
from constants import COLORS


class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, display):
        pygame.draw.rect(display, COLORS["WALL"], self.rect)
