import cv2                                    # OpenCV: đổi màu, đổi kích thước ảnh
import pygame                                 # Pygame: tạo Surface để vẽ lên cửa sổ game


def frame_to_surface(frame_bgr, size):
    """Đổi ảnh camera của OpenCV (BGR) thành Surface của Pygame để hiển thị."""
    small = cv2.resize(frame_bgr, size)                       # thu nhỏ ảnh về kích thước mong muốn
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)              # Pygame cần RGB, OpenCV đang là BGR
    return pygame.image.frombuffer(rgb.tobytes(), size, "RGB")   # dựng Surface từ dữ liệu điểm ảnh