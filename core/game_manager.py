import pygame                                             # Pygame: vẽ con trỏ

from config import game_config as cfg                     # các thông số cấu hình
from core.data_models import GameState                    # các trạng thái toàn cục
from frontend.menu import Menu                            # Main Menu (duy nhất)
from games.angry_bird.game import AngryBirdGame
from core.asset_manager import AssetManager
from core.database import Database


from games.road_dodge.game import RoadDodgeGame
from games.fruit_catch.game import FruitCatchGame


class GameManager:
    """Quản lý trạng thái toàn cục: đang ở Menu hay đang chơi game nào.
    Game KHÔNG được tự đổi trạng thái, mọi việc chuyển màn hình đều đi qua đây."""

    def __init__(self, screen):
        self.screen = screen                              # cửa sổ Pygame để vẽ lên
        self.state = GameState.MENU                       # bắt đầu ở Main Menu
        self.menu = Menu()

        # Mỗi trạng thái game <-> 1 đối tượng game (tạo 1 lần, dùng lại nhiều lần)
        self.phases = {

        }
        # Menu trả về số ngón (1/2/3) -> đổi thành trạng thái game tương ứng
        self.finger_to_state = {
            1: GameState.ANGRY_BIRD,
            2: GameState.ROAD_DODGE,
            3: GameState.FRUIT_CATCH,
        }
        self._index_pos = None                            # vị trí ngón trỏ, dùng để vẽ con trỏ
        self.assets = AssetManager()
        self.database = Database()
        self.phases = {
            GameState.ANGRY_BIRD: AngryBirdGame(self.screen, self.assets, self.database),
            GameState.ROAD_DODGE: RoadDodgeGame(self.screen, self.assets, self.database),
            GameState.FRUIT_CATCH: FruitCatchGame(self.screen, self.assets, self.database),
        }
    # ---------- Chuyển trạng thái ----------
    def start_phase(self, state):
        self.phases[state].reset()                        # game bắt đầu lại từ đầu
        self.state = state

    def return_to_menu(self):
        self.state = GameState.MENU
        self.menu.on_enter()                              # xoá lựa chọn cũ + bật cooldown

    # ---------- Vòng lặp ----------
    def update(self, gesture, control, dt):
        """Gọi mỗi khung hình. gesture = GestureData, control = ControllerData, dt = giây."""
        self._index_pos = control.index_pos

        if self.state == GameState.MENU:
            chosen = self.menu.update(gesture, dt)        # menu báo người chơi chọn số mấy
            if chosen is not None:
                self.start_phase(self.finger_to_state[chosen])
            return

        # Đang trong game. QUY TẮC: hai tay = huỷ, ưu tiên cao hơn mọi logic của game.
        # Xử lý ở ĐÂY một lần, không lặp lại trong từng game.
        if gesture.two_hands:
            self.return_to_menu()
            return

        self.phases[self.state].update(control, dt)       # để game hiện tại tự cập nhật

    def render(self):
        if self.state == GameState.MENU:
            self.menu.render(self.screen)
        else:
            self.phases[self.state].render(self.screen)

        # Chấm tròn = vị trí ngón trỏ (giúp người chơi thấy mình đang chỉ đâu)
        if self._index_pos is not None:
            pygame.draw.circle(self.screen, cfg.COLOR_CURSOR, self._index_pos, cfg.CURSOR_RADIUS)
            pygame.draw.circle(self.screen, cfg.COLOR_TEXT, self._index_pos, cfg.CURSOR_RADIUS, 2)