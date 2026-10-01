import os
import pygame


class AssetManager:
    """Quản lý và load các hình ảnh trong project."""

    def __init__(self):
        # Lấy thư mục gốc của project
        self.base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        # Đường dẫn đến assets/images
        self.image_dir = os.path.join(
            self.base_dir,
            "assets",
            "images"
        )

        # Cache các image đã load
        self.images = {}

    def load_image(self, filename):
        """
        Load một hình ảnh từ assets/images.

        Ví dụ:
            bird = assets.load_image("bird.png")
        """

        # Nếu ảnh đã được load trước đó thì dùng lại
        if filename in self.images:
            return self.images[filename]

        # Tạo đường dẫn đầy đủ
        path = os.path.join(self.image_dir, filename)

        # Kiểm tra file có tồn tại không
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Không tìm thấy asset: {path}"
            )

        # Load ảnh
        image = pygame.image.load(path).convert_alpha()

        # Lưu vào cache
        self.images[filename] = image

        return image

    def clear_cache(self):
        """Xóa toàn bộ ảnh đang được cache."""
        self.images.clear()