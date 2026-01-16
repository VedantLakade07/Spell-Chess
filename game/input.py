import pygame
from rules import Rules, WHITE, BLACK


class InputHandler:
    def __init__(self, state):
        self.state = state

    # ---------------- ENTRY POINT ----------------

    def handle_event(self, event):
        
        if self.state.game_mode == "pvc" and self.state.turn == BLACK:
            return
        

        if event.type == pygame.KEYDOWN:
            self.handle_key(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse(event.pos)

    # ---------------- KEYBOARD ----------------

    def handle_key(self, key):
        # Game-over controls
        if self.state.game_over:
            if key == pygame.K_r:
                self.state.reset()
            elif key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.quit()
                raise SystemExit
            return

        # Undo
        if key == pygame.K_z and self.state.history:
            self.state.redo.append(self.state.snapshot())
            self.state.restore(self.state.history.pop())

        # Redo
        elif key == pygame.K_y and self.state.redo:
            self.state.history.append(self.state.snapshot())
            self.state.restore(self.state.redo.pop())

    # ---------------- MOUSE ----------------

    def handle_mouse(self, pos):
        ui = self.state.ui

        # ----- RESIGN (ALWAYS ACTIVE) -----
        if ui.resign_rect.collidepoint(pos) and not self.state.game_over:
            self.state.game_over = True
            self.state.result_text = (
                f"{Rules.enemy(self.state.turn).capitalize()} wins by resignation"
            )
            return

        # ----- BLOCK INPUT STATES -----
                # ----- BLOCK ONLY BOARD INPUT -----
        if self.state.animation.active:
            return
        
        # Game over: allow only resign / replay / quit
        if self.state.game_over:
            return
        

        # Promotion clicks handled in game.py
        if self.state.promotion_square:
            return

        x, y = pos

        # Ignore clicks on top bar
        if y < ui.TOP_BAR:
            return

        r = (y - ui.TOP_BAR) // ui.SQ
        c = x // ui.SQ

        if not (0 <= r < 8 and 0 <= c < 8):
            return

        board = self.state.board
        clicked = board[r][c]

        # ---------- PIECE SELECTED ----------
        if self.state.selected:
            sr, sc = self.state.selected

            # Switch selection
            if clicked != "." and self.is_own(clicked):
                self.select(r, c)
                return

            # Attempt move
            if Rules.is_move_legal(
                board, sr, sc, r, c,
                self.state.turn,
                self.state.last_move
            ):
                self.make_move(sr, sc, r, c)
                return

            # Invalid click → deselect
            self.state.selected = None
            self.state.legal_moves = []
            return

        # ---------- NO PIECE SELECTED ----------
        if clicked != "." and self.is_own(clicked):
            self.select(r, c)

    # ---------------- HELPERS ----------------

    def is_own(self, piece):
        return (
            (self.state.turn == WHITE and piece.isupper()) or
            (self.state.turn == BLACK and piece.islower())
        )

    def select(self, r, c):
        self.state.selected = (r, c)
        self.state.legal_moves = [
            (rr, cc)
            for rr in range(8)
            for cc in range(8)
            if Rules.is_move_legal(
                self.state.board,
                r, c, rr, cc,
                self.state.turn,
                self.state.last_move
            )
        ]

    def make_move(self, sr, sc, r, c):
        # Save undo snapshot
        self.state.history.append(self.state.snapshot())
        self.state.redo.clear()

        piece = self.state.board[sr][sc]

        # En passant detection
        self.state.en_passant_capture = None
        if piece.lower() == "p" and sc != c and self.state.board[r][c] == ".":
            self.state.en_passant_capture = (sr, c)

        self.state.pending_move = (sr, sc, r, c, piece)
        self.state.selected = None
        self.state.legal_moves = []

        self.state.animation.start(sr, sc, r, c, piece)
