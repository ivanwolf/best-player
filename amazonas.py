import copy
import random
import signal
import math
import sys


BLANK='--'
WHITE='W'
BLACK='B'
BLOCKED='XX'

class Board:
    def __init__(self,init_board=None):
        # create an initial board
        if init_board==None:
            self.board=[]
            for i in range(0,10):
                self.board.append([BLANK]*10)
            self.queens = [[3,0],[0,3],[0,6],[3,9],[6,0],[9,3],[9,6],[6,9]]
            num=0
            for q in self.queens:
                if num < 4:
                    ch = BLACK
                else:
                    ch = WHITE
                self.board[q[0]][q[1]] = ch+str(num%4)
                num += 1
        else:
            self.board  = copy.deepcopy(init_board.board)
            self.queens = copy.deepcopy(init_board.queens)

    def __repr__(self):
        s = "   "+"  ".join([str(i) for i in range(0,10)])+"\n"
        for i in range(0,10):
            s += str(i)+" "+" ".join(self.board[i]) + "\n"
        return s

    def succ(self,queen,xf,yf,xb,yb):
         # returns a new board like self but with queen moved to xf,yf and position xb,yb blocked
        bsucc=Board(self)
        xi=self.queens[queen][0]
        yi=self.queens[queen][1]
        bsucc.queens[queen][0] = xf
        bsucc.queens[queen][1] = yf
        bsucc.board[xf][yf] = bsucc.board[xi][yi]
        bsucc.board[xi][yi] = BLANK
        bsucc.board[xb][yb] = BLOCKED
        return bsucc

    def queen2str(q):
        if q<4:
            return BLACK+str(q)
        return WHITE+str(q%4)

    def show_move(color,q,xf,yf,xb,yb):
        print("Jugador",color,"mueve reina",q%4,"hasta","("+str(xf)+","+str(yf)+")","bloqueando","("+str(xb)+","+str(yb)+")"+"\n")

    def is_legal_jump(self,q,xi,yi,xf,yf):
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
            if self.board[x][y] != BLANK and self.board[x][y] != q_str:
                return False
            if (x,y) == (xf,yf):
                break
            x += dx
            y += dy

        return True


    def is_legal_move(self,queen,xf,yf):
        # true iff queen queen can move to xf to yf
        xi=self.queens[queen][0]
        yi=self.queens[queen][1]
        return self.is_legal_jump(queen,xi,yi,xf,yf)

    def can_play(self,color):
        return self.moves(color,1)!=[]

    def moves(self,color,limit=100000):
        n = 0
        if color==BLACK:
            queens = range(0,4)
        else:
            queens = range(4,8)
        moves = []
        for q in queens:
            queen_str=color+str(q%4)
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx==dy==0:
                        continue
                    xf=self.queens[q][0]+dx
                    yf=self.queens[q][1]+dy
                    while 0<=xf<10 and 0<=yf<10:
                        if self.board[xf][yf] != BLANK:
                            break
                        for ddx in [-1,0,1]:
                            for ddy in [-1,0,1]:
                                if ddx==ddy==0:
                                    continue
                                xb=xf+ddx
                                yb=yf+ddy
                                while 0<=xb<10 and 0<=yb<10:
                                    if self.board[xb][yb] != BLANK and self.board[xb][yb] != queen_str:
                                        break
                                    moves.append((q,xf,yf,xb,yb))
                                    n += 1
                                    if n == limit:
                                        return moves
                                    xb += ddx
                                    yb += ddy
                        xf += dx
                        yf += dy
        return moves

class HumanPlayer:
    def __init__(self,color):
        self.color = color

    def play(self):
        while True:
            q = int(input("Jugador, "+self.color+" ingrese número de reina a mover (0-4): "))
            if q in range(0,5):
                break
            print("Input no válido")

        if self.color == WHITE:
            q += 4
        while True:
            inp = input("Jugador, "+self.color+" ingrese posición de destino (fila columna): ")
            l=inp.split()
            xf=int(l[0])
            yf=int(l[1])
            if not xf in range(0,10) or not yf in range(0,10):
                print("Posición fuera del tablero")
                continue
            if main_board.is_legal_move(q,xf,yf):
                break
            print("Movida ilegal")


        while True:
            inp = input("Jugador, "+self.color+" ingrese posición de bloqueo (fila columna): ")
            l=inp.split()
            xb=int(l[0])
            yb=int(l[1])
            if not xb in range(0,10) or not yb in range(0,10):
                print("Posición fuera del tablero")
                continue
            if main_board.is_legal_jump(q,xf,yf,xb,yb):
                break;
            print("Posición ilegal",xf,yf,xb,yb)
        return q,xf,yf,xb,yb

class RandomPlayer:
    def __init__(self,color,time=1):
        self.color = color
        self.time = time

    def play(self):
        def handler(signum, frame):
            raise IOError

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.time)

        try:  ## here we do the hard computation
            moves=main_board.moves(self.color)
            x=0
            while self.time:  # pretend we are doing something unless time is 0
                x=x+1

        except IOError: ## here quickly obtain a move
            signal.alarm(0)


        # here we return a solution very quickly
        q,xf,yf,xb,yb = random.choice(moves)

        if not main_board.is_legal_move(q,xf,yf) or not main_board.is_legal_jump(q,xf,yf,xb,yb):
            print("--------------------movida ilegal!??!")
            input("")
        return q,xf,yf,xb,yb

