# Hand Gesture Interactive Games

Ứng dụng game tương tác điều khiển hoàn toàn bằng webcam và cử chỉ tay — không cần chuột, bàn phím.

## Công nghệ

- Python 3.10
- OpenCV — đọc webcam
- MediaPipe Hands — nhận diện bàn tay, 21 điểm mốc (landmark)
- Pygame — dựng giao diện, vòng lặp game
- SQLite — lưu điểm cao

## Yêu cầu hệ thống

- Python 3.10 (MediaPipe 0.10.21 chỉ hỗ trợ Python 3.9–3.12)
- Webcam
- Windows (đã test), có thể chạy trên hệ điều hành khác có hỗ trợ OpenCV + MediaPipe

## Cài đặt

```bash
# Tạo virtual environment bằng Python 3.10
python3.10 -m venv venv
venv\Scripts\activate

# Cài thư viện
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
python main.py
```

Một cửa sổ Pygame sẽ mở lên, kèm khung xem trước webcam ở góc trên-phải.

## Cách chơi

### Main Menu

Giơ ngón tay và **giữ yên khoảng 1 giây** để chọn:

| Cử chỉ | Game |
|---|---|
| ☝️ 1 ngón | Angry Bird |
| ✌️ 2 ngón | Road Dodge |
| 🤟 3 ngón | Fruit Catch |

### Trong game

Dùng **ngón trỏ** để điều khiển (vị trí X/Y trên màn hình, tương ứng vị trí tay trước webcam).

Giơ **CẢ HAI TAY** bất kỳ lúc nào để huỷ ván đang chơi và quay về Main Menu.

### Phase 1 — Angry Bird

Di chuyển ngón trỏ lên/xuống để điều khiển chim bay qua các cột. Vượt qua 1 cặp cột được +1 điểm. Tốc độ cột tăng dần sau mỗi 10 điểm. Chạm cột/đất/trần = Game Over.

### Phase 2 — Road Dodge

Di chuyển ngón trỏ trái/phải để xe chuyển làn, né xe địch rơi xuống từ 4 làn đường. Vượt qua 1 xe được +1 điểm. Tốc độ tăng dần sau mỗi 10 điểm. Va chạm = Game Over.

### Phase 3 — Fruit Catch

Di chuyển ngón trỏ trái/phải để giỏ hứng quả rơi. Quả tốt +10 điểm, quả xấu −15 điểm. Điểm xuống dưới 0 = Game Over.

Mọi phase đều hiện điểm số hiện tại và kỷ lục ("Best") ngay trên màn hình, tự động lưu vào `database/game.db` khi kết thúc ván.

## Cấu trúc project