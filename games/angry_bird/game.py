import pygame
from config import game_config as cfg
from .bird import Bird
from .pipe import Pipe


class AngryBirdGame:
    """GameManager tạo object này 1 lần (truyền screen + assets),
    sau đó mỗi khung hình gọi update(control, dt) rồi render(screen)."""

    def __init__(self, screen, assets, database):
        bird_image = assets.load_image("chim.jpg")
        pipe_image = assets.load_image("pipe.jpg")

        self.bird = Bird(bird_image)
        self.pipes = [Pipe(cfg.SCREEN_WIDTH + i * cfg.PIPE_SPACING, pipe_image)
                      for i in range(cfg.PIPE_COUNT)]

        self.score = 0
        self.database = database
        self.high_score = database.get_high_score("angry_bird")
        self.game_over = False

        self.font = pygame.font.Font(None, 50)
        self.game_over_font = pygame.font.Font(None, 70)
        self.font_small = pygame.font.Font(None, 30)
        self.ground_rect = pygame.Rect(
            0, cfg.SCREEN_HEIGHT - cfg.GROUND_HEIGHT, cfg.SCREEN_WIDTH, cfg.GROUND_HEIGHT
        )

    def reset(self):
        """GameManager.start_phase() gọi khi bắt đầu ván mới."""
        self.score = 0
        self.game_over = False
        self.bird.reset()
        for i, pipe in enumerate(self.pipes):
            pipe.speed = cfg.PIPE_SPEED
            pipe.reset(cfg.SCREEN_WIDTH + i * cfg.PIPE_SPACING)

    def update(self, control, dt):
        if self.game_over:
            return

        self.bird.update(control.index_pos)

        current_speed = cfg.PIPE_SPEED + (self.score // 10) * cfg.PIPE_SPEED_INCREMENT
        for pipe in self.pipes:
            pipe.speed = current_speed
            pipe.update(dt)

        self._recycle_pipes()
        self._check_score()
        self._check_collision()

    def _recycle_pipes(self):
        for pipe in self.pipes:
            if pipe.is_off_screen():
                rightmost_x = max(p.x for p in self.pipes)
                pipe.reset(rightmost_x + cfg.PIPE_SPACING)

    def _check_score(self):
        bird_x = self.bird.get_rect().centerx
        for pipe in self.pipes:
            if not pipe.passed and bird_x > pipe.x + pipe.width:
                self.score += 1
                pipe.passed = True

    def _check_collision(self):
        bird_rect = self.bird.get_rect()
        if bird_rect.top <= 0 or bird_rect.colliderect(self.ground_rect):
            self._end_game()
            return
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.get_top_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):
                self._end_game()
                return

    def _end_game(self):
        self.game_over = True
        self.high_score = max(self.high_score, self.score)
        self.database.save_score("angry_bird", self.score)


    def render(self, screen):
        screen.fill((135, 206, 235))
        for pipe in self.pipes:
            pipe.render(screen)
        pygame.draw.rect(screen, cfg.COLOR_GROUND, self.ground_rect)
        self.bird.render(screen)

        score_surf = self.font.render(str(self.score), True, cfg.COLOR_TEXT)
        screen.blit(score_surf, score_surf.get_rect(center=(cfg.SCREEN_WIDTH // 2, 50)))
        high_surf = self.font_small.render(f"Best: {self.high_score}", True, cfg.COLOR_MUTED)
        screen.blit(high_surf, high_surf.get_rect(center=(cfg.SCREEN_WIDTH // 2, 90)))
        if self.game_over:
            text = self.game_over_font.render("GAME OVER", True, cfg.COLOR_TEXT)
            screen.blit(text, text.get_rect(center=(cfg.SCREEN_WIDTH // 2, cfg.SCREEN_HEIGHT // 2)))