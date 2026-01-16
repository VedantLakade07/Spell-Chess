from rules import Rules, WHITE, BLACK


class RulesEngine:
    def __init__(self, state):
        self.state = state

    def check_game_end(self):
                # No clock mode → skip time logic entirely
        if self.state.clock.mode == "none":
            pass
        
        if self.state.game_over or self.state.animation.active:
            return

        flagged = self.state.clock.is_flagged()
        if self.state.clock.mode != "none":
            flagged = self.state.clock.is_flagged()
            if flagged:
                winner = BLACK if flagged == WHITE else WHITE
                self.state.result_text = f"{winner.capitalize()} wins on time"
                self.state.game_over = True
                return
        

        state = Rules.game_state(
            self.state.board,
            self.state.turn,
            self.state.last_move
        )

        if state == "checkmate":
            self.state.result_text = f"CHECKMATE! {Rules.enemy(self.state.turn).capitalize()} wins"
            self.state.game_over = True

        elif state == "stalemate":
            self.state.result_text = "STALEMATE! Draw"
            self.state.game_over = True
