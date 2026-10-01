import pygame                                 # Pygame: vẽ giao diện

from config import game_config as cfg         # các thông số cấu hình


class Menu:

    def __init__(self):
        # Tạo sẵn các font một lần (tạo font mỗi khung hình sẽ rất chậm)
        self.font_title = pygame.font.SysFont("arial", 52, bold=True)
        self.font_item = pygame.font.SysFont("arial", 30)
        self.font_small = pygame.font.SysFont("arial", 20)
        self.on_enter()                                       # đặt trạng thái ban đầu

    def on_enter(self):
        """Gọi mỗi khi (quay lại) menu: xoá lựa chọn cũ và bật thời gian chờ."""
        self.candidate = None                                 # số ngón đang được b giữ (1/2/3) hoặc None
        self.hold_time = 0.0                                  # đã giữ cử chỉ này bao lâu (giây)
        # Cooldown: sau khi quay về menu người chơi vẫn đang giơ tay,
        # nếu không chờ thì menu chọn game ngay lập tức
        self.cooldown = cfg.MENU_COOLDOWN

    def update(self, gesture, dt):
        """Nhận GestureData và dt (giây trôi qua). Trả về 1/2/3 nếu vừa chọn xong, ngược lại None."""
        if self.cooldown > 0:                                 # đang trong thời gian chờ
            self.cooldown -= dt
            self._clear_hold()
            return None

        # Cử chỉ không hợp lệ: 2 tay, hoặc số ngón không phải 1/2/3 -> huỷ việc đang giữ
        if gesture.two_hands or gesture.finger_count not in cfg.GAME_TITLES:
            self._clear_hold()
            return None

        if gesture.finger_count != self.candidate:            # đổi sang cử chỉ khác -> đếm lại từ 0
            self.candidate = gesture.finger_count
            self.hold_time = 0.0

        self.hold_time += dt                                  # cộng dồn thời gian giữ cử chỉ
        if self.hold_time >= cfg.MENU_HOLD_TIME:              # giữ đủ lâu -> xác nhận chọn
            chosen = self.candidate
            self.on_enter()                                   # reset + bật cooldown: 1 cử chỉ chỉ chọn 1 lần
            return chosen
        return None

    def _clear_hold(self):
        self.candidate = None
        self.hold_time = 0.0

    def render(self, screen):

        screen.fill(cfg.COLOR_BG)                             # nền
        w = cfg.SCREEN_WIDTH

        title = self.font_title.render("HAND GESTURE GAMES", True, cfg.COLOR_ACCENT)
        screen.blit(title, title.get_rect(center=(w // 2, 80)))
        sub = self.font_small.render("Choose a game with your fingers - hold the gesture for 1 second",
                                     True, cfg.COLOR_MUTED)
        screen.blit(sub, sub.get_rect(center=(w // 2, 130)))

        # Vẽ 3 dòng lựa chọn
        for i, (fingers, name) in enumerate(cfg.GAME_TITLES.items()):
            row = pygame.Rect(120, 190 + i * 100, w - 240, 76)          # hình chữ nhật của dòng
            selected = (fingers == self.candidate)                      # dòng đang được giữ?
            pygame.draw.rect(screen, cfg.COLOR_PANEL, row, border_radius=14)
            if selected:
                pygame.draw.rect(screen, cfg.COLOR_ACCENT, row, width=3, border_radius=14)
                # Thanh tiến trình: đầy dần cho tới khi giữ đủ MENU_HOLD_TIME
                ratio = min(self.hold_time / cfg.MENU_HOLD_TIME, 1.0)
                bar = pygame.Rect(row.x + 16, row.bottom - 16, int((row.w - 32) * ratio), 6)
                pygame.draw.rect(screen, cfg.COLOR_ACCENT, bar, border_radius=3)

            unit = "finger" if fingers == 1 else "fingers"
            label = self.font_item.render(f"{fingers} {unit}   ->   {name}", True, cfg.COLOR_TEXT)
            screen.blit(label, label.get_rect(midleft=(row.x + 30, row.centery - 6)))

        footer = self.font_small.render("In a game: show TWO HANDS to return to this menu   |   ESC to quit",
                                        True, cfg.COLOR_MUTED)
        screen.blit(footer, footer.get_rect(center=(w // 2, cfg.SCREEN_HEIGHT - 40)))