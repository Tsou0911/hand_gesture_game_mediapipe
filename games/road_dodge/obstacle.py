import random
import pygame
from config import game_config as cfg
from .player import lane_center_x   # dùng chung công thức tính tâm làn với player


class Obstacle:
    """1 xe địch, luôn rơi đúng giữa 1 trong cfg.ROAD_LANE_COUNT làn (random mỗi lần tái sinh)."""

    def __init__(self, y, image=None):
        self.width = cfg.ROAD_OBSTACLE_WIDTH
        self.height = cfg.ROAD_OBSTACLE_HEIGHT
        self.speed = cfg.ROAD_BASE_SPEED
        self.image = pygame.transform.scale(image, (self.width, self.height)) if image else None

        self.x = 0
        self.y = y
        self.passed = False
        self.randomize_lane()

    def randomize_lane(self):
        lane = random.randint(0, cfg.ROAD_LANE_COUNT - 1)
        self.x = lane_center_x(lane)
        self.passed = False

    def update(self, dt):
        self.y += self.speed * dt

    def reset(self, new_y):
        self.y = new_y
        self.randomize_lane()

    def is_off_screen(self):
        return self.y - self.height / 2 > cfg.SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )

    def render(self, screen):
        rect = self.get_rect()
        if self.image:
            screen.blit(self.image, rect)
        else:
            pygame.draw.rect(screen, cfg.COLOR_OBSTACLE, rect)