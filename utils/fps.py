import time


class FPSCounter:
    def __init__(self):
        self._last = time.time()
        self.fps = 0.0

    def tick(self):
        now = time.time()
        dt = now - self._last
        self._last = now
        if dt > 0:
            self.fps = 0.9 * self.fps + 0.1 * (1.0 / dt)   # làm mượt
        return self.fps