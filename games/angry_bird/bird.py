import pygame
from config import game_config as cfg


class Bird:
    """Con chim: X cố định (cfg.BIRD_X), Y bám theo ngón trỏ. Có ảnh asset."""

    def __init__(self, image):
        self.x = cfg.BIRD_X
        self.y = cfg.SCREEN_HEIGHT / 2
        self.radius = cfg.BIRD_RADIUS

        size = self.radius * 2
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def reset(self):
        self.y = cfg.SCREEN_HEIGHT / 2
        self.rect.center = (int(self.x), int(self.y))

    def update(self, index_pos):
        if index_pos is None:
            return
        target_y = index_pos[1]
        self.y += (target_y - self.y) * cfg.BIRD_SMOOTHING
        self.rect.center = (int(self.x), int(self.y))

    def get_rect(self):
        return self.rect

    def render(self, screen):
        screen.blit(self.image, self.rect)