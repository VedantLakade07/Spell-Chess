# game/spells.py
from rules import WHITE, BLACK


class SpellSystem:

    @staticmethod
    def use_double_move(state):
        spells = state.spells[state.turn]
        if not spells["double_move"]:
            return
    
        spells["double_move"] = False
        state.double_move_active = True
    


    @staticmethod
    def use_freeze(state, pos):
        spells = state.spells[state.turn]
        if not spells["spell_2"]:
            return
    
        r, c = pos
        piece = state.board[r][c]
    
        if piece == ".":
            return
    
        if state.turn == WHITE and piece.isupper():
            return
        if state.turn == BLACK and piece.islower():
            return
    
        state.frozen_square = (r, c)
        state.freeze_timer = 3      # ❄️ freeze for 2 moves
        spells["spell_2"] = False
    
