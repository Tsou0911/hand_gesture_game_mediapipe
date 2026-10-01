import pygame


def shrink_rect(rect, ratio=0.8):
    """Thu nhỏ rect quanh tâm — dùng khi ảnh có nhiều khoảng trong suốt xung quanh,
    để hitbox nhỏ hơn ảnh thật, va chạm cảm giác công bằng hơn (mục 16 trong đặc tả)."""
    new_rect = pygame.Rect(0, 0, int(rect.width * ratio), int(rect.height * ratio))
    new_rect.center = rect.center
    return new_rect


def check_collision(rect_a, rect_b):
    """So va chạm 2 rect. Chỉ bọc quanh colliderect() cho code gọi dễ đọc hơn."""
    return rect_a.colliderect(rect_b)


def check_collision_any(rect, others):
    """Trả về object ĐẦU TIÊN trong `others` (mỗi object phải có get_rect()) va chạm với rect, hoặc None."""
    for obj in others:
        if check_collision(rect, obj.get_rect()):
            return obj
    return None