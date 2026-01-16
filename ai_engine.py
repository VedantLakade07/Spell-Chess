import os
import chess
import chess.engine


class AIEngine:
    def __init__(self):
        # Absolute path based on THIS file location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        engine_path = os.path.join(base_dir, "engine", "stockfish.exe")

        print("Stockfish path:", engine_path)
        print("Exists:", os.path.exists(engine_path))

        if not os.path.exists(engine_path):
            raise FileNotFoundError(f"Stockfish not found at {engine_path}")

        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    def get_move(self, board, turn):
        rows = []
        for r in board:
            empty = 0
            row = ""
            for p in r:
                if p == ".":
                    empty += 1
                else:
                    if empty:
                        row += str(empty)
                        empty = 0
                    row += p
            if empty:
                row += str(empty)
            rows.append(row)

        side = "w" if turn == "white" else "b"
        fen = "/".join(rows) + f" {side} - - 0 1"

        chess_board = chess.Board(fen)
        result = self.engine.play(
            chess_board,
            chess.engine.Limit(depth=12)
        )

        move = result.move

        return (
            7 - (move.from_square // 8),
            move.from_square % 8,
            7 - (move.to_square // 8),
            move.to_square % 8
        )

    def quit(self):
        self.engine.quit()
