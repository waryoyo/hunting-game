import pygame
from constants import COLORS, SCREEN_HEIGHT, SCREEN_WIDTH
from gameObjects.wall import Wall


def draw_arena(display):
    """Draw the background."""
    display.fill(COLORS["ARENA_BG"])


def generate_arena_walls():
    """Create walls for the arena border."""
    walls = []
    border_thickness = 10

    # Top wall
    walls.append(Wall(0, 0, SCREEN_WIDTH, border_thickness))
    # Bottom wall
    walls.append(
        Wall(0, SCREEN_HEIGHT - border_thickness, SCREEN_WIDTH, border_thickness)
    )
    # Left wall
    walls.append(Wall(0, 0, border_thickness, SCREEN_HEIGHT))
    # Right wall
    walls.append(
        Wall(SCREEN_WIDTH - border_thickness, 0, border_thickness, SCREEN_HEIGHT)
    )

    return walls
