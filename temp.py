import chess
import chess.engine
import os

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, "engine", "stockfish.exe")

print("Exists:", os.path.exists(path))
print("Absolute:", path)

engine = chess.engine.SimpleEngine.popen_uci(path)
board = chess.Board()
print(engine.play(board, chess.engine.Limit(depth=8)))
engine.quit()