############
# Acá empeiza mi codigo
############


class Nodo:
    def __init__(self, board, color, parent=None, jugada=None):
        self.board = board
        self.color = color #El color indica a quien le toca jugar
        self.jugada = jugada #La jugada es el movimiento que genero este tablero
        self.parent = parent
        self.hijos = []
        self.n = 0
        self.q = 0
        self.movimientos = []


    def __repr__(self):
        return repr(self.board)

    @property
    def es_terminal(self):
        if self.board.can_play(self.color):
            return False
        return True

    @property
    def se_puede_expandir(self):
        if len(self.movimientos) == len(self.board.moves(self.color)):
            return False
        return True

    def expand(self, turno):
        moves = self.board.moves(self.color)

        h_min = 10000000

        for movimiento in moves:
            next_board = self.board.succ(*movimiento)
            h_value = heuristic(next_board, self.color, turno)

            if h_value <= h_min:
                best_board = next_board
                jugada = movimiento
                h_min = h_value

        nuevo_nodo = Nodo(best_board, otro_color(self.color), self, jugada)
        self.hijos.append(nuevo_nodo)
        return nuevo_nodo

def heuristic(board, color, turno):

    return len(board.moves(otro_color(color)))



def tree_policy(nodo, turno):
    while not nodo.es_terminal:
        if nodo.se_puede_expandir:
            return nodo.expand(turno)
        else:
            nodo = best_child(nodo, CONS)

def best_child(nodo, c):
    def func(hijo):
        if hijo.n > 0:
            result = hijo.q / hijo.n + c * math.sqrt(2 * math.log(hijo.parent.n) / hijo.n)
        else:
            result = 10000000
        return result
    lista = list(map(func, nodo.hijos))

    f_max = -1

    for i in range(len(lista)):
        if lista[i] >= f_max:
            index = i
    try:
        return nodo.hijos[index]
    except UnboundLocalError:
        print('Necesito más tiempo, puedes darme un segundo más pora pensar mi jugada')
        sys.exit()

def backup(nodo, delta):
    while nodo is not None:
        nodo.n += 1
        nodo.q += delta
        delta = -1 * delta
        nodo = nodo.parent


def default_policy(board, color):
    board = Board(board)

    while True:
        if board.can_play(WHITE):
            moves = board.moves(WHITE)
            q,xf,yf,xb,yb = random.choice(moves)
        else:
            winner = BLACK
            break
        board = board.succ(q, xf, yf, xb, yb)

        if board.can_play(BLACK):
            moves = board.moves(BLACK)
            q,xf,yf,xb,yb = random.choice(moves)
        else:
            winner = WHITE
            break
        board = board.succ(q, xf, yf, xb, yb)

    if winner == color:
        return 1
    else:
        return -1


def otro_color(color):
    if color == WHITE:
        return BLACK
    elif color == BLACK:
        return WHITE

class BestPlayer:
    def __init__(self,color,time=1):
        self.color = color
        self.time = time
        self.turno = 0

    def play(self):
        def handler(signum, frame):
            raise IOError

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.time)

        try:  ## here we do the hard computation
            root = Nodo(main_board, self.color)
            while self.time:  # pretend we are doing something unless time is 0
                v = tree_policy(root, self.turno)
                delta = default_policy(v.board, self.color)
                backup(v, delta)

        except IOError: ## here quickly obtain a move
            signal.alarm(0)
            jugada = best_child(root, 0).jugada

        # here we return a solution very quickly
        q,xf,yf,xb,yb = jugada

        if not main_board.is_legal_move(q,xf,yf) or not main_board.is_legal_jump(q,xf,yf,xb,yb):
            print("--------------------movida ilegal!??!")
            input("")
        self.turno += 1
        return q,xf,yf,xb,yb

############
# MAIN
############

if __name__ == '__main__':



    main_board=Board()

    player_white = BestPlayer(BLACK,4) # Random Player (fast)
    player_black = RandomPlayer(WHITE,0) # Random Player (one sec per move)

    plays = 0

    while True:
        print(main_board)
        if main_board.can_play(WHITE):
            q,xf,yf,xb,yb = player_white.play()
            Board.show_move(WHITE,q,xf,yf,xb,yb)
            plays += 1
        else:
            print("Jugador",BLACK,"ha ganado")
            break
        main_board = main_board.succ(q,xf,yf,xb,yb)
        print('posibles_jugadas', len(main_board.moves(WHITE)))
        print(main_board)
        if main_board.can_play(BLACK):
            q,xf,yf,xb,yb = player_black.play()
            Board.show_move(BLACK,q,xf,yf,xb,yb)
            plays += 1
        else:
            print("Jugador",WHITE,"ha ganado")
            break
        main_board = main_board.succ(q,xf,yf,xb,yb)

    print("Fin del juego en",plays,"jugadas.")
