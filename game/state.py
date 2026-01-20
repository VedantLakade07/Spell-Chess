import copy
import pygame
from rules import Rules, WHITE, BLACK
from pgn import move_to_pgn
from .board import init_board


class GameState:
    def __init__(self, ui, clock, animation, pgn):

        self.swap_bishop_square = None

        self.ui = ui
        self.clock = clock
        self.animation = animation
        self.pgn = pgn

        self.reset()

    # -------------------------------------------------
    # RESET GAME
    # -------------------------------------------------

    def reset(self):
        self.board = init_board()

        self.turn = WHITE
        self.last_move = None

        self.selected = None
        self.legal_moves = []
        self.frozen_square = None
        self.freeze_timer = 0
        self.frozen_square = None
        self.freeze_timer = 0
        
        self.double_move_active = False


        self.history = []
        self.redo = []

        self.pending_move = None
        self.en_passant_capture = None

        self.promotion_square = None
        self.promotion_color = None

        self.game_over = False
        self.result_text = ""
        self.pgn_saved = False
        # --- SPELL 3 FLAGS ---
        self.bishop_any_direction = False
        self.queen_knight_move = False
        self.spell_3_active = False


        self.spells = {
            WHITE: {
                "double_move": True,
                "spell_2": True,
                "spell_3": True
            },
            BLACK: {
                "double_move": True,
                "spell_2": True,
                "spell_3": True
            }
        }




        self.double_move_active = False



        # ---- CASTLING RIGHTS ----
        self.castling_rights = {
            "white": {"K": True, "Q": True},
            "black": {"K": True, "Q": True}
        }

        # ---- CLOCK ----
        self.game_mode = self.ui.ask_game_mode()
        
        if self.game_mode == "pvc":
            self.clock.set_mode("none", 0, 0)
        else:
            mode, base, inc = self.ui.ask_time_screen()
            pygame.event.clear()
            self.clock.set_mode(mode, base, inc)
        

    # -------------------------------------------------
    # SNAPSHOT (UNDO / REDO)
    # -------------------------------------------------

    def snapshot(self):
        return (
            copy.deepcopy(self.board),
            self.turn,
            self.last_move,
            self.clock.white_time,
            self.clock.black_time,
            copy.deepcopy(self.castling_rights),
            list(self.pgn.moves),
            self.promotion_square,
            self.promotion_color
        )

    def restore(self, state):
        (
            self.board,
            self.turn,
            self.last_move,
            self.clock.white_time,
            self.clock.black_time,
            self.castling_rights,
            pgn_moves,
            self.promotion_square,
            self.promotion_color
        ) = state

        self.pgn.moves = list(pgn_moves)

        self.selected = None
        self.legal_moves = []
        self.pending_move = None
        self.en_passant_capture = None
        self.animation.active = False
        self.clock.reset_tick()

    # -------------------------------------------------
    # CASTLING RIGHTS UPDATE
    # -------------------------------------------------

    def update_castling_rights(self, piece, sr, sc):
        side = "white" if piece.isupper() else "black"

        if piece.lower() == "k":
            self.castling_rights[side]["K"] = False
            self.castling_rights[side]["Q"] = False

        if piece.lower() == "r":
            if sc == 0:
                self.castling_rights[side]["Q"] = False
            elif sc == 7:
                self.castling_rights[side]["K"] = False

    # -------------------------------------------------
    # APPLY MOVE AFTER ANIMATION
    # -------------------------------------------------

    def finish_animation(self):
        sr, sc, dr, dc, piece = self.pending_move
        mover = self.turn
    
        # ---------- EN PASSANT ----------
        capture = False
        if self.en_passant_capture:
            cr, cc = self.en_passant_capture
            self.board[cr][cc] = "."
            capture = True
        else:
            capture = self.board[dr][dc] != "."
    
        # ---------- CASTLING (ROOK MOVE) ----------
        if piece.lower() == "k" and abs(dc - sc) == 2:
            if dc > sc:  # king side
                self.board[dr][5] = self.board[dr][7]
                self.board[dr][7] = "."
            else:        # queen side
                self.board[dr][3] = self.board[dr][0]
                self.board[dr][0] = "."
    
        # ---------- APPLY MOVE ----------
        # ---------- CAPTURE DETECTION ----------
        captured_piece = self.board[dr][dc]
        
        # ---------- APPLY MOVE ----------
        self.board[dr][dc] = piece
        self.board[sr][sc] = "."
        
        # ---------- KING CAPTURE ----------
        if captured_piece.lower() == "k":
            self.game_over = True
            self.result_text = f"{mover.capitalize()} wins (King captured)"
            self.animation.active = False
            return
        

        # ---------- UPDATE CASTLING RIGHTS ----------
        self.update_castling_rights(piece, sr, sc)
    
        # ---------- PROMOTION ----------
        if piece.lower() == "p" and (dr == 0 or dr == 7):
            self.promotion_square = (dr, dc)
            self.promotion_color = mover
        else:
            self.pgn.add(
                move_to_pgn(sr, sc, dr, dc, piece, capture)
            
            )
        
        # ---------- SPELL 3 RESET (ONE MOVE ONLY) ----------
        ######################
        if self.spell_3_active:
            self.bishop_any_direction = False
            self.queen_knight_move = False
            self.spell_3_active = False


    
        # ---------- TURN HANDLING (DOUBLE MOVE FIX) ----------
        # ---------- TURN HANDLING ----------
        if self.double_move_active:
            self.double_move_active = False
        else:
            self.turn = Rules.enemy(mover)
            self.clock.on_move_complete(mover)


    
        # ---------- FINALIZE ----------
        self.last_move = (sr, sc, dr, dc, piece)
        self.pending_move = None
        self.en_passant_capture = None
        self.animation.active = False
    
        # ---------- FREEZE TIMER ----------
        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            if self.freeze_timer == 0:
                self.frozen_square = None

        #--------SWAP------------------
        if self.swap_bishop_square == (sr, sc):
            self.swap_bishop_square = None

    

    # -------------------------------------------------
    # COMPLETE PROMOTION
    # -------------------------------------------------

    def complete_promotion(self, promoted_piece):
        r, c = self.promotion_square
        mover = self.promotion_color

        self.board[r][c] = promoted_piece

        file = chr(c + 97)
        rank = 8 - r
        self.pgn.add(f"{file}{rank}={promoted_piece.upper()}")

        self.turn = Rules.enemy(mover)
        self.clock.on_move_complete(mover)

        self.promotion_square = None
        self.promotion_color = None
        self.clock.reset_tick()


    