import sys
from math import sqrt, log
from random import choice
from signal import alarm, signal, SIGALRM
from board import Board


class WolfPlayer:
    """Iván Wolf"""

    def __init__(self, color, time=0, h=1):
        """
        h: Wich heuristic should I use? 1: Offensive, 2: Defensive
        """
        self.color = color
        self.time = time
        self.turno = 0
        self.h = h

    def play(self, board_copy):
        def handler(signum, frame):
            raise IOError

        signal(SIGALRM, handler)
        alarm(self.time)

        try:  # UCT
            root = Node(board_copy, self.color)
            while self.time:
                v = Node.tree_policy(root, self.h)
                delta = Node.default_policy(v.board, self.color)
                v.backup(delta)

        except IOError:  # here quickly obtain a move
            alarm(0)
            jugada = Node.best_child(root, 0).jugada

        # here we return a solution very quickly
        q, xf, yf, xb, yb = jugada

        if (not board_copy.is_legal_move(q, xf, yf) or
                not board_copy.is_legal_jump(q, xf, yf, xb, yb)):
            print("--------------------movida ilegal!??!")
            input("")
        self.turno += 1
        return q, xf, yf, xb, yb


class Node:
    CONS = 1 / sqrt(2)

    def __init__(self, board, color, parent=None, jugada=None):
        self.board = board
        self.color = color  # El color indica a quien le toca jugar
        self.jugada = jugada  # La jugada es el movimiento que genero este tablero
        self.parent = parent
        self.hijos = []
        self.n = 0
        self.q = 0
        self.movimientos = []

    def __repr__(self):
        return repr(self.board)

    @property
    def is_terminal(self):
        if self.board.can_play(self.color):
            return False
        return True

    @property
    def can_expand(self):
        if len(self.movimientos) == len(self.board.moves(self.color)):
            return False
        return True

    def expand(self, h):
        moves = self.board.moves(self.color)
        h_min = 10000000

        for play in moves:
            next_board = self.board.succ(*play)
            if h == 1:
                h_value = Node.heuristic(next_board, self.color)
            elif h == 2:
                h_value = Node.heuristic_2(next_board, self.color)

            if h_value <= h_min:
                best_board = next_board
                best_play = play
                h_min = h_value

        new_node = Node(best_board, Board.opponent(self.color), self, best_play)
        self.hijos.append(new_node)
        return new_node

    def backup(self, delta):
        node = self
        while node is not None:
            node.n += 1
            node.q += delta
            delta = -1 * delta
            node = node.parent

    @staticmethod
    def heuristic(board, color):
        return len(board.moves(Board.opponent(color)))

    @staticmethod
    def heuristic_2(board, color):
        return -1 * len(board.moves(color))

    @staticmethod
    def tree_policy(node, h):
        while not node.is_terminal:
            if node.can_expand:
                return node.expand(h)
            else:
                node = Node.best_child(node, Node.CONS)

    @staticmethod
    def best_child(node, c):
        def func(hijo):
            if hijo.n > 0:
                result = hijo.q / hijo.n + c * sqrt(2 * log(hijo.parent.n) / hijo.n)
            else:
                result = 10000000
            return result

        lista = [func(hijo) for hijo in node.hijos]
        f_max = -1
        for i, value in enumerate(lista):
            if value >= f_max:
                index = i
        try:
            return node.hijos[index]
        except UnboundLocalError:
            print('Necesito más tiempo, puedes darme un segundo más pora pensar mi jugada')
            sys.exit()

    @staticmethod
    def default_policy(board, color):
        board = Board(board)

        while True:
            if board.can_play(Board.WHITE):
                moves = board.moves(Board.WHITE)
                q, xf, yf, xb, yb = choice(moves)
            else:
                winner = Board.BLACK
                break
            board = board.succ(q, xf, yf, xb, yb)

            if board.can_play(Board.BLACK):
                moves = board.moves(Board.BLACK)
                q, xf, yf, xb, yb = choice(moves)
            else:
                winner = Board.WHITE
                break
            board = board.succ(q, xf, yf, xb, yb)

        if winner == color:
            return 1
        else:
            return -1
