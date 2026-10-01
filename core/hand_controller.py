from config import game_config as cfg
from core.data_models import ControllerData


class HandController:
    """Đổi vị trí ngón trỏ (toạ độ 0..1 của MediaPipe) thành pixel trên màn hình game,
    đồng thời làm mượt (EMA smoothing) để khử rung/giật giữa các khung hình."""

    def __init__(self, screen_width=cfg.SCREEN_WIDTH, screen_height=cfg.SCREEN_HEIGHT):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._smooth_x = None   # vị trí đã làm mượt của khung hình TRƯỚC (None = chưa có khung nào)
        self._smooth_y = None

    def process(self, hand_data):
        """Nhận HandData, trả về ControllerData chứa index_pos (đã mượt)."""
        data = ControllerData()
        if hand_data.hand_count == 0:
            return data

        x, y = hand_data.landmarks[0][cfg.INDEX_TIP]
        x = self._remap(x)
        y = self._remap(y)
        x, y = self._smooth(x, y)

        data.index_pos = (
            int(x * self.screen_width),
            int(y * self.screen_height)
        )
        return data

    def _smooth(self, x, y):
        """Lọc trung bình trượt: vị trí mới = trộn giữa vị trí cũ và vị trí vừa đo."""
        if self._smooth_x is None:              # lần đầu thấy tay -> nhận luôn, không trộn
            self._smooth_x, self._smooth_y = x, y
        else:
            a = cfg.CONTROLLER_SMOOTHING
            self._smooth_x += (x - self._smooth_x) * a
            self._smooth_y += (y - self._smooth_y) * a
        return self._smooth_x, self._smooth_y

    @staticmethod
    def _remap(v):
        m = cfg.CONTROL_MARGIN
        v = (v - m) / (1 - 2 * m)
        return min(max(v, 0.0), 1.0)