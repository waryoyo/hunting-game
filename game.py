import math
import pygame
from characters.player import Player
from characters.enemy import Enemy
from gameObjects.wall import Wall
from gameObjects.bullet import Bullet
from gameObjects.arena import draw_arena, generate_arena_walls
from gameObjects.sound_manager import SoundManager
from utils import check_collision_with_walls
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MAP_HEIGHT, MAP_WIDTH


class Game:
    def __init__(self):
        pygame.init()

        # Setup display
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Refactored Game")

        # Clock and sound
        self.clock = pygame.time.Clock()
        self.sound_manager = SoundManager()

        # Game entities
        self.player = Player(250, 160, 32, 32)
        self.enemy = Enemy(400, 300, 32, 32)
        self.bullets = []
        self.arena_walls = generate_arena_walls()
        self.walls = self.arena_walls + [
            Wall(400, 200, 200, 40),
            Wall(600, 400, 40, 200),
        ]

    def draw_cone_of_light(self, surface, player):
        """Create the cone of light effect."""
        darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        darkness.fill((0, 0, 0, 200))

        # Cone calculations
        cone_length = 200  # Length of the cone
        cone_angle = math.radians(60)  # Cone width in degrees
        player_center = self.player.position

        direction_vectors = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        dir_vector = pygame.Vector2(direction_vectors[player.direction])
        left_bound = dir_vector.rotate(-30) * cone_length
        right_bound = dir_vector.rotate(30) * cone_length

        # Define cone points
        cone_points = [
            player_center,
            (player_center[0] + left_bound.x, player_center[1] + left_bound.y),
            (player_center[0] + right_bound.x, player_center[1] + right_bound.y),
        ]

        # Cut out the cone from the darkness layer
        pygame.draw.polygon(darkness, (0, 0, 0, 0), cone_points)

        # Blit the darkness onto the screen
        surface.blit(darkness, (0, 0))

    def clamp_camera(self, player, map_width, map_height):
        """Center the camera on the player, but clamp to the map boundaries."""
        camera_x = max(
            0, min(player.position.x - SCREEN_WIDTH // 2, map_width - SCREEN_WIDTH)
        )
        camera_y = max(
            0, min(player.position.y - SCREEN_HEIGHT // 2, map_height - SCREEN_HEIGHT)
        )
        return camera_x, camera_y

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bullet_x, bullet_y = self.player.get_locking_square_position()
                    direction = {
                        "up": pygame.Vector2(0, -1),
                        "down": pygame.Vector2(0, 1),
                        "left": pygame.Vector2(-1, 0),
                        "right": pygame.Vector2(1, 0),
                    }[self.player.direction]
                    self.bullets.append(Bullet(bullet_x, bullet_y, direction))

            # Update
            self.player.move(
                keys,
                lambda pos: check_collision_with_walls(
                    pos, self.player.size, self.walls
                ),
            )
            self.enemy.follow_player(self.player.position)

            camera_x, camera_y = self.clamp_camera(self.player, MAP_WIDTH, MAP_HEIGHT)

            for bullet in self.bullets[:]:
                if bullet.update(self.walls):
                    self.sound_manager.play_bullet_hit()
                    self.bullets.remove(bullet)

            # Draw
            draw_arena(self.display)
            self.player.draw(self.display)
            self.enemy.draw(self.display)
            for wall in self.walls:
                wall.draw(self.display)
            for bullet in self.bullets:
                bullet.draw(self.display)

            self.draw_cone_of_light(self.display, self.player)

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
