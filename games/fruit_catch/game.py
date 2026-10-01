import pygame
from config import game_config as cfg
from core.collision import check_collision_any
from .basket import Basket
from .fruit import Fruit


class FruitCatchGame:
    def __init__(self, screen, assets, database):
        basket_image = assets.load_image("basket.jpg")
        self.basket = Basket(basket_image)

        self.fruits = [Fruit(-i * cfg.FRUIT_VERTICAL_SPACING) for i in range(cfg.FRUIT_COUNT)]

        self.database = database
        self.score = 0
        self.high_score = database.get_high_score("fruit_catch")
        self.game_over = False

        self.font = pygame.font.Font(None, 50)
        self.game_over_font = pygame.font.Font(None, 70)
        self.font_small = pygame.font.Font(None, 30)
    def reset(self):
        self.score = 0
        self.game_over = False
        self.basket.reset()
        for i, fruit in enumerate(self.fruits):
            fruit.reset(-i * cfg.FRUIT_VERTICAL_SPACING)

    def update(self, control, dt):
        if self.game_over:
            return

        self.basket.update(control.index_pos)

        speed_bonus = (self.score // 50) * cfg.FRUIT_SPEED_INCREMENT
        for fruit in self.fruits:
            fruit.update(dt)

        self._check_catch(speed_bonus)
        self._recycle_fruits(speed_bonus)
        self._check_game_over()

    def _check_catch(self, speed_bonus):
        caught = check_collision_any(self.basket.get_rect(), self.fruits)
        if caught is not None:
            self.score += caught.value
            topmost_y = min(f.y for f in self.fruits)
            caught.reset(topmost_y - cfg.FRUIT_VERTICAL_SPACING, speed_bonus)

    def _recycle_fruits(self, speed_bonus):
        for fruit in self.fruits:
            if fruit.is_off_screen():
                topmost_y = min(f.y for f in self.fruits)
                fruit.reset(topmost_y - cfg.FRUIT_VERTICAL_SPACING, speed_bonus)

    def _check_game_over(self):
        if self.score < cfg.FRUIT_GAME_OVER_SCORE:
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
            self.database.save_score("fruit_catch", self.score)

    def render(self, screen):
        screen.fill((40, 20, 60))

        for fruit in self.fruits:
            fruit.render(screen)
        self.basket.render(screen)

        score_surf = self.font.render(str(self.score), True, cfg.COLOR_TEXT)
        screen.blit(score_surf, score_surf.get_rect(center=(cfg.SCREEN_WIDTH // 2, 50)))
        high_surf = self.font_small.render(f"Best: {self.high_score}", True, cfg.COLOR_MUTED)
        screen.blit(high_surf, high_surf.get_rect(center=(cfg.SCREEN_WIDTH // 2, 90)))
        if self.game_over:
            text = self.game_over_font.render("GAME OVER", True, cfg.COLOR_TEXT)
            screen.blit(text, text.get_rect(center=(cfg.SCREEN_WIDTH // 2, cfg.SCREEN_HEIGHT // 2)))