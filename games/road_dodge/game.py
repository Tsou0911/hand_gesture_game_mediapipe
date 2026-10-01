import pygame
from config import game_config as cfg
from .player import Player
from .obstacle import Obstacle


class RoadDodgeGame:
    def __init__(self, screen, assets, database):
        player_image = assets.load_image("player.jpg")
        self.player = Player(player_image)

        self.obstacles = [Obstacle(-i * cfg.ROAD_OBSTACLE_SPACING_Y) for i in range(cfg.ROAD_OBSTACLE_COUNT)]

        self.database = database
        self.score = 0
        self.high_score = database.get_high_score("road_dodge")
        self.game_over = False

        self.font = pygame.font.Font(None, 50)
        self.game_over_font = pygame.font.Font(None, 70)
        self.font_small = pygame.font.Font(None, 30)
    def reset(self):
        self.score = 0
        self.game_over = False
        self.player.reset()
        for i, obstacle in enumerate(self.obstacles):
            obstacle.speed = cfg.ROAD_BASE_SPEED
            obstacle.reset(-i * cfg.ROAD_OBSTACLE_SPACING_Y)

    def update(self, control, dt):
        if self.game_over:
            return

        self.player.update(control.index_pos)

        current_speed = cfg.ROAD_BASE_SPEED + (self.score // 10) * cfg.ROAD_SPEED_INCREMENT
        for obstacle in self.obstacles:
            obstacle.speed = current_speed
            obstacle.update(dt)

        self._recycle_obstacles()
        self._check_score()
        self._check_collision()

    def _recycle_obstacles(self):
        for obstacle in self.obstacles:
            if obstacle.is_off_screen():
                topmost_y = min(o.y for o in self.obstacles)
                obstacle.reset(topmost_y - cfg.ROAD_OBSTACLE_SPACING_Y)

    def _check_score(self):
        player_bottom = self.player.get_rect().bottom
        for obstacle in self.obstacles:
            if not obstacle.passed and obstacle.get_rect().top > player_bottom:
                self.score += 1
                obstacle.passed = True

    def _check_collision(self):
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                self.game_over = True
                self.high_score = max(self.high_score, self.score)
                self.database.save_score("road_dodge", self.score)
                return

    def render(self, screen):
        screen.fill((60, 60, 70))
        lane_width = cfg.SCREEN_WIDTH / cfg.ROAD_LANE_COUNT
        for i in range(1, cfg.ROAD_LANE_COUNT):
            x = int(i * lane_width)
            pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, cfg.SCREEN_HEIGHT), 2)

        for obstacle in self.obstacles:
            obstacle.render(screen)
        self.player.render(screen)

        score_surf = self.font.render(str(self.score), True, cfg.COLOR_TEXT)
        screen.blit(score_surf, score_surf.get_rect(center=(cfg.SCREEN_WIDTH // 2, 50)))
        high_surf = self.font_small.render(f"Best: {self.high_score}", True, cfg.COLOR_MUTED)
        screen.blit(high_surf, high_surf.get_rect(center=(cfg.SCREEN_WIDTH // 2, 90)))
        if self.game_over:
            text = self.game_over_font.render("GAME OVER", True, cfg.COLOR_TEXT)
            screen.blit(text, text.get_rect(center=(cfg.SCREEN_WIDTH // 2, cfg.SCREEN_HEIGHT // 2)))