import pygame

class MoveAnimation:
    def __init__(self):
        self.active = False
        self.progress = 0.0
        self.duration = 0.25  # seconds
        self.data = None      # (sr, sc, dr, dc, piece)

        self.start_time = 0

    def start(self, sr, sc, dr, dc, piece):
        self.active = True
        self.progress = 0.0
        self.data = (sr, sc, dr, dc, piece)
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if not self.active:
            return False

        now = pygame.time.get_ticks()
        elapsed = (now - self.start_time) / 1000.0
        self.progress = min(1.0, elapsed / self.duration)

        if self.progress >= 1.0:
            self.active = False
            return True   # animation finished

        return False

    def get_position(self, sq, top_bar):
        if not self.data:
            return None

        sr, sc, dr, dc, _ = self.data

        sx = sc * sq
        sy = sr * sq + top_bar
        ex = dc * sq
        ey = dr * sq + top_bar

        x = sx + (ex - sx) * self.progress
        y = sy + (ey - sy) * self.progress

        return x, y
