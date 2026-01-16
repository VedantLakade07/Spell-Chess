# rules.py
import copy

EMPTY = "."

WHITE, BLACK = "white", "black"

class Rules:
    @staticmethod
    def in_bounds(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    @staticmethod
    def enemy(color):
        return BLACK if color == WHITE else WHITE

    @staticmethod
    def is_white(piece):
        return piece.isupper()

    @staticmethod
    def find_king(board, color):
        k = "K" if color == WHITE else "k"
        for r in range(8):
            for c in range(8):
                if board[r][c] == k:
                    return r, c
        return None

    # ---------- CHECK / ATTACK ---------- #

    @staticmethod
    def is_king_in_check(board, color):
        kr, kc = Rules.find_king(board, color)
        return Rules.is_square_attacked(board, kr, kc, Rules.enemy(color))

    @staticmethod
    def is_square_attacked(board, r, c, attacker):
        for sr in range(8):
            for sc in range(8):
                p = board[sr][sc]
                if p == EMPTY:
                    continue
                if attacker == WHITE and p.islower():
                    continue
                if attacker == BLACK and p.isupper():
                    continue
                if Rules.attacks(board, sr, sc, r, c):
                    return True
        return False

    # ---------- ATTACK LOGIC ---------- #

    @staticmethod
    def ray_clear(board, sr, sc, tr, tc):
        dr = (tr - sr) // max(1, abs(tr - sr)) if tr != sr else 0
        dc = (tc - sc) // max(1, abs(tc - sc)) if tc != sc else 0
        r, c = sr + dr, sc + dc
        while (r, c) != (tr, tc):
            if board[r][c] != EMPTY:
                return False
            r += dr
            c += dc
        return True

    @staticmethod
    def attacks(board, sr, sc, tr, tc):
        p = board[sr][sc].lower()
        dr, dc = tr - sr, tc - sc

        if p == "p":
            direction = -1 if board[sr][sc].isupper() else 1
            return dr == direction and abs(dc) == 1

        if p == "n":
            return (abs(dr), abs(dc)) in [(2,1),(1,2)]

        if p == "k":
            return max(abs(dr), abs(dc)) == 1

        if p == "r":
            return (dr == 0 or dc == 0) and Rules.ray_clear(board, sr, sc, tr, tc)

        if p == "b":
            return abs(dr) == abs(dc) and Rules.ray_clear(board, sr, sc, tr, tc)

        if p == "q":
            return (dr == 0 or dc == 0 or abs(dr) == abs(dc)) and Rules.ray_clear(board, sr, sc, tr, tc)

        return False

    # ---------- MOVE VALIDATION ---------- #

    @staticmethod
    def is_move_legal(board, sr, sc, dr, dc, color, last_move):
        if not Rules.in_bounds(dr, dc):
            return False

        piece = board[sr][sc]
        target = board[dr][dc]

        if target != EMPTY:
            if piece.isupper() == target.isupper():
                return False

        if not Rules.valid_piece_move(board, sr, sc, dr, dc, piece, last_move):
            return False

        temp = copy.deepcopy(board)

        # En passant removal
        if piece.lower() == "p" and sc != dc and board[dr][dc] == EMPTY:
            temp[sr][dc] = EMPTY

        temp[dr][dc] = temp[sr][sc]
        temp[sr][sc] = EMPTY

        return not Rules.is_king_in_check(temp, color)

    @staticmethod
    def valid_piece_move(board, sr, sc, dr, dc, piece, last_move):
        p = piece.lower()
        drc, dcc = dr - sr, dc - sc

        # ---------- PAWN ----------
        if p == "p":
            direction = -1 if piece.isupper() else 1
            start = 6 if piece.isupper() else 1

            if dcc == 0:
                if drc == direction and board[dr][dc] == EMPTY:
                    return True
                if sr == start and drc == 2 * direction:
                    return board[sr + direction][dc] == EMPTY and board[dr][dc] == EMPTY

            if abs(dcc) == 1 and drc == direction:
                if board[dr][dc] != EMPTY:
                    return True
                if last_move:
                    lsr, lsc, ldr, ldc, lp = last_move
                    if lp.lower() == "p" and abs(lsr - ldr) == 2 and ldr == sr and ldc == dc:
                        return True
            return False

        # ---------- KNIGHT ----------
        if p == "n":
            return (abs(drc), abs(dcc)) in [(2,1),(1,2)]

        # ---------- KING ----------
        if p == "k":
            # Normal king move
            if max(abs(drc), abs(dcc)) == 1:
                return True

            # Castling must stay on same rank
            if dr != sr:
                return False

            return Rules.can_castle(board, sr, sc, dc, piece)

        # ---------- ROOK ----------
        if p == "r":
            return (drc == 0 or dcc == 0) and Rules.ray_clear(board, sr, sc, dr, dc)

        # ---------- BISHOP ----------
        if p == "b":
            return abs(drc) == abs(dcc) and Rules.ray_clear(board, sr, sc, dr, dc)

        # ---------- QUEEN ----------
        if p == "q":
            return (drc == 0 or dcc == 0 or abs(drc) == abs(dcc)) and Rules.ray_clear(board, sr, sc, dr, dc)

        return False

    @staticmethod
    def can_castle(board, r, c, dc, king):
        color = WHITE if king.isupper() else BLACK

        if Rules.is_king_in_check(board, color):
            return False

        # King-side
        if dc - c == 2:
            rook_col = 7
            path = [c + 1, c + 2]

        # Queen-side
        elif c - dc == 2:
            rook_col = 0
            path = [c - 1, c - 2, c - 3]

        else:
            return False

        if board[r][rook_col].lower() != "r":
            return False

        for col in path:
            if board[r][col] != EMPTY:
                return False
            if col != path[-1]:
                if Rules.is_square_attacked(board, r, col, Rules.enemy(color)):
                    return False

        return True

    # ---------- GAME STATE ---------- #

    @staticmethod
    def has_legal_move(board, color, last_move):
        for sr in range(8):
            for sc in range(8):
                piece = board[sr][sc]
                if piece == EMPTY:
                    continue
                if color == WHITE and piece.islower():
                    continue
                if color == BLACK and piece.isupper():
                    continue
                for dr in range(8):
                    for dc in range(8):
                        if Rules.is_move_legal(board, sr, sc, dr, dc, color, last_move):
                            return True
        return False

    @staticmethod
    def game_state(board, color, last_move):
        in_check = Rules.is_king_in_check(board, color)
        has_move = Rules.has_legal_move(board, color, last_move)

        if in_check and not has_move:
            return "checkmate"
        if not in_check and not has_move:
            return "stalemate"
        if in_check:
            return "check"
        return "normal"
