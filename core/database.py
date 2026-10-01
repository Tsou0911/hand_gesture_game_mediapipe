import os
import sqlite3


class Database:
    """Lưu & đọc điểm cao nhất của từng game bằng SQLite (database/game.db)."""

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_dir = os.path.join(base_dir, "database")
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, "game.db")

        self._conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._conn.commit()

    def save_score(self, game_name, score):
        """Gọi mỗi khi 1 ván kết thúc (Game Over)."""
        self._conn.execute(
            "INSERT INTO scores (game_name, score) VALUES (?, ?)",
            (game_name, score),
        )
        self._conn.commit()

    def get_high_score(self, game_name):
        """Điểm cao nhất từ trước giờ. Trả về 0 nếu game_name chưa có lượt chơi nào."""
        row = self._conn.execute(
            "SELECT MAX(score) FROM scores WHERE game_name = ?", (game_name,)
        ).fetchone()
        return row[0] if row and row[0] is not None else 0

    def get_recent_scores(self, game_name, limit=5):
        """Vài lượt chơi gần nhất, mới nhất trước."""
        return self._conn.execute(
            "SELECT score, created_at FROM scores WHERE game_name = ? ORDER BY id DESC LIMIT ?",
            (game_name, limit),
        ).fetchall()

    def close(self):
        self._conn.close()