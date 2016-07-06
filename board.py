"""
Amazonas Board Module
"""
import copy


class Board:
    """
    Amazonas Board
    """

    BLANK = '--'
    WHITE = 'W'
    BLACK = 'B'
    BLOCKED = 'xx'

    delta = [(-1, -1), (-1, 0), (-1, 1),
             ( 0, -1),          ( 0, 1),
             ( 1, -1), ( 1, 0), ( 1, 1)]

    @staticmethod
    def opponent(color):
        """
        Returns the opponent's color
        """
        if color == Board.WHITE:
            return Board.BLACK
        elif color == Board.BLACK:
            return Board.WHITE
        raise Exception("'%s' is not a Color" % color)

    def __init__(self, init_board=None):
        """
        Creates a new board or clones one
        """

        if init_board is None:
            self.board = []
            for _ in range(10):
                self.board.append([Board.BLANK]*10)

            self.queens = [[3, 0], [0, 3], [0, 6], [3, 9],
                           [6, 0], [9, 3], [9, 6], [6, 9]]
            num = 0
            for q in self.queens:
                if num < 4:
                    ch = Board.BLACK
                else:
                    ch = Board.WHITE
                self.board[q[0]][q[1]] = ch+str(num%4)
                num += 1
        else:
            self.board = copy.deepcopy(init_board.board)
            self.queens = copy.deepcopy(init_board.queens)

    def __repr__(self):
        s = "   "+"  ".join([str(i) for i in range(10)])+"\n"
        for i in range(10):
            s += str(i)+" "+" ".join(self.board[i]) + "\n"
        return s

    def __eq__(self, other):
        # Check type
        if not isinstance(other, Board):
            return False

        # Check queen lists
        for (s_q, o_q) in zip(self.queens, other.queens):
            if s_q != o_q:
                return False

        # Check board rows
        for (s_r, o_r) in zip(self.board, other.board):
            # Check row elements
            for (s_e, o_e) in zip(s_r, o_r):
                if s_e != o_e:
                    return False

        # No proof for `!=` found
        return True

    def __hash__(self):
        return hash(self.board.__repr__())

    def succ(self, queen, xf, yf, xb, yb):
        """
        returns a new board like self but with queen moved to xf,yf and position xb,yb blocked
        """
        bsucc = Board(self)

        (xi, yi) = self.queens[queen]

        bsucc.queens[queen] = (xf, yf)

        bsucc.board[xf][yf] = bsucc.board[xi][yi]
        bsucc.board[xi][yi] = Board.BLANK
        bsucc.board[xb][yb] = Board.BLOCKED

        return bsucc

    @staticmethod
    def queen2str(q):
        if q < 4:
            return Board.BLACK+str(q)
        return Board.WHITE+str(q%4)

    @staticmethod
    def show_move(color, q, xf, yf, xb, yb):
        print("%s moves amazona %d hasta (%d,%d) y dispara a (%d,%d)" % (color, q%4, xf,yf, xb,yb))

    def is_legal_jump(self, q, xi, yi, xf, yf):
        q_str = Board.queen2str(q)
        dx = xf - xi
        dy = yf - yi
        if dx == dy == 0 or (abs(dx)!=abs(dy) and abs(dx)!=0 and abs(dy)!=0):
            return False
        if dx!=0:
            dx //= abs(dx)
        if dy!=0:
            dy //= abs(dy)
        x = xi + dx
        y = yi + dy

        while True:
            if self.board[x][y] != Board.BLANK and self.board[x][y] != q_str:
                return False
            if (x, y) == (xf, yf):
                break
            x += dx
            y += dy

        return True

    def is_legal_move(self,queen,xf,yf):
        """
        true iff queen queen can move to xf to yf
        """
        (xi, yi) = self.queens[queen]

        return self.is_legal_jump(queen,xi,yi,xf,yf)

    def can_play(self, color):
        return self.moves(color, 1)!=[]

    def moves(self, color, limit=100000):
        if color==Board.BLACK:
            queens = range(4)
        else:
            queens = range(4,8)

        moves = []
        moves_count = 0
        for q in queens:
            queen_str = color + str(q%4)

            for (dx, dy) in Board.delta:
                xf = self.queens[q][0] + dx
                yf = self.queens[q][1] + dy

                while 0 <= xf < 10 and 0 <= yf < 10:
                    if self.board[xf][yf] != Board.BLANK:
                        break

                    for (ddx, ddy) in Board.delta:
                        xb = xf + ddx
                        yb = yf + ddy

                        while 0 <= xb < 10 and 0 <= yb < 10:
                            if self.board[xb][yb] != Board.BLANK and self.board[xb][yb] != queen_str:
                                break
                            moves.append((q,xf,yf,xb,yb))

                            moves_count += 1
                            if moves_count >= limit:
                                return moves

                            xb += ddx
                            yb += ddy
                    xf += dx
                    yf += dy
        return moves
