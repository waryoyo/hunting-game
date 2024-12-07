import pygame
import sys
import random

pygame.init()

# Create a maximized display and keep the close button visible
display = pygame.display.set_mode(
    (pygame.display.Info().current_w, pygame.display.Info().current_h),
    pygame.RESIZABLE  # Allow resizing the window but keep borders for close button
)
pygame.display.set_caption("Maximized Display")

clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = "down"  # Initial direction

    def main(self, display):
        pygame.draw.rect(display, (255, 64, 79), (self.x, self.y, self.width, self.height))
        self.draw_locking_square(display)

    def get_locking_square_position(self):
        """Get the position of the locking square based on the player's direction."""
        offset = 20  # Distance of the locking square from the player
        lock_size = 10  # Size of the locking square

        if self.direction == "up":
            lock_x = self.x + self.width // 2 - lock_size // 2
            lock_y = self.y - offset
        elif self.direction == "down":
            lock_x = self.x + self.width // 2 - lock_size // 2
            lock_y = self.y + self.height + offset
        elif self.direction == "left":
            lock_x = self.x - offset
            lock_y = self.y + self.height // 2 - lock_size // 2
        elif self.direction == "right":
            lock_x = self.x + self.width + offset
            lock_y = self.y + self.height // 2 - lock_size // 2
        else:
            return self.x, self.y  # Default to player's position

        return lock_x, lock_y

    def draw_locking_square(self, display):
        """Draw a small square indicating where the player is locking."""
        lock_x, lock_y = self.get_locking_square_position()
        lock_size = 10  # Size of the locking square
        pygame.draw.rect(display, (0, 0, 255), (lock_x, lock_y, lock_size, lock_size))

def draw_arena():
    """Draw an empty arena with the larger size."""
    display_width, display_height = display.get_size()
    menu_rect = pygame.Rect(
        display_width // 8, display_height // 8, display_width * 3 // 4, display_height * 3 // 4
    )
    pygame.draw.rect(display, (56, 47, 6), menu_rect)  # Gray background
    pygame.draw.rect(display, (173, 167, 137), menu_rect, 5)  # White border
    return menu_rect


class PlayerBullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 15

    def main(self, display):
        # Update bullet position based on its direction
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

        # Draw the bullet
        pygame.draw.circle(display, (0, 0, 0), (int(self.x), int(self.y)), 5)



class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def main(self, display):
        pygame.draw.rect(display, (173, 167, 137), (self.x, self.y, self.width, self.height))


def generate_walls():
    walls = []
    walls.append(Wall(560, 200, 40, 160))  # Example wall
    walls.append(Wall(900, 500, 35, 90))  # Another example wall
    walls.append(Wall(880, 200, 40, 140))  # Add more walls as needed
    return walls


# Generate walls before starting the game loop
walls = generate_walls()


def check_collision_with_arena(player, arena_rect):
    arena_rect.left -= 5
    arena_rect.top -= 5

    """Check if the player is colliding with the arena boundaries."""
    if player.x - 10 < arena_rect.left:
        player.x = arena_rect.left + 10
    elif player.x + player.width > arena_rect.right:
        player.x = arena_rect.right - player.width

    if player.y - 10 < arena_rect.top:
        player.y = arena_rect.top + 10
    elif player.y + player.height > arena_rect.bottom:
        player.y = arena_rect.bottom - player.height

def get_player_speed(keys):
    """Determine the speed based on diagonal movement."""
    if (keys[pygame.K_a] or keys[pygame.K_d]) and (keys[pygame.K_w] or keys[pygame.K_s]):
        # Moving diagonally, reduce speed by half
        return 2.5  # Half of 5 (default speed)
    return 5  # Normal speed when not moving diagonally


player = Player(250, 160, 32, 32)
player_bullets = []
key_stack = []  # Track pressed keys


while True:
    display.fill((0, 82, 33))
    arena_rect = draw_arena()  # Get the arena boundaries(LEFT - UP - RIGHT - DOWN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle direction changes on key press
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):
                key = {pygame.K_a: "left", pygame.K_d: "right", pygame.K_w: "up", pygame.K_s: "down"}[event.key]
                if key not in key_stack:
                    key_stack.append(key)
                player.direction = key
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):
                key = {pygame.K_a: "left", pygame.K_d: "right", pygame.K_w: "up", pygame.K_s: "down"}[event.key]
                if key in key_stack:
                    key_stack.remove(key)
                if key_stack:  # Default to the last pressed key
                    player.direction = key_stack[-1]
        # Shoot bullets on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Get the position of the locking square
                lock_x, lock_y = player.get_locking_square_position()
                # Add a bullet starting from the locking square's position
                player_bullets.append(PlayerBullet(lock_x + 5, lock_y + 5, player.direction))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Get the position of the locking square
                lock_x, lock_y = player.get_locking_square_position()
                # Add a bullet starting from the locking square's position
                player_bullets.append(PlayerBullet(lock_x + 5, lock_y + 5, player.direction))

    keys = pygame.key.get_pressed()

    # Get the adjusted player speed
    player_speed = get_player_speed(keys)

    # Move player based on the currently pressed keys
    if keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_s]:
        player.y += player_speed

    # Check collision with arena border
    check_collision_with_arena(player, arena_rect)

    # Draw player and bullets
    player.main(display)

    # Update bullets and remove those that go off-screen
    for bullet in player_bullets[:]:
        bullet.main(display)
        if bullet.x < arena_rect.left + 22 or bullet.x > arena_rect.right - 12 or bullet.y < arena_rect.top + 22 or bullet.y > arena_rect.bottom - 18:
            player_bullets.remove(bullet)

    for wall in walls:
        wall.main(display)

    clock.tick(60)
    pygame.display.update()
