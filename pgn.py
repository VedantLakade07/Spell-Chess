from datetime import datetime

def square_to_notation(r, c):
    return chr(c + 97) + str(8 - r)

def move_to_pgn(sr, sc, dr, dc, piece, capture):
    p = piece.lower()
    dest = square_to_notation(dr, dc)

    if p == "p":
        return (square_to_notation(sr, sc)[0] + "x" + dest) if capture else dest

    return p.upper() + ("x" if capture else "") + dest

class PGN:
    def __init__(self):
        self.moves = []

    def add(self, move):
        self.moves.append(move)

    def save(self, result):
        name = datetime.now().strftime("game_%Y-%m-%d_%H-%M-%S.pgn")
        with open(name, "w") as f:
            f.write(f"[Event \"Casual Game\"]\n")
            f.write(f"[Site \"Local\"]\n")
            f.write(f"[Date \"{datetime.now().strftime('%Y.%m.%d')}\"]\n")
            f.write("[Round \"-\"]\n")
            f.write("[White \"White\"]\n")
            f.write("[Black \"Black\"]\n")
            f.write(f"[Result \"{result}\"]\n\n")

            for i in range(0, len(self.moves), 2):
                line = f"{i//2 + 1}. {self.moves[i]}"
                if i + 1 < len(self.moves):
                    line += f" {self.moves[i+1]}"
                f.write(line + "\n")
