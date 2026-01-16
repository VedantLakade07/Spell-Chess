import pygame
from rules import WHITE, BLACK


class ChessClock:
    def __init__(self):
        self.mode = "sudden"   # sudden | increment | none
        self.increment = 0

        self.white_time = 0
        self.black_time = 0

        self.last_tick = pygame.time.get_ticks()

    # ---------------- SETUP ----------------

    def set_mode(self, mode, base_time=0, increment=0):
        self.mode = mode
        self.increment = increment

        if mode == "none":
            self.white_time = None
            self.black_time = None
        else:
            self.white_time = float(base_time)
            self.black_time = float(base_time)

        self.reset_tick()

    def reset_tick(self):
        self.last_tick = pygame.time.get_ticks()

    # ---------------- UPDATE ----------------

    def update(self, turn, game_over):
        if game_over or self.mode == "none":
            self.reset_tick()
            return

        now = pygame.time.get_ticks()
        dt = (now - self.last_tick) / 1000.0
        self.last_tick = now

        if turn == WHITE:
            self.white_time = max(0, self.white_time - dt)
        else:
            self.black_time = max(0, self.black_time - dt)

    # ---------------- MOVE COMPLETE ----------------

    def on_move_complete(self, color):
        if self.mode == "increment":
            if color == WHITE:
                self.white_time += self.increment
            else:
                self.black_time += self.increment

    # ---------------- FLAG FALL ----------------

    def is_flagged(self):
        if self.mode == "none":
            return None

        if self.white_time <= 0:
            return WHITE
        if self.black_time <= 0:
            return BLACK
        return None
