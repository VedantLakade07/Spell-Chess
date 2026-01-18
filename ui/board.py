# ui/board.py

import pygame
from ui.constants import (
    BOARD_LIGHT,
    BOARD_DARK,
    SELECT_BG,
    SELECT_BORDER,
    MOVE,
    EMPTY
)


class BoardRenderer:
    def __init__(self, win, sq, top_bar, assets):
        self.win = win
        self.sq = sq
        self.top = top_bar
        self.assets = assets

    def draw(self, board, selected, legal, animation, frozen_square):

        moving_square = None
        moving_piece = None

        if animation and animation.active:
            sr, sc, dr, dc, piece = animation.data
            moving_square = (sr, sc)
            moving_piece = piece

        for r in range(8):
            for c in range(8):
                # -------- SQUARE COLOR --------
                color = BOARD_LIGHT if (r + c) % 2 == 0 else BOARD_DARK

                rect = pygame.Rect(
                    c * self.sq,
                    r * self.sq + self.top,
                    self.sq,
                    self.sq
                )
                pygame.draw.rect(self.win, color, rect)
                #
                # ---------- FROZEN GLOW ----------
                if frozen_square == (r, c):
                    glow = pygame.Surface((self.sq, self.sq), pygame.SRCALPHA)
                    glow.fill((80, 160, 255, 120))  # soft blue glow
                    self.win.blit(glow, rect.topleft)
                
                    pygame.draw.rect(
                        self.win,
                        (120, 200, 255),
                        rect,
                        3
                    )
                

                # -------- SELECTED SQUARE --------
                if selected == (r, c):
                    pygame.draw.rect(self.win, SELECT_BG, rect)
                    pygame.draw.rect(self.win, SELECT_BORDER, rect, 4)

                # -------- LEGAL MOVES --------
                if (r, c) in legal:
                    pygame.draw.rect(self.win, MOVE, rect, 4)

                # -------- PIECE --------
                piece = board[r][c]
                if piece != EMPTY and moving_square != (r, c):
                    key = ("w" if piece.isupper() else "b") + piece.lower()
                    self.win.blit(self.assets.images[key], rect)

        # -------- ANIMATED PIECE --------
        if animation and animation.active:
            pos = animation.get_position(self.sq, self.top)
            if pos:
                x, y = pos
                key = ("w" if moving_piece.isupper() else "b") + moving_piece.lower()
                self.win.blit(self.assets.images[key], (x, y))
