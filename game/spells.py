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
        state.pgn.add_spell("DoubleMove")


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
        state.freeze_timer = 3
        spells["spell_2"] = False
        state.pgn.add_spell("Freeze", (r, c))


    @staticmethod
    def use_spell_3(state):
        spells = state.spells[state.turn]
        if not spells["spell_3"]:
            return
    
        state.bishop_any_direction = True
        state.queen_knight_move = True
        state.spell_3_active = True
    
        spells["spell_3"] = False
        state.pgn.add_spell("ChaosMove")
    
