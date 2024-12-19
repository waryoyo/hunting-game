import pygame


class SoundManager:
    def __init__(self):
        self.bullet_hit = pygame.mixer.Sound("soundFX/080998_bullet-hit-39870.mp3")

    def play_bullet_hit(self):
        self.bullet_hit.play()
