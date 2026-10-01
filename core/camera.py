import cv2
from config import game_config as cfg


class Camera:
    def __init__(self):
        self._cap = cv2.VideoCapture(cfg.CAMERA_INDEX)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.CAMERA_WIDTH)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.CAMERA_HEIGHT)
        if not self._cap.isOpened():
            raise RuntimeError("Không mở được webcam. Thử đổi CAMERA_INDEX")

    def read(self):
        ok, frame = self._cap.read()
        if not ok:
            return None
        return cv2.flip(frame, 1)   # lật gương

    def release(self):
        self._cap.release()