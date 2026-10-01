import random
import pygame
from config import game_config as cfg


class Pipe:
    """1 cặp cột trên/dưới. Ảnh cột dưới dùng pipe.jpg, cột trên dùng chính ảnh đó lật ngược."""

    def __init__(self, x, image=None):
        self.x = x
        self.width = cfg.PIPE_WIDTH
        self.gap_size = cfg.PIPE_GAP
        self.speed = cfg.PIPE_SPEED        # game.py sẽ cập nhật giá trị này mỗi khung hình

        self.min_gap_y = cfg.PIPE_GAP_MARGIN
        self.max_gap_y = cfg.SCREEN_HEIGHT - cfg.GROUND_HEIGHT - cfg.PIPE_GAP_MARGIN

        self.image = image
        self.image_flipped = pygame.transform.flip(image, False, True) if image else None

        self.gap_y = 0
        self.passed = False
        self.randomize_gap()

    def randomize_gap(self):
        self.gap_y = random.randint(self.min_gap_y, self.max_gap_y)
        self.passed = False

    def update(self, dt):
        self.x -= self.speed * dt   # speed tính bằng pixel/GIÂY, dt là số giây trôi qua -> mượt dù FPS dao động

    def reset(self, new_x):
        self.x = new_x
        self.randomize_gap()

    def get_top_rect(self):
        top_height = self.gap_y - self.gap_size // 2
        return pygame.Rect(int(self.x), 0, self.width, top_height)

    def get_bottom_rect(self):
        bottom_y = self.gap_y + self.gap_size // 2
        bottom_height = (cfg.SCREEN_HEIGHT - cfg.GROUND_HEIGHT) - bottom_y
        return pygame.Rect(int(self.x), bottom_y, self.width, bottom_height)

    def is_off_screen(self):
        return self.x + self.width < 0

    def render(self, screen):
        top_rect, bottom_rect = self.get_top_rect(), self.get_bottom_rect()
        if self.image:
            top_img = pygame.transform.scale(self.image_flipped, (self.width, max(top_rect.height, 1)))
            bottom_img = pygame.transform.scale(self.image, (self.width, max(bottom_rect.height, 1)))
            screen.blit(top_img, top_rect)
            screen.blit(bottom_img, bottom_rect)
        else:
            pygame.draw.rect(screen, cfg.COLOR_PIPE, top_rect)
            pygame.draw.rect(screen, cfg.COLOR_PIPE, bottom_rect)