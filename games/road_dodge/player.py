import pygame
from config import game_config as cfg


def lane_center_x(lane_index):
    """Toạ độ X tâm của làn số lane_index (0 = trái cùng, cfg.ROAD_LANE_COUNT-1 = phải cùng)."""
    lane_width = cfg.SCREEN_WIDTH / cfg.ROAD_LANE_COUNT
    return lane_width * (lane_index + 0.5)


class Player:
    """Xe người chơi: Y cố định gần đáy, nhảy giữa cfg.ROAD_LANE_COUNT làn theo vị trí X ngón trỏ."""

    def __init__(self, image):
        self.width = cfg.ROAD_PLAYER_WIDTH
        self.height = cfg.ROAD_PLAYER_HEIGHT
        self.y = cfg.ROAD_PLAYER_Y
        self.lane = cfg.ROAD_LANE_COUNT // 2         # bắt đầu ở làn giữa

        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(int(lane_center_x(self.lane)), int(self.y)))

    def reset(self):
        self.lane = cfg.ROAD_LANE_COUNT // 2
        self.rect.center = (int(lane_center_x(self.lane)), int(self.y))

    def update(self, index_pos):
        """index_pos: (x, y) pixel ngón trỏ. Chia màn hình thành N làn, xem ngón trỏ đang ở làn nào."""
        if index_pos is None:
            return
        lane_width = cfg.SCREEN_WIDTH / cfg.ROAD_LANE_COUNT
        lane = int(index_pos[0] // lane_width)
        lane = min(max(lane, 0), cfg.ROAD_LANE_COUNT - 1)   # kẹp trong khoảng 0..N-1, phòng tay ra sát mép
        self.lane = lane
        self.rect.centerx = int(lane_center_x(lane))

    def get_rect(self):
        return self.rect

    def render(self, screen):
        screen.blit(self.image, self.rect)