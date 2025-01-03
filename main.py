import pygame
import sys
import random

pygame.init()

# Create a maximized display and keep the close button visible
display = pygame.display.set_mode(
    (pygame.display.Info().current_w, pygame.display.Info().current_h),
    pygame.RESIZABLE,  # Allow resizing the window but keep borders for close button
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
        pygame.draw.rect(
            display, (255, 64, 79), (self.x, self.y, self.width, self.height)
        )
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


class Enemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 2


    #apply ai downthere!!
    def follow_player(self, player):
        if self.x < player.x:
            self.x += self.speed
        elif self.x > player.x:
            self.x -= self.speed
        if self.y < player.y:
            self.y += self.speed
        elif self.y > player.y:
            self.y -= self.speed

    def main(self, display, player):
        self.follow_player(player)
        pygame.draw.rect(display, (200, 0, 0), (self.x, self.y, self.width, self.height))



def draw_arena():
    """Draw an empty arena with the larger size."""
    display_width, display_height = display.get_size()
    menu_rect = pygame.Rect(
        display_width // 8,
        display_height // 8,
        display_width * 3 // 4,
        display_height * 3 // 4,
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
        pygame.draw.rect(
            display, (173, 167, 137), (self.x, self.y, self.width, self.height)
        )


def generate_walls():
    walls = []
    walls.append(Wall(560, 200, 40, 160))  # Example wall
    walls.append(Wall(900, 500, 35, 90))  # Another example wall
    walls.append(Wall(880, 200, 40, 140))  # Add more walls as needed
    return walls


# Generate walls before starting the game loop


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
    if (keys[pygame.K_a] or keys[pygame.K_d]) and (
        keys[pygame.K_w] or keys[pygame.K_s]
    ):
        # Moving diagonally, reduce speed by half
        return 2.5  # Half of 5 (default speed)
    return 5  # Normal speed when not moving diagonally


player = Player(250, 160, 32, 32)
enemy = Enemy(400, 300, 32, 32)
player_bullets = []
key_stack = []  # Track pressed keys


walls = []


def generate_map(display):
    display_width, display_height = display.get_size()
    tile_width = display_width // 60
    tile_height = display_height // 45

    cols = (display_width + tile_width - 1) // tile_width
    rows = (display_height + tile_height - 1) // tile_height

    tiles = [[0 for _ in range(cols)] for _ in range(rows)]

    # Add walls around the edges
    for row in range(rows):
        for col in range(cols):

            if row == 5 and col >= 5 and col <= cols - 5:
                tiles[row][col] = 1

            if row == rows - 5 and col >= 5 and col <= cols - 5:
                tiles[row][col] = 1

            if col == 5 and row >= 5 and row <= rows - 5:
                tiles[row][col] = 1

            if col == cols - 5 and row >= 5 and row <= rows - 5:
                tiles[row][col] = 1
            # if row == 5 or row == rows - 5 or col == 5 or col == cols - 5:
            #     # if row > rows - 3 or col > cols - 3:
            #     tiles[row][col] = 1

    for row in range(rows):
        for col in range(cols):
            tile_value = tiles[row][col]
            xPos = col * tile_width
            yPos = row * tile_height

            if tile_value == 1:  # Wall
                walls.append(Wall(xPos, yPos, tile_width, tile_height))

    return tiles


# def draw_map(display, tiles):
#     display_width, display_height = display.get_size()
#     tile_width = display_width // 60
#     tile_height = display_height // 45

#     cols = (display_width + tile_width - 1) // tile_width
#     rows = (display_height + tile_height - 1) // tile_height


# (0, 82, 33)


tiles = generate_map(display)


def check_collision(player, speed):
    """Check if the player is about to collide with a wall based on their direction."""
    display_width = pygame.display.Info().current_w
    display_height = pygame.display.Info().current_h
    tile_width = display_width // 60
    tile_height = display_height // 45

    # Calculate the player's next position based on their direction
    next_x, next_y = player.x, player.y
    if player.direction == "left":
        next_x -= speed
    elif player.direction == "right":
        next_x += speed
    elif player.direction == "up":
        next_y -= speed
    elif player.direction == "down":
        next_y += speed

    # Get the tile indices for the next position's corners
    corners = [
        (next_x, next_y),  # Top-left
        (next_x + player.width, next_y),  # Top-right
        (next_x, next_y + player.height),  # Bottom-left
        (next_x + player.width, next_y + player.height),  # Bottom-right
    ]

    for corner_x, corner_y in corners:
        col = max(0, min(len(tiles[0]) - 1, int(corner_x // tile_width)))
        row = max(0, min(len(tiles) - 1, int(corner_y // tile_height)))

        # Check if the tile is a wall
        if tiles[row][col] == 1:
            return True  # Collision detected
    return False

            # if player.direction == "up" and player.y < display_height/2:
            #     player.y = (row + 1) * tile_height
            # elif player.direction == "down" and player.y > display_height/2:
            #     player.y = ((row - 1) * tile_height)-(player.height/2)
            # elif player.direction == "left" and player.x < display_width/2:
            #     player.x = (col + 1) * tile_width
            # elif player.direction == "right" and player.x < display_width / 2:
            #     player.x = ((col - 1) * tile_width)-(player.width/2)


bullet_hit_sound = pygame.mixer.Sound('./soundFX/080998_bullet-hit-39870.mp3')  # Load sound

def check_bullet_collision(bullet, walls):
    """Check if a bullet collides with any wall."""
    bullet_rect = pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)  # Bullet hitbox

    for wall in walls:
        wall_rect = pygame.Rect(wall.x, wall.y, wall.width, wall.height)
        if bullet_rect.colliderect(wall_rect):
            bullet_hit_sound.play()  # Play sound on collision
            return True  # Bullet collides with a wall
    return False



while True:
    display.fill((0, 82, 33))
    # draw_map(display, tiles)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle direction changes on key press
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):
                key = {
                    pygame.K_a: "left",
                    pygame.K_d: "right",
                    pygame.K_w: "up",
                    pygame.K_s: "down",
                }[event.key]
                if key not in key_stack:
                    key_stack.append(key)
                player.direction = key
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):
                key = {
                    pygame.K_a: "left",
                    pygame.K_d: "right",
                    pygame.K_w: "up",
                    pygame.K_s: "down",
                }[event.key]
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
                player_bullets.append(
                    PlayerBullet(lock_x + 5, lock_y + 5, player.direction)
                )
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Get the position of the locking square
                lock_x, lock_y = player.get_locking_square_position()
                # Add a bullet starting from the locking square's position
                player_bullets.append(
                    PlayerBullet(lock_x + 5, lock_y + 5, player.direction)
                )


    keys = pygame.key.get_pressed()

    # Get the adjusted player speed
    player_speed = get_player_speed(keys)

    # Move player based on the currently pressed keys
    if keys[pygame.K_a]:
        player.direction = "left"
        if not check_collision(player, player_speed):
            player.x -= player_speed
    if keys[pygame.K_d]:
        player.direction = "right"
        if not check_collision(player, player_speed):
            player.x += player_speed
    if keys[pygame.K_w]:
        player.direction = "up"
        if not check_collision(player, player_speed):
            player.y -= player_speed
    if keys[pygame.K_s]:
        player.direction = "down"
        if not check_collision(player, player_speed):
            player.y += player_speed

    # Draw player and bullets
    player.main(display)

    enemy.main(display, player)

    for wall in walls:
        wall.main(display)

    for bullet in player_bullets[:]:
        bullet.main(display)
        if check_bullet_collision(bullet, walls):
            player_bullets.remove(bullet)  # Remove bullet on collision

    clock.tick(60)
    pygame.display.update()
