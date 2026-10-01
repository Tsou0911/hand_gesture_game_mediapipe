import random
import pygame
from config import game_config as cfg


class Fruit:
    """1 quả rơi (tốt hoặc xấu). Pool cfg.FRUIT_COUNT quả, tái dùng — giống cột/xe địch."""

    def __init__(self, y):
        self.radius = cfg.FRUIT_RADIUS
        self.speed = cfg.FRUIT_MIN_SPEED
        self.x = 0
        self.y = y
        self.is_good = True
        self.value = cfg.FRUIT_GOOD_SCORE
        self.randomize(0)

    def randomize(self, speed_bonus):
        half = self.radius
        self.x = random.randint(half, cfg.SCREEN_WIDTH - half)

        self.is_good = random.random() > cfg.FRUIT_BAD_CHANCE
        self.value = cfg.FRUIT_GOOD_SCORE if self.is_good else cfg.FRUIT_BAD_SCORE

        self.speed = random.randint(
            cfg.FRUIT_MIN_SPEED + speed_bonus,
            cfg.FRUIT_MAX_SPEED + speed_bonus,
        )

    def update(self, dt):
        self.y += self.speed * dt

    def reset(self, new_y, speed_bonus=0):
        self.y = new_y
        self.randomize(speed_bonus)

    def is_off_screen(self):
        return self.y - self.radius > cfg.SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )

    def render(self, screen):
        color = cfg.COLOR_FRUIT_GOOD if self.is_good else cfg.COLOR_FRUIT_BAD
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)