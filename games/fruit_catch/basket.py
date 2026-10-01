import pygame
from config import game_config as cfg


class Basket:
    """Giỏ hứng quả: Y cố định gần đáy, X bám theo ngón trỏ."""

    def __init__(self, image):
        self.width = cfg.FRUIT_BASKET_WIDTH
        self.height = cfg.FRUIT_BASKET_HEIGHT
        self.y = cfg.FRUIT_BASKET_Y

        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(cfg.SCREEN_WIDTH // 2, int(self.y)))

    def reset(self):
        self.rect.center = (cfg.SCREEN_WIDTH // 2, int(self.y))

    def update(self, index_pos):
        """index_pos: (x, y) ngón trỏ. Chỉ dùng X: basket_x = index_pos[0]."""
        if index_pos is None:
            return
        half = self.width // 2
        x = min(max(index_pos[0], half), cfg.SCREEN_WIDTH - half)
        self.rect.centerx = int(x)

    def get_rect(self):
        return self.rect

    def render(self, screen):
        screen.blit(self.image, self.rect)