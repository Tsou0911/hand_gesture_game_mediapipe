import cv2
import pygame

from config import game_config as cfg
from core.camera import Camera
from core.hand_detector import HandDetector
from core.gesture_detector import GestureDetector
from core.hand_controller import HandController
from core.game_manager import GameManager


def frame_to_surface(frame_bgr):
    """Đổi 1 khung hình OpenCV (BGR, numpy array) thành Surface để Pygame vẽ được."""
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    height, width = frame_rgb.shape[:2]
    return pygame.image.frombuffer(frame_rgb.tobytes(), (width, height), "RGB")


def main():
    pygame.init()
    screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    pygame.display.set_caption(cfg.WINDOW_TITLE)
    clock = pygame.time.Clock()

    camera = Camera()
    hand_detector = HandDetector()
    gesture_detector = GestureDetector()
    hand_controller = HandController()
    game_manager = GameManager(screen)

    running = True
    try:
        while running:
            dt = clock.tick(cfg.FPS) / 1000.0   # giây trôi qua từ khung hình trước

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            frame = camera.read()
            if frame is None:
                continue   # webcam chưa kịp trả khung hình, bỏ qua, thử lại khung sau

            hand_data = hand_detector.detect(frame)
            gesture_data = gesture_detector.detect(hand_data)
            control_data = hand_controller.process(hand_data)

            game_manager.update(gesture_data, control_data, dt)
            game_manager.render()

            # Vẽ khung xương bàn tay lên frame rồi dán preview camera ở góc trên-phải
            hand_detector.draw(frame)
            preview = pygame.transform.scale(frame_to_surface(frame), cfg.PREVIEW_SIZE)
            px = cfg.SCREEN_WIDTH - cfg.PREVIEW_SIZE[0] - cfg.PREVIEW_MARGIN
            py = cfg.PREVIEW_MARGIN
            screen.blit(preview, (px, py))
            pygame.draw.rect(screen, cfg.COLOR_ACCENT, (px, py, *cfg.PREVIEW_SIZE), 2)

            pygame.display.flip()
    finally:
        hand_detector.close()
        camera.release()
        pygame.quit()


if __name__ == "__main__":
    main()