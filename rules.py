# rules.py
import copy

EMPTY = "."
WHITE, BLACK = "white", "black"


class Rules:

    # ---------- BASIC HELPERS ----------

    @staticmethod
    def in_bounds(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    @staticmethod
    def enemy(color):
        return BLACK if color == WHITE else WHITE

    @staticmethod
    def find_king(board, color):
        k = "K" if color == WHITE else "k"
        for r in range(8):
            for c in range(8):
                if board[r][c] == k:
                    return r, c
        return None

    # ---------- CHECK / ATTACK ----------

    @staticmethod
    def is_king_in_check(board, color):
        pos = Rules.find_king(board, color)
        if pos is None:
            return True  # king is gone → treated as checkmate
        kr, kc = pos
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

    # ---------- ATTACK LOGIC ----------

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
            return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]

        if p == "k":
            return max(abs(dr), abs(dc)) == 1

        if p == "r":
            return (dr == 0 or dc == 0) and Rules.ray_clear(board, sr, sc, tr, tc)

        if p == "b":
            return abs(dr) == abs(dc) and Rules.ray_clear(board, sr, sc, tr, tc)

        if p == "q":
            return (dr == 0 or dc == 0 or abs(dr) == abs(dc)) and Rules.ray_clear(board, sr, sc, tr, tc)

        return False

    # ---------- MOVE VALIDATION ----------

    @staticmethod
    def is_move_legal(
        board, sr, sc, dr, dc,
        color, last_move,
        castling_rights,
        frozen_square,
        freeze_timer,
        swap_bishop_square,
        bishop_any_direction=False,
        queen_knight_move=False
    ):

        # Frozen piece cannot move
        # ---------- FREEZE ----------
        if (
            freeze_timer > 0
            and frozen_square is not None
            and (sr, sc) == frozen_square
        ):
            return False

        
        



        if not Rules.in_bounds(dr, dc):
            return False

        piece = board[sr][sc]
        target = board[dr][dc]

        if target != EMPTY and piece.isupper() == target.isupper():
            return False

        if not Rules.valid_piece_move(
            board, sr, sc, dr, dc,
            piece, last_move,
            castling_rights,
            swap_bishop_square,
            bishop_any_direction,
            queen_knight_move
        ):

            return False

        temp = copy.deepcopy(board)

        # En passant
        if piece.lower() == "p" and sc != dc and board[dr][dc] == EMPTY:
            temp[sr][dc] = EMPTY

        temp[dr][dc] = temp[sr][sc]
        temp[sr][sc] = EMPTY

        # If king is captured, allow move (game will end immediately)
        if Rules.find_king(temp, color) is None:
            return True

        return not Rules.is_king_in_check(temp, color)


    @staticmethod
    def valid_piece_move(
        board, sr, sc, dr, dc,
        piece, last_move,
        castling_rights,
        swap_bishop_square,
        bishop_any_direction=False,
        queen_knight_move=False
    ):

        p = piece.lower()
        drc, dcc = dr - sr, dc - sc

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

        if p == "n":
            return (abs(drc), abs(dcc)) in [(2, 1), (1, 2)]

        if p == "k":
            if max(abs(drc), abs(dcc)) == 1:
                return True
            if dr != sr:
                return False
            return Rules.can_castle(board, sr, sc, dc, piece, castling_rights)

        if p == "r":
            return (drc == 0 or dcc == 0) and Rules.ray_clear(board, sr, sc, dr, dc)

        if p == "b":
            # Spell 3 OR old swap-bishop logic
            if bishop_any_direction or swap_bishop_square == (sr, sc):
                return max(abs(drc), abs(dcc)) == 1

            return abs(drc) == abs(dcc) and Rules.ray_clear(board, sr, sc, dr, dc)




        if p == "q":
            # Normal queen move
            if (drc == 0 or dcc == 0 or abs(drc) == abs(dcc)) and Rules.ray_clear(board, sr, sc, dr, dc):
                return True

            # Spell 3: Queen moves like knight
            if queen_knight_move:
                return (abs(drc), abs(dcc)) in [(2, 1), (1, 2)]

            return False


        return False

    @staticmethod
    def can_castle(board, r, c, dc, king, castling_rights):
        color = WHITE if king.isupper() else BLACK
        side = "white" if color == WHITE else "black"

        if Rules.is_king_in_check(board, color):
            return False

        if dc - c == 2:
            if not castling_rights[side]["K"]:
                return False
            rook_col = 7
            path = [c + 1, c + 2]

        elif c - dc == 2:
            if not castling_rights[side]["Q"]:
                return False
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

    # ---------- GAME STATE ----------

    @staticmethod
    def has_legal_move(
        board, color, last_move,
        castling_rights,
        frozen_square,
        freeze_timer,
        swap_bishop_square,
        bishop_any_direction=False,
        queen_knight_move=False
    ):


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
                        if Rules.is_move_legal(
                            board,
                            sr, sc, dr, dc,
                            color,
                            last_move,
                            castling_rights,
                            frozen_square,
                            freeze_timer,
                            swap_bishop_square,
                            bishop_any_direction,
                            queen_knight_move
                        ):

                            return True
        return False

    @staticmethod
    def game_state(
        board, color, last_move,
        castling_rights,
        frozen_square,
        freeze_timer,
        swap_bishop_square,
        bishop_any_direction=False,
        queen_knight_move=False
    ):


        # ---------- KING MISSING ----------
        if Rules.find_king(board, color) is None:
            return "checkmate"


        in_check = Rules.is_king_in_check(board, color)
        has_move = Rules.has_legal_move(
            board,
            color,
            last_move,
            castling_rights,
            frozen_square,
            freeze_timer,
            swap_bishop_square,
            bishop_any_direction,
            queen_knight_move
        )



        if in_check and not has_move:
            return "checkmate"
        if not in_check and not has_move:
            return "stalemate"
        if in_check:
            return "check"
        return "normal"
