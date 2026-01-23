import pygame

from ui.constants import (
    SQ,
    BOARD_SIZE,
    SPELL_PANEL_WIDTH,
    WIDTH,
    HEIGHT,
    TOP_BAR_HEIGHT
)

from .assets import Assets
from .board import BoardRenderer
from .topbar import TopBar
from .promotion import PromotionUI
from .game_over import GameOverUI
from ui.menu import ask_game_mode, ask_time_screen


class UI:
    def __init__(self):
        self.SQ = SQ
        self.BOARD_SIZE = BOARD_SIZE
        self.WIDTH = WIDTH
        self.TOP_BAR = TOP_BAR_HEIGHT

        self.spell_rects = {}

        self.WIN = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )
        pygame.display.set_caption("Chess")

        # -------- WINDOW --------
        self.WIN = pygame.display.set_mode(
            (self.WIDTH, self.BOARD_SIZE + self.TOP_BAR)
        )
        pygame.display.set_caption("Chess")

        # -------- FONTS --------
        self.FONT = pygame.font.SysFont("arial", 20)
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
            self.BOARD_SIZE + self.TOP_BAR,
            self.FONT,
            self.BIG
        )

    # -------- PUBLIC FACADE --------

    @property
    def resign_rect(self):
        return self.topbar.resign_rect

    def ask_game_mode(self):
        return ask_game_mode(self)

    def ask_time_screen(self):
        return ask_time_screen(self)

    # -------- DRAW --------

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
        promotion_color,
        spells,
        frozen_square,
        spell_3_active
    ):

        self.WIN.fill((15, 15, 15))

        # Board & UI
        self.topbar.draw(clock, turn)
        self.board.draw(board, selected, legal, animation, frozen_square)


        # Spell panel
        self.draw_spells(spells, turn, spell_3_active)


        # Promotion
        if promotion_color:
            self.promotion.draw(promotion_color)

        # Game over
        if game_over:
            self.game_over_ui.draw(text)

        pygame.display.update()

    # -------- SPELL PANEL --------

    def draw_spells(self, spells, turn, spell_3_active):

        self.spell_rects.clear()

        panel_x = self.BOARD_SIZE + 10
        panel_y = self.TOP_BAR + 30

        # Optional panel background (nice visual)
        panel_rect = pygame.Rect(
            self.BOARD_SIZE,
            self.TOP_BAR,
            SPELL_PANEL_WIDTH,
            self.BOARD_SIZE
        )
        pygame.draw.rect(self.WIN, (30, 30, 30), panel_rect)

        data = [
            ("double_move", "Double Move"),
            ("spell_2", "Freeze"),
            ("spell_3", "ChaosMove")
        ]
        

        for i, (key, label) in enumerate(data):
            rect = pygame.Rect(
                panel_x,
                panel_y + i * 70,
                SPELL_PANEL_WIDTH - 20,
                50
            )

            available = spells[turn][key]
            color = (70, 170, 90) if available else (70, 70, 70)

            pygame.draw.rect(self.WIN, color, rect, border_radius=8)

            if not available:
                overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 140))
                self.WIN.blit(overlay, rect.topleft)

            txt = self.FONT.render(label, True, (255, 255, 255))
            self.WIN.blit(txt, txt.get_rect(center=rect.center))

            self.spell_rects[key] = rect
