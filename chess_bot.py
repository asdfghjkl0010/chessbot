import pygame
from pygame.locals import *
import random


piece_moves = {
    'k': [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
    'n': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)],
    'r': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    'b': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    'q': [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
}


class ChessBot:
    def __init__(self, board, moves, threats, side):
        self.board = board
        self.moves = moves
        self.threats = threats
        self.side = side

    def generate_move(self):
        best_move = None
        best_score = self.evaluate_position(self.board)
        no_change=True
        okmove=[]
        for move in self.moves:
            # Make the move
            piece=self.board[move[0]][move[1]]
            temp=self.board[move[2]][move[3]]
            self.board[move[0]][move[1]] = ""
            self.board[move[2]][move[3]] = piece

            score=self.evaluate_position(self.board)
            
            if self.threats[move[2]][move[3]]==1 and temp!='':
                if self.piece_value(temp.name)>self.piece_value(piece.name):
                    score=1000
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                    no_change=False
            if self.threats[move[2]][move[3]]==0:
                okmove.append(move)
            # Undo the move
            self.board[move[0]][move[1]] = piece
            self.board[move[2]][move[3]] = temp

            
            if score==best_score:
                okmove.append(move)
        if no_change:
            r=random.randint(1,len(okmove))
            best_move=okmove[r-1]

        return best_move
    def evaluate_position(self, board):
        w_score=0
        b_score=0
        score=0
        for r in range(8):
            for c in range(8):
                piece=board[r][c]
                if piece!='':
                    if piece.color=='w':
                        w_score+=self.piece_value(piece.name)
                    elif piece.color=='b':
                        b_score+=self.piece_value(piece.name)
        points=[w_score,b_score]
        return w_score
    def piece_value(self, piece):
        score=0
        if piece=='p':
            score=1
        elif piece=='r':
            score=5
        elif piece=='n':
            score=3
        elif piece=='b':
            score=3
        elif piece=='q':
            score=9
        elif piece=='k':
            score=0
        return score
    def possible_threats(color):
        global threats
        threats = [[0 for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                if board[r][c]!='':
                    piece=board[r][c]
                    if piece.color!=color:
                        if piece.name=='p':
                            if piece.color=='w':
                                if c==0:
                                    threats[r-1][c+1]=1
                                elif c==7:
                                    threats[r-1][c-1]=1
                                else:
                                    threats[r-1][c+1]=1
                                    threats[r-1][c-1]=1
                            elif piece.color=='b':
                                if c==0:
                                    threats[r+1][c+1]=1
                                elif c==7:
                                    threats[r+1][c-1]=1
                                else:
                                    threats[r+1][c+1]=1
                                    threats[r+1][c-1]=1
                        else:
                            for dr, dc in piece_moves[piece.name]:
                                r1 = r + dr
                                c1 = c + dc
                                if piece.name=='k' or piece.name=='n':
                                    if 0 <= r1 < 8 and 0 <= c1 < 8:
                                       threats[r1][c1] = 1
                                else:
                                    while 0 <= r1 < 8 and 0 <= c1 < 8:
                                        if board[r1][c1]!='':
                                            threats[r1][c1]=1
                                            break
                                        threats[r1][c1]=1
                                        r1+=dr
                                        c1+=dc
        return threats
    def all_possible_moves():
        all_moves=[]
        for r in range(8):
            for c in range(8):
                piece=self.board[r][c]
                if board[r][c]!='' and piece.color==turn:         
                    possible_moves((r,c))
                    piece_moves=posmoves
                    if piece_moves:
                        for move in piece_moves:
                            all_moves.append((r, c, move[0], move[1]))
        for x in range(len(all_moves)-1,-1,-1):
            piece=board[all_moves[x][0]][all_moves[x][1]]
            temp=board[all_moves[x][2]][all_moves[x][3]]
            board[all_moves[x][0]][all_moves[x][1]]=""
            board[all_moves[x][2]][all_moves[x][3]]=piece
            for i in range(8):
                    for j in range(8):
                        if board[i][j]!="" and board[i][j].name=='k' and board[i][j].color==turn:
                                kr=i
                                kc=j
                #check if legal move
            possible_threats()
            if threats[kr][kc]==1:
                board[all_moves[x][0]][all_moves[x][1]]=piece
                board[all_moves[x][2]][all_moves[x][3]]=temp
                all_moves.pop(x)
            else:
                board[all_moves[x][0]][all_moves[x][1]]=piece
                board[all_moves[x][2]][all_moves[x][3]]=temp
        return all_moves
    def checkmate():
        for i in range(8):
            for j in range(8):
                if board[i][j]!="" and board[i][j].name=='k' and board[i][j].color==turn:
                    kr=i
                    kc=j
        a=possible_threats()
        if a[kr][kc]==1 and len(all_possible_moves())==0:
            if turn=='w':
                string="Checkmate! Black wins!"
            else:
                string='Checkmate! White Wins!'
