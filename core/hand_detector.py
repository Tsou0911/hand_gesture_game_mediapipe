#------------- XÁC ĐỊNH TỌA ĐỘ NGÓN TAY


import cv2
import mediapipe as mp

from config import game_config as cfg
from core.data_models import HandData


class HandDetector:
    def __init__(self):
        self._mp_hands = mp.solutions.hands
        self._mp_draw = mp.solutions.drawing_utils
        # Tạo mô hình nhận diện
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,  #tracking theo ngón tay
            max_num_hands=cfg.MAX_HANDS,
            model_complexity=cfg.MODEL_COMPLEXITY,
            min_detection_confidence=cfg.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=cfg.MIN_TRACKING_CONFIDENCE,
        )
        self._last_results = None

    def detect(self, frame_bgr):
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb)
        self._last_results = results

        data = HandData()
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                points = [(lm.x, lm.y) for lm in hand.landmark]
                data.landmarks.append(points)
            data.hand_count = len(data.landmarks)
        return data

    def draw(self, frame_bgr):
        if self._last_results and self._last_results.multi_hand_landmarks:
            for hand in self._last_results.multi_hand_landmarks:
                self._mp_draw.draw_landmarks(
                    frame_bgr, hand, self._mp_hands.HAND_CONNECTIONS)

    def close(self):
        self._hands.close()