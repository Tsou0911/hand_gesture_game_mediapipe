"""Nơi DUY NHẤT chứa các "gói dữ liệu" (dataclass) dùng chung cho cả project.
File nào cần thì import ra dùng: from core.data_models import HandData
"""
from dataclasses import dataclass, field      # dataclass: tạo class chứa dữ liệu ngắn gọn
from enum import Enum, auto                   # Enum: tạo tập các trạng thái có tên
from typing import Optional, Tuple            # kiểu dữ liệu: "có thể là None", "cặp (x, y)"


@dataclass
class HandData:
    """Kết quả nhận diện tay của 1 khung hình (do HandDetector tạo ra)."""
    hand_count: int = 0                                  # số bàn tay đang thấy (0, 1 hoặc 2)
    # Mỗi phần tử là 1 bàn tay = list 21 điểm (x, y), toạ độ chuẩn hoá 0.0 -> 1.0
    # x=0 là mép trái ảnh, x=1 là mép phải; y=0 là mép TRÊN, y=1 là mép DƯỚI
    landmarks: list = field(default_factory=list)        # field(default_factory=list): mỗi gói có list riêng


@dataclass
class GestureData:
    """Kết quả cử chỉ của 1 khung hình (do GestureDetector tạo ra)."""
    hand_count: int = 0        # số bàn tay đang thấy
    finger_count: int = 0      # số ngón duỗi của bàn tay đầu tiên (0 nếu không có tay)
    two_hands: bool = False    # True khi thấy từ 2 tay trở lên (dùng để quay về Menu)


@dataclass
class ControllerData:
    """Dữ liệu điều khiển gửi cho game (do HandController tạo ra)."""
    # (x, y) tính bằng PIXEL trên cửa sổ game. index_pos[0] là X, index_pos[1] là Y.
    # Bằng None khi không thấy tay, nên game PHẢI kiểm tra "if index_pos is not None".
    index_pos: Optional[Tuple[int, int]] = None


class GameState(Enum):
    """Các trạng thái toàn cục của ứng dụng (chỉ GameManager được đổi)."""
    MENU = auto()          # đang ở Main Menu
    ANGRY_BIRD = auto()    # đang chơi Phase 1
    ROAD_DODGE = auto()    # đang chơi Phase 2
    FRUIT_CATCH = auto()   # đang chơi Phase 3