import pygame
from .assets import Assets
from .board import BoardRenderer
from .topbar import TopBar
from .promotion import PromotionUI
from .game_over import GameOverUI
from .menu import ask_time_screen


class UI:
    def __init__(self):
        # -------- DIMENSIONS --------
        self.WIDTH = 640
        self.TOP_BAR = 80
        self.SQ = self.WIDTH // 8

        # -------- WINDOW (MUST BE FIRST) --------
        self.WIN = pygame.display.set_mode(
            (self.WIDTH, self.WIDTH + self.TOP_BAR)
        )
        pygame.display.set_caption("Chess")

        # -------- FONTS --------
        self.FONT = pygame.font.SysFont("arial", 22)
        self.BIG = pygame.font.SysFont("arial", 36)

        # -------- ASSETS --------
        self.assets = Assets(self.SQ)

        # -------- UI COMPONENTS --------
        self.board = BoardRenderer(
            self.WIN,
            self.SQ,
            self.TOP_BAR,
            self.assets
        )

        self.topbar = TopBar(
            self.WIN,
            self.WIDTH,
            self.TOP_BAR,
            self.FONT
        )

        self.promotion = PromotionUI(
            self.WIN,
            self.WIDTH,
            self.SQ,
            self.assets
        )

        self.game_over_ui = GameOverUI(
            self.WIN,
            self.WIDTH,
            self.WIDTH + self.TOP_BAR,
            self.FONT,
            self.BIG
        )

    # -------- PUBLIC FACADE --------

    @property
    def resign_rect(self):
        return self.topbar.resign_rect

    def draw(
        self,
        board,
        selected,
        legal,
        clock,
        turn,
        game_over,
        text,
        animation,
        promotion_color=None
    ):
        self.WIN.fill((0, 0, 0))

        self.topbar.draw(clock, turn)
        self.board.draw(board, selected, legal, animation)

        if promotion_color:
            self.promotion.draw(promotion_color)

        if game_over:
            self.game_over_ui.draw(text)

        pygame.display.update()

    def ask_time_screen(self):
        return ask_time_screen(self)
