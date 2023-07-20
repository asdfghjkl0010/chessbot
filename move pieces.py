#PHASE 1: import pygame, setup board
#pygame setup
import pygame
from pygame.locals import *
pygame.init()
window = pygame.display.set_mode((640, 640))
window.fill((255, 255, 255))

#create the pieces class
class Piece:
    def __init__(self,color,name,image):
        self.color=color
        self.name=name
        self.image=pygame.image.load(image)

#create pieces
wp=Piece('w','p','wp.png')
wp.image=pygame.transform.scale(wp.image,(40,40))
bp=Piece('b','p','bp.png')
bp.image=pygame.transform.scale(bp.image,(40,40))
wr=Piece('w','r','wr.png')
wr.image=pygame.transform.scale(wr.image,(40,40))
br=Piece('b','r','br.png')
br.image=pygame.transform.scale(br.image,(40,40))
wn=Piece('w','n','wn.png')
wn.image=pygame.transform.scale(wn.image,(40,40))
bn=Piece('b','n','bn.png')
bn.image=pygame.transform.scale(bn.image,(40,40))
wb=Piece('w','b','wb.png')
wb.image=pygame.transform.scale(wb.image,(40,40))
bb=Piece('b','b','bb.png')
bb.image=pygame.transform.scale(bb.image,(40,40))
wq=Piece('w','q','wq.png')
wq.image=pygame.transform.scale(wq.image,(40,40))
bq=Piece('b','q','bq.png')
bq.image=pygame.transform.scale(bq.image,(40,40))
wk=Piece('w','k','wk.png')
wk.image=pygame.transform.scale(wk.image,(40,40))
bk=Piece('b','k','bk.png')
bk.image=pygame.transform.scale(bk.image,(40,40))

#create a board array
board=[
    [br,bn,bb,bq,bk,bb,bn,br],
    [bp,bp,bp,bp,bp,bp,bp,bp],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    [wp,wp,wp,wp,wp,wp,wp,wp],
    [wr,wn,wb,wq,wk,wb,wn,wr]
    ]

#create and setup board
def drawboard():
    x = 0
    y = 0
    for i in range(8):
        for j in range(8):
            if i % 2 != j % 2:
                pygame.draw.rect(window, (0, 0, 0), [x, y, 80, 80], 0)
            if board[i][j] != "":
                window.blit(board[i][j].image,(x+20,y+20))
            x += 80
        x = 0
        y += 80

#updates to display the board and pieces
drawboard()
pygame.display.update()

#PHASE 2: code rules for pieces
posmoves=[]
enpassant=False
castle=True
piece_moves = {
    'k': [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
    'n': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)],
    'r': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    'b': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    'q': [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
}
def possible_moves(piece):
    posmoves.clear()
    p = board[piece[0]][piece[1]]
    color = p.color
    if p.name=="p":
        if p.color=="w":
            if board[piece[0]-1][piece[1]]=="":
                posmoves.append((piece[0]-1,piece[1]))
                if piece[0]==6 and board[piece[0]-2][piece[1]]=="":
                    posmoves.append((4,piece[1]))
            if piece[1]==0:
                if board[piece[0]-1][piece[1]+1]!="":
                    posmoves.append((piece[0]-1,piece[1]+1))
            elif piece[1]==7:
                if board[piece[0]-1][piece[1]-1]!="":
                    posmoves.append((piece[0]-1,piece[1]-1))
            else:
                if board[piece[0]-1][piece[1]+1]!="":
                    posmoves.append((piece[0]-1,piece[1]+1))
                if board[piece[0]-1][piece[1]-1]!="":
                    posmoves.append((piece[0]-1,piece[1]-1))
        elif p.color=="b":
            if board[piece[0]+1][piece[1]]=="":
                posmoves.append((piece[0]+1,piece[1]))
                if piece[0]==1 and board[piece[0]+2][piece[1]]=="":
                    posmoves.append((3,piece[1]))
            if piece[1]==0:
                if board[piece[0]+1][piece[1]+1]!="":
                    posmoves.append((piece[0]+1,piece[1]+1))
            elif piece[1]==7:
                if board[piece[0]+1][piece[1]-1]!="":
                    posmoves.append((piece[0]+1,piece[1]-11))
            else:
                if board[piece[0]+1][piece[1]+1]!="":
                    posmoves.append((piece[0]+1,piece[1]+1))
                if board[piece[0]+1][piece[1]-1]!="":
                    posmoves.append((piece[0]+1,piece[1]-1))
    else:
        for dr, dc in piece_moves[p.name]:
            r, c = piece[0] + dr, piece[1] + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "":
                    posmoves.append((r, c))
                elif board[r][c].color != color:
                    posmoves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

#PHASE 3: move pieces with mouse
#Get the row and column from mouse position
def get_row_col_from_mouse_pos(pos):
    x, y = pos
    row = y // 80
    col = x // 80
    return row, col

selected_piece = None
turn = 'w'
turnnum=1
#Move the piece to the selected position
def move_piece(row, col):
    global selected_piece
    global turn
    global turnnum
    piece = board[selected_piece[0]][selected_piece[1]]
    if selected_piece:
        if (row, col) in posmoves:
            board[selected_piece[0]][selected_piece[1]] = ""
            board[row][col] = piece
            selected_piece = None
            if turnnum%2==1:
                turn="b"
            else:
                turn="w"
            turnnum+=1
        else:
            print("Illegal move")
            selected_piece = None
        window.fill((255, 255, 255))
        drawboard()
        pygame.display.update()       

#Handle mouse clicks
def handle_mouse_click(row, col):
    global selected_piece
    piece = board[row][col]
    if piece != "" and piece.color==turn and selected_piece==None:
        selected_piece = (row, col)
        possible_moves(selected_piece)
    elif piece =="" and selected_piece==None:
        posmoves.clear()
    elif piece=="" and selected_piece!=None:
        move_piece(row, col)
    elif piece!="" and piece.color!=turn and selected_piece!=None:
        move_piece(row, col)
    else:
        print("Not your turn")

#Main game loop
gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse_pos(pos)
                handle_mouse_click(row, col)
