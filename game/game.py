import pygame

from ui.ui import UI
from clock import ChessClock
from animation import MoveAnimation
from pgn import PGN
from rules import Rules, WHITE, BLACK


from .state import GameState
from .input import InputHandler
from .rules_engine import RulesEngine

from ai_engine import AIEngine


class Game:
    def __init__(self):
        pygame.init()
        self.ai = AIEngine()

        self.ui = UI()
        self.clock = ChessClock()
        self.animation = MoveAnimation()
        self.pgn = PGN()

        self.state = GameState(
            ui=self.ui,
            clock=self.clock,
            animation=self.animation,
            pgn=self.pgn
        )

        self.input = InputHandler(self.state)
        self.rules_engine = RulesEngine(self.state)

    # -------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------

    def run(self):
        fps = pygame.time.Clock()

        while True:
            fps.tick(60)

            # ---------- CLOCK ----------
            self.clock.update(self.state.turn, self.state.game_over)

            # ---------- ANIMATION ----------
            if self.animation.active:
                if self.animation.update():
                    self.state.finish_animation()

            # ---------- AI MOVE ----------
            if (
                self.state.game_mode == "pvc" and
                self.state.turn == BLACK and
                not self.state.animation.active and
                not self.state.promotion_square and
                not self.state.game_over
            ):
                sr, sc, dr, dc = self.ai.get_move(self.state.board, self.state.turn)
            
                piece = self.state.board[sr][sc]
                self.state.history.append(self.state.snapshot())
                self.state.pending_move = (sr, sc, dr, dc, piece)
                self.state.animation.start(sr, sc, dr, dc, piece)
            


            # ---------- GAME END CHECK ----------
            if not self.state.promotion_square:
                self.rules_engine.check_game_end()

            # ---------- SAVE PGN ONCE ----------
            if self.state.game_over and not self.state.pgn_saved:
                if "White wins" in self.state.result_text:
                    result = "1-0"
                elif "Black wins" in self.state.result_text:
                    result = "0-1"
                else:
                    result = "1/2-1/2"

                self.pgn.save(result)
                self.state.pgn_saved = True

            # ---------- EVENTS ----------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                # ----- PROMOTION INPUT (MODAL) -----
                if self.state.promotion_square:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_promotion_click(event.pos)
                    continue

                # ----- NORMAL INPUT -----
                self.input.handle_event(event)

            # ---------- DRAW ----------
            self.ui.draw(
            self.state.board,
            self.state.selected,
            self.state.legal_moves,
            self.clock,
            self.state.turn,
            self.state.game_over,
            self.state.result_text,
            self.animation,
            self.state.promotion_color,
            self.state.spells,
            self.state.frozen_square
        )

            
            
        
            # Promotion overlay on top (NO EXTRA LOOP)
            if self.state.promotion_square:
                self.ui.draw(
                    board=self.state.board,
                    selected=self.state.selected,
                    legal=self.state.legal_moves,
                    clock=self.clock,
                    turn=self.state.turn,
                    game_over=self.state.game_over,
                    text=self.state.result_text,
                    animation=self.state.animation,
                    promotion_color=self.state.promotion_color,
                    spells=self.state.spells,
                    frozen_square=self.state.frozen_square
                )
            

    # -------------------------------------------------
    # PROMOTION HANDLING
    # -------------------------------------------------

    def handle_promotion_click(self, pos):
        r, c = self.state.promotion_square
        color = self.state.promotion_color

        y = self.ui.WIDTH // 2 - self.ui.SQ // 2
        start_x = self.ui.WIDTH // 2 - 2 * self.ui.SQ

        for i, p in enumerate(["q", "r", "b", "n"]):
            rect = pygame.Rect(
                start_x + i * self.ui.SQ,
                y,
                self.ui.SQ,
                self.ui.SQ
            )
            if rect.collidepoint(pos):
                piece = p.upper() if color == WHITE else p
                self.state.board[r][c] = piece

                # PGN promotion
                self.state.pgn.add(
                    f"{chr(c + 97)}{8 - r}={p.upper()}"
                )

                self.state.turn = Rules.enemy(color)
                self.state.promotion_square = None
                self.state.promotion_color = None
                self.clock.reset_tick()
                break
