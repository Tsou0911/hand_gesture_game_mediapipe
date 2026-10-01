#------------- ĐẾM SỐ NGÓN TAY


import math
from core.data_models import GestureData
from config import game_config as cfg         # lấy các chỉ số điểm mốc từ file cấu hình

def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


class GestureDetector:
    """Đọc 21 điểm của bàn tay rồi cho biết: bao nhiêu tay, bao nhiêu ngón."""

    def detect(self, hand_data):
        """Nhận HandData từ HandDetector, trả về GestureData."""
        gesture = GestureData(
            hand_count=hand_data.hand_count,             # chép số tay từ hand_data sang
            two_hands=hand_data.hand_count >= 2,         # từ 2 tay trở lên thì bật cờ two_hands
        )
        if hand_data.hand_count >= 1:                    # chỉ đếm ngón khi thật sự có tay
            # landmarks[0] = bàn tay đầu tiên (list 21 điểm)
            gesture.finger_count = self._count_fingers(hand_data.landmarks[0])
        return gesture

    def _count_fingers(self, pts):
        """Đếm số ngón đang duỗi. pts là list 21 điểm (x, y) của 1 bàn tay."""
        count = 0                                        # biến đếm, bắt đầu từ 0

        # --- 4 ngón dài: trỏ, giữa, áp út, út ---
        # zip ghép từng cặp (đầu ngón, khớp giữa): (8,6), (12,10), (16,14), (20,18)
        for tip, pip in zip(cfg.FINGER_TIPS, cfg.FINGER_PIPS):
            # pts[i][1] là toạ độ y của điểm i. Trục y hướng XUỐNG,
            # nên y nhỏ hơn = nằm CAO hơn. Đầu ngón cao hơn khớp giữa = ngón đang duỗi.
            if pts[tip][1] < pts[pip][1]:
                count += 1                               # ngón duỗi -> cộng 1

        # --- Ngón cái: xử lý riêng ---
        if self._thumb_is_open(pts):
            count += 1
        return count                                     # tổng số ngón duỗi (0 đến 5)

    def _thumb_is_open(self, pts):
        """Ngón cái duỗi sang ngang nên không so độ cao (y) được, phải dùng khoảng cách."""
        # Ngón cái MỞ khi đầu ngón cái ở XA gốc ngón út hơn khớp ngay dưới nó.
        # Ngón cái gập thì đầu ngón cái chui vào lòng bàn tay, tức là GẦN gốc ngón út.
        # Cách này đúng cho cả tay trái lẫn tay phải, không cần biết là tay nào.
        tip_to_pinky = _dist(pts[cfg.THUMB_TIP], pts[cfg.PINKY_MCP])   # đầu ngón cái -> gốc ngón út
        ip_to_pinky = _dist(pts[cfg.THUMB_IP], pts[cfg.PINKY_MCP])     # khớp ngón cái -> gốc ngón út
        return tip_to_pinky > ip_to_pinky