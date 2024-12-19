import pygame


def check_collision_with_walls(position, size, walls):
    rect = pygame.Rect(position.x, position.y, *size)
    for wall in walls:
        if wall.rect.colliderect(rect):
            return True
    return False
