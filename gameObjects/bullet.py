import pygame
from constants import COLORS


class Bullet:
    def __init__(self, x, y, direction, speed=10):
        self.position = pygame.Vector2(x, y)
        self.direction = direction.normalize()
        self.speed = speed
        self.radius = 5

    def update(self, walls):
        self.position += self.direction * self.speed
        for wall in walls:
            if wall.rect.collidepoint(self.position):
                return True  # Collision
        return False

    def draw(self, display):
        pygame.draw.circle(
            display,
            COLORS["BULLET"],
            (int(self.position.x), int(self.position.y)),
            self.radius,
        )
