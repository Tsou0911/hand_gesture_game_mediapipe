"""Toàn bộ thông số cấu hình để ở đây, sửa 1 chỗ là đổi cả project."""

# ----- Camera -----
CAMERA_INDEX = 0          # 0 = webcam mặc định. Nếu không mở được, thử 1
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# ----- MediaPipe Hands -----
MAX_HANDS = 2                    # cần 2 để phát hiện "hai tay = quay về menu"
MODEL_COMPLEXITY = 0             # 0 = nhanh/nhẹ, 1 = chính xác hơn
MIN_DETECTION_CONFIDENCE = 0.7   # độ tin cậy tối thiểu để phát hiện bàn tay mới
MIN_TRACKING_CONFIDENCE = 0.6    # độ tin cậy tối thiểu để tiếp tục theo dõi
CONTROLLER_SMOOTHING = 0.35


# ----- Chỉ số điểm mốc (landmark) của MediaPipe Hands -----
FINGER_TIPS = (8, 12, 16, 20)   # đầu ngón: trỏ, giữa, áp út, út
FINGER_PIPS = (6, 10, 14, 18)   # khớp giữa của 4 ngón đó
THUMB_TIP = 4                   # đầu ngón cái
THUMB_IP = 3                    # khớp ngay dưới đầu ngón cái
PINKY_MCP = 17                  # gốc ngón út
INDEX_TIP = 8                   # đầu ngón trỏ (ngón điều khiển game)

# ----- Cửa sổ game (Pygame) -----
WINDOW_TITLE = "Hand Gesture Games"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30                        # số khung hình mỗi giây của vòng lặp chính

# ----- Điều khiển bằng ngón trỏ -----
# Bỏ đi 10% mép camera ở mỗi cạnh: tay không cần với ra sát mép mới chạm được rìa màn hình
CONTROL_MARGIN = 0.10
CURSOR_RADIUS = 12              # bán kính chấm tròn hiển thị vị trí ngón trỏ

# ----- Main Menu -----
GAME_TITLES = {1: "Angry Bird", 2: "Road Dodge", 3: "Fruit Catch"}   # số ngón -> tên game
MENU_HOLD_TIME = 1.0            # giữ nguyên cử chỉ bao nhiêu GIÂY thì mới chọn (chống chọn nhầm)
MENU_COOLDOWN = 1.0             # sau khi chọn/quay về menu, chờ bao nhiêu giây mới cho chọn tiếp

# ----- Xem trước camera (góc trên bên phải màn hình) -----
PREVIEW_SIZE = (200, 150)
PREVIEW_MARGIN = 10

# ----- Màu sắc (R, G, B) -----
COLOR_BG = (20, 24, 40)
COLOR_PANEL = (40, 48, 80)
COLOR_TEXT = (240, 240, 240)
COLOR_MUTED = (150, 155, 175)
COLOR_ACCENT = (255, 200, 60)
COLOR_CURSOR = (0, 200, 255)

# ----- Phase 1: Angry Bird -----
BIRD_X = 150                    # vị trí X cố định của chim (không đổi khi chơi)
BIRD_RADIUS = 18                # bán kính chim (dùng để vẽ + tính va chạm)
BIRD_SMOOTHING = 0.18           # 0..1, càng nhỏ chim di chuyển càng "mượt/trễ", càng lớn càng "nhạy/giật"
GROUND_HEIGHT = 40              # dải đất ở đáy màn hình, chạm vào = thua

PIPE_WIDTH = 70                 # bề ngang mỗi ống
PIPE_GAP = 160                  # khoảng trống (chỗ chim bay lọt qua) giữa ống trên và ống dưới
PIPE_SPEED = 220                # tốc độ ống di chuyển sang trái, đơn vị: pixel/giây
PIPE_SPAWN_INTERVAL = 1.6       # cứ bao nhiêu giây thì sinh ra 1 cặp ống mới
PIPE_GAP_MARGIN = 80            # khoảng cách tối thiểu từ mép trên/dưới màn hình tới tâm khe hở

COLOR_BIRD = (255, 210, 60)
COLOR_PIPE = (60, 180, 90)
COLOR_GROUND = (90, 70, 50)

PIPE_COUNT = 4                  # số cột tái sử dụng (pool), không tạo/xoá object liên tục
PIPE_SPACING = 260              # khoảng cách giữa tâm 2 cột liền kề (pixel)
PIPE_SPEED_INCREMENT = 40       # mỗi 10 điểm, tốc độ cột cộng thêm bấy nhiêu pixel/giây

# ----- Phase 2: Road Dodge -----
ROAD_PLAYER_WIDTH = 60
ROAD_PLAYER_HEIGHT = 100
ROAD_PLAYER_Y = SCREEN_HEIGHT - 120      # Y cố định của xe người chơi, gần đáy màn hình
ROAD_OBSTACLE_WIDTH = 60
ROAD_OBSTACLE_HEIGHT = 100
ROAD_OBSTACLE_COUNT = 4                  # số xe địch tái sử dụng (pool, giống 4 cột Angry Bird)
ROAD_OBSTACLE_SPACING_Y = 220            # khoảng cách dọc giữa các xe địch khi sinh/tái dùng
ROAD_BASE_SPEED = 240                    # pixel/giây
ROAD_SPEED_INCREMENT = 40                # mỗi 10 điểm, tốc độ += bấy nhiêu
ROAD_SCORE_RATE = 10                     # điểm cộng mỗi GIÂY sống sót
COLOR_OBSTACLE = (200, 60, 60)
ROAD_LANE_COUNT = 4


# ----- Phase 3: Fruit Catch -----
FRUIT_BASKET_WIDTH = 90
FRUIT_BASKET_HEIGHT = 70
FRUIT_BASKET_Y = SCREEN_HEIGHT - 80

FRUIT_COUNT = 5                     # số quả rơi tái sử dụng (pool), giống 4 cột/4 xe
FRUIT_RADIUS = 20
FRUIT_MIN_SPEED = 150               # pixel/giây, random mỗi quả trong khoảng min-max
FRUIT_MAX_SPEED = 260
FRUIT_SPEED_INCREMENT = 15          # cứ mỗi 50 điểm, cộng thêm vào khoảng tốc độ
FRUIT_VERTICAL_SPACING = 160        # khoảng cách dọc giữa các quả khi tái sinh

FRUIT_GOOD_SCORE = 10
FRUIT_BAD_SCORE = -15
FRUIT_BAD_CHANCE = 0.3              # 30% là quả xấu

FRUIT_GAME_OVER_SCORE = 0           # điểm xuống DƯỚI mức này -> Game Over

COLOR_FRUIT_GOOD = (220, 60, 60)    # tạm: đỏ. Khi có apple.png/banana.png thì thay bằng ảnh
COLOR_FRUIT_BAD = (120, 60, 160)    # tạm: tím