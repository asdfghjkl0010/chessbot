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
def possible_moves(piece):
    global posmoves
    global enpassant
    global castle
    p = board[piece[0]][piece[1]]
    color=p.color
    #pawn rules NEED TO CODE ENPASSANT AND PROMOTION
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
    #king rules NEED TO CODE CASTLING
    elif p.name=="k":
        if piece[0]!=7 and piece[1]!=7 and (board[piece[0]+1][piece[1]+1]=="" or board[piece[0]+1][piece[1]+1].color!=color):
            posmoves.append((piece[0]+1,piece[1]+1))
        if piece[1]!=7 and (board[piece[0]][piece[1]+1]=="" or board[piece[0]][piece[1]+1].color!=color):
            posmoves.append((piece[0],piece[1]+1))
        if piece[0]!=0 and piece[1]!=7 and (board[piece[0]-1][piece[1]+1]=="" or board[piece[0]-1][piece[1]+1].color!=color):
            posmoves.append((piece[0]-1,piece[1]+1))
        if piece[0]!=0 and (board[piece[0]-1][piece[1]]=="" or board[piece[0]-1][piece[1]].color!=color):
            posmoves.append((piece[0]-1,piece[1]))
        if piece[0]!=7 and (board[piece[0]+1][piece[1]]=="" or board[piece[0]+1][piece[1]].color!=color):
            posmoves.append((piece[0]+1,piece[1]))
        if piece[0]!=0 and piece[1]!=0 and (board[piece[0]-1][piece[1]-1]=="" or board[piece[0]-1][piece[1]-1].color!=color):
            posmoves.append((piece[0]-1,piece[1]-1))
        if piece[1]!=0 and (board[piece[0]][piece[1]-1]=="" or board[piece[0]][piece[1]-1].color!=color):
            posmoves.append((piece[0],piece[1]-1))
        if piece[1]!=0 and piece[0]!=7 and (board[piece[0]+1][piece[1]-1]=="" or board[piece[0]+1][piece[1]-1].color!=color):
            posmoves.append((piece[0]+1,piece[1]-1))
    #knight rules
    elif p.name=="n":
        if piece[0]>1 and piece[1]!=0 and (board[piece[0]-2][piece[1]-1]=="" or board[piece[0]-2][piece[1]-1].color!=color):
            posmoves.append((piece[0]-2,piece[1]-1))   
        if piece[0]>1 and piece[1]!=7 and (board[piece[0]-2][piece[1]+1]=="" or board[piece[0]-2][piece[1]+1].color!=color):
            posmoves.append((piece[0]-2,piece[1]+1))
        if piece[0]!=0 and piece[1]<6 and (board[piece[0]-1][piece[1]+2]=="" or board[piece[0]-1][piece[1]+2].color!=color):
            posmoves.append((piece[0]-1,piece[1]+2))
        if piece[0]!=7 and piece[1]<6 and (board[piece[0]+1][piece[1]+2]=="" or board[piece[0]+1][piece[1]+2].color!=color):
            posmoves.append((piece[0]+1,piece[1]+2))
        if piece[0]<6 and piece[1]!=7 and (board[piece[0]+2][piece[1]+1]=="" or board[piece[0]+2][piece[1]+1].color!=color):
            posmoves.append((piece[0]+2,piece[1]+1))
        if piece[0]<6 and piece[1]!=0 and (board[piece[0]+2][piece[1]-1]=="" or board[piece[0]+2][piece[1]-1].color!=color):
            posmoves.append((piece[0]+2,piece[1]-1))
        if piece[0]!=7 and piece[1]>1 and (board[piece[0]+1][piece[1]-2]=="" or board[piece[0]+1][piece[1]-2].color!=color):           
            posmoves.append((piece[0]+1,piece[1]-2))
        if piece[0]!=0 and piece[1]>1 and (board[piece[0]-1][piece[1]-2]=="" or board[piece[0]-1][piece[1]-2].color!=color):
            posmoves.append((piece[0]-1,piece[1]-2))
    #rook rules
    elif p.name=="r":
        i=piece[0]+1
        while i<=7:
            if board[i][piece[1]]=="":
                posmoves.append((i,piece[1]))
            elif board[i][piece[1]]!="":
                if board[i][piece[1]].color==color:
                    break
                elif board[i][piece[1]].color!=color:
                    posmoves.append((i,piece[1]))
                    break
            i+=1
        i=piece[0]-1
        while i>=0:
            if board[i][piece[1]]=="":
                posmoves.append((i,piece[1]))
            elif board[i][piece[1]]!="":
                if board[i][piece[1]].color==color:
                    break
                elif board[i][piece[1]].color!=color:
                    posmoves.append((i,piece[1]))
                    break
            i-=1
        i=piece[1]+1
        while i<=7:
            if board[piece[0]][i]=="":
                posmoves.append((piece[0],i))
            elif board[piece[0]][i]!="":
                if board[piece[0]][i].color==color:
                    break
                elif board[piece[0]][i].color!=color:
                    posmoves.append((piece[0],i))
                    break
            i+=1
        i=piece[1]-1
        while i>=0:
            if board[piece[0]][i]=="":
                posmoves.append((piece[0],i))
            elif board[piece[0]][i]!="":
                if board[piece[0]][i].color==color:
                    break
                elif board[piece[0]][i].color!=color:
                    posmoves.append((piece[0],i))
                    break
            i-=1
    #bishop rules
    elif p.name=="b":
        r=piece[0]+1
        c=piece[1]+1
        while r<=7 and c<=7:
            if board[r][c]=="":
                posmoves.append((r,c))
            elif board[r][c]!="":
                if board[r][c].color==color:
                    break
                elif board[r][c].color!=color:
                    posmoves.append((r,c))
                    break
            r+=1
            c+=1
        r=piece[0]+1
        c=piece[1]-1
        while r<=7 and c>=0:
            if board[r][c]=="":
                posmoves.append((r,c))
            elif board[r][c]!="":
                if board[r][c].color==color:
                    break
                elif board[r][c].color!=color:
                    posmoves.append((r,c))
                    break
            r+=1
            c-=1
        r=piece[0]-1
        c=piece[1]+1
        while r>=0 and c<=7:
            if board[r][c]=="":
                posmoves.append((r,c))
            elif board[r][c]!="":
                if board[r][c].color==color:
                    break
                elif board[r][c].color!=color:
                    posmoves.append((r,c))
                    break
            r-=1
            c+=1
        r=piece[0]-1
        c=piece[1]-1
        while r>=0 and c>=0:
            if board[r][c]=="":
                posmoves.append((r,c))
            elif board[r][c]!="":
                if board[r][c].color==color:
                    break
                elif board[r][c].color!=color:
                    posmoves.append((r,c))
                    break
            r-=1
            c-=1
    #queen rules    
    elif p.name=="q":
        i=piece[0]+1
        while i<=7:
            if board[i][piece[1]]=="":
                posmoves.append((i,piece[1]))
            elif board[i][piece[1]]!="":
                if board[i][piece[1]].color==color:
                    break
                elif board[i][piece[1]].color!=color:
                    posmoves.append((i,piece[1]))
                    break
            i+=1
        i=piece[0]-1
        while i>=0:
            if board[i][piece[1]]=="":
                posmoves.append((i,piece[1]))
            elif board[i][piece[1]]!="":
                if board[i][piece[1]].color==color:
                    break
                elif board[i][piece[1]].color!=color:
                    posmoves.append((i,piece[1]))
                    break
            i-=1
        i=piece[1]+1
        while i<=7:
            if board[piece[0]][i]=="":
                posmoves.append((piece[0],i))
            elif board[piece[0]][i]!="":
                if board[piece[0]][i].color==color:
                    break
                elif board[piece[0]][i].color!=color:
                    posmoves.append((piece[0],i))
                    break
            i+=1
        i=piece[1]-1
        while i>=0:
            if board[piece[0]][i]=="":
                posmoves.append((piece[0],i))
            elif board[piece[0]][i]!="":
                if board[piece[0]][i].color==color:
                    break
                elif board[piece[0]][i].color!=color:
                    posmoves.append((piece[0],i))
                    break
            i-=1
        r=piece[0]+1
        c=piece[1]+1
        while r<=7 and c<=7:
            if board[r][c]=="":
                posmoves.append((r,c))
            elif board[r][c]!="":
                if board[r][c].color==color:
                    break
                elif board[r][c].color!=color:
                    posmoves.append((r,c))
                    break
            r+=1
            c+=1
        r=piece[0]+1
        c=piece[1]-1
        while r<=7 and c>=0:
            if board[r][c]=="":
                posmoves.append((r,c))
            elif board[r][c]!="":
                if board[r][c].color==color:
                    break
                elif board[r][c].color!=color:
                    posmoves.append((r,c))
                    break
            r+=1
            c-=1
        r=piece[0]-1
        c=piece[1]+1
        while r>=0 and c<=7:
            if board[r][c]=="":
                posmoves.append((r,c))
            elif board[r][c]!="":
                if board[r][c].color==color:
                    break
                elif board[r][c].color!=color:
                    posmoves.append((r,c))
                    break
            r-=1
            c+=1
        r=piece[0]-1
        c=piece[1]-1
        while r>=0 and c>=0:
            if board[r][c]=="":
                posmoves.append((r,c))
            elif board[r][c]!="":
                if board[r][c].color==color:
                    break
                elif board[r][c].color!=color:
                    posmoves.append((r,c))
                    break
            r-=1
            c-=1







#PHASE 3: move pieces with mouse
#Get the row and column from mouse position
def get_row_col_from_mouse_pos(pos):
    x, y = pos
    row = y // 80
    col = x // 80
    return row, col

selected_piece = None

#Move the piece to the selected position
def move_piece(row, col):
    global selected_piece
    global turn
    piece = board[selected_piece[0]][selected_piece[1]]
    if selected_piece:
        if (row,col) in posmoves:
            board[selected_piece[0]][selected_piece[1]] = ""
            board[row][col] = piece
            selected_piece = None
        else:
            print("Illegal move")
            selected_piece = None
    window.fill((255, 255, 255))
    posmoves.clear()
    drawboard()
    pygame.display.update()        

#Handle mouse clicks
def handle_mouse_click(row, col):
    global selected_piece
    piece = board[row][col]
    if piece != "" and selected_piece==None:
        selected_piece = (row, col)
        possible_moves(selected_piece)
    elif piece =="" and selected_piece==None:
        posmoves.clear()
    else:
        move_piece(row, col)

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
