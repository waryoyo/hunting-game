import pygame
from constants import COLORS


class Enemy:
    def __init__(self, x, y, width, height, speed=2):
        self.position = pygame.Vector2(x, y)
        self.size = (width, height)
        self.speed = speed

    def follow_player(self, player_position):
        direction = (player_position - self.position).normalize()
        self.position += direction * self.speed

    def draw(self, display):
        pygame.draw.rect(display, COLORS["ENEMY"], (*self.position, *self.size))
