# player.py
import pygame
from constants import COLORS


class Player:
    def __init__(self, x, y, width, height, speed=5):
        self.position = pygame.Vector2(x, y)
        self.size = (width, height)
        self.speed = speed
        self.direction = "down"  # Default direction for shooting

    def move(self, keys, check_collision):
        """Move the player based on key inputs and check for collisions."""
        move_vector = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            move_vector.y = -1
            self.direction = "up"
        if keys[pygame.K_s]:
            move_vector.y = 1
            self.direction = "down"
        if keys[pygame.K_a]:
            move_vector.x = -1
            self.direction = "left"
        if keys[pygame.K_d]:
            move_vector.x = 1
            self.direction = "right"

        if move_vector.length() > 0:
            move_vector = move_vector.normalize()

        new_position = self.position + move_vector * self.speed
        if not check_collision(new_position):
            self.position = new_position

    def get_locking_square_position(self):
        """Get bullet spawn position based on direction."""
        offset = 20  # Offset distance from the player
        lock_size = 10
        x, y = self.position.x, self.position.y

        if self.direction == "up":
            return x + self.size[0] // 2 - lock_size // 2, y - offset
        elif self.direction == "down":
            return x + self.size[0] // 2 - lock_size // 2, y + self.size[1] + offset
        elif self.direction == "left":
            return x - offset, y + self.size[1] // 2 - lock_size // 2
        elif self.direction == "right":
            return x + self.size[0] + offset, y + self.size[1] // 2 - lock_size // 2

        return x, y

    def draw(self, display):
        """Draw the player and the locking square."""
        pygame.draw.rect(display, COLORS["PLAYER"], (*self.position, *self.size))

        # Draw the locking square where the player is "looking"
        lock_x, lock_y = self.get_locking_square_position()
        pygame.draw.rect(display, COLORS["LOCKING_SQUARE"], (lock_x, lock_y, 10, 10))
