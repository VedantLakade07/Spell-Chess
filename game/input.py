import pygame
from rules import Rules, WHITE, BLACK
from game.spells import SpellSystem


class InputHandler:
    def __init__(self, state):
        self.state = state
        self.pending_spell = None   # "freeze" when targeting


    # ---------------- ENTRY POINT ----------------

    def handle_event(self, event):

        # Block player input during AI turn
        if self.state.game_mode == "pvc" and self.state.turn == BLACK:
            return

        if event.type == pygame.KEYDOWN:
            self.handle_key(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse(event.pos)


    # ---------------- KEYBOARD ----------------

    def handle_key(self, key):
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
    #

    def handle_mouse(self, pos):
        ui = self.state.ui
        x, y = pos

        # ----- RESIGN -----
        if ui.resign_rect.collidepoint(pos) and not self.state.game_over:
            self.state.game_over = True
            self.state.result_text = (
                f"{Rules.enemy(self.state.turn).capitalize()} wins by resignation"
            )
            return

        # ----- SPELL BUTTON CLICK -----
        for spell, rect in ui.spell_rects.items():
            if rect.collidepoint(pos):
            
                if spell == "double_move":
                    SpellSystem.use_double_move(self.state)
                    return

                if spell == "spell_2" and self.state.spells[self.state.turn]["spell_2"]:
                    self.pending_spell = "freeze"
                    return

                if spell == "spell_3" and self.state.spells[self.state.turn]["spell_3"]:
                    self.pending_spell = "swap"
                    return


        # ----- BLOCK STATES -----
        if self.state.animation.active or self.state.game_over or self.state.promotion_square:
            return

        if y < ui.TOP_BAR:
            return

        r = (y - ui.TOP_BAR) // ui.SQ
        c = x // ui.SQ

        if not (0 <= r < 8 and 0 <= c < 8):
            return

        board = self.state.board
        clicked = board[r][c]

        # ----- SPELL TARGETING -----
        if self.pending_spell == "freeze":
            if clicked != "." and not self.is_own(clicked):
                SpellSystem.use_freeze(self.state, (r, c))
                self.pending_spell = None
            return



        if self.pending_spell == "swap":
            if clicked.lower() == "b" and self.is_own(clicked):
                self.state.swap_bishop_square = (r, c)
                self.state.spells[self.state.turn]["spell_3"] = False
                self.pending_spell = None
            return

        # ---------- PIECE SELECTED ----------
        if self.state.selected:
            sr, sc = self.state.selected

            # Switch selection
            if clicked != "." and self.is_own(clicked):
                self.select(r, c)
                return

            # Attempt move
            if Rules.is_move_legal(
                    board,
                    sr, sc,
                    r, c,
                    self.state.turn,
                    self.state.last_move,
                    self.state.castling_rights,
                    self.state.frozen_square,
                    self.state.freeze_timer,
                    self.state.swap_bishop_square
                ):
                self.make_move(sr, sc, r, c)
                return

            # Invalid → deselect
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
        board = self.state.board

        self.state.legal_moves = [
            (rr, cc)
            for rr in range(8)
            for cc in range(8)
            if Rules.is_move_legal(
                    board,
                    r, c,
                    rr, cc,
                    self.state.turn,
                    self.state.last_move,
                    self.state.castling_rights,
                    self.state.frozen_square,
                    self.state.freeze_timer,
                    self.state.swap_bishop_square
                )

        ]


    def make_move(self, sr, sc, r, c):
        # Save undo snapshot
        self.state.history.append(self.state.snapshot())
        self.state.redo.clear()

        piece = self.state.board[sr][sc]

        # En passant
        self.state.en_passant_capture = None
        if piece.lower() == "p" and sc != c and self.state.board[r][c] == ".":
            self.state.en_passant_capture = (sr, c)

        self.state.pending_move = (sr, sc, r, c, piece)
        self.state.selected = None
        self.state.legal_moves = []

        self.state.animation.start(sr, sc, r, c, piece)
