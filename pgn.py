from datetime import datetime

# ------------------ HELPERS ------------------

def square_to_notation(r, c):
    return chr(c + 97) + str(8 - r)

def move_to_pgn(sr, sc, dr, dc, piece, capture):
    p = piece.lower()
    dest = square_to_notation(dr, dc)

    if p == "p":
        return (square_to_notation(sr, sc)[0] + "x" + dest) if capture else dest

    return p.upper() + ("x" if capture else "") + dest


# ------------------ PGN CLASS ------------------

class PGN:
    def __init__(self):
        self.moves = []

    # Normal chess move
    def add(self, move):
        self.moves.append(move)

    # Spell move (stored as PGN comment)
    def add_spell(self, spell_name, square=None, extra=None):
        """
        spell_name : str  -> 'DoubleMove', 'Freeze', 'Swap'
        square     : (r,c) or None
        extra      : optional text
        """

        text = spell_name

        if square:
            text += " " + square_to_notation(*square)

        if extra:
            text += f" ({extra})"

        # PGN-safe comment
        self.moves.append(f"{{{text}}}")

    # Save PGN file
    def save(self, result):
        name = datetime.now().strftime("game_%Y-%m-%d_%H-%M-%S.pgn")

        with open(name, "w") as f:
            f.write('[Event "Casual Game"]\n')
            f.write('[Site "Local"]\n')
            f.write(f'[Date "{datetime.now().strftime("%Y.%m.%d")}"]\n')
            f.write('[Round "-"]\n')
            f.write('[White "White"]\n')
            f.write('[Black "Black"]\n')
            f.write(f'[Result "{result}"]\n\n')

            move_number = 1
            i = 0

            while i < len(self.moves):
                # White move
                line = f"{move_number}. {self.moves[i]}"
                i += 1

                # Black move (if exists and is not a comment-only line)
                if i < len(self.moves):
                    line += f" {self.moves[i]}"
                    i += 1

                f.write(line + "\n")
                move_number += 1
