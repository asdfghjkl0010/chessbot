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
    x=0
    y=0
    for i in range(8):
        for j in range(8):
            if i%2!=j%2:
                pygame.draw.rect(window,(0, 0,0),[x, y, 80, 80], 0)
            x+=80
        x=0
        y+=80

def gamepos():
    x=0
    y=0
    for i in range(8):
        for j in range(8):
            if board[i][j]!="":
                window.blit(board[i][j].image,(x+20,y+20))
            x+=80
        x=0
        y+=80
    
#updates to display the board and pieces
drawboard()
gamepos()
pygame.display.update()

#PHASE 2: move pieces with mouse
#selected piece class

# Get the row and column from mouse position
def get_row_col_from_mouse_pos(pos):
    x, y = pos
    row = y // 80
    col = x // 80
    return row, col

selected_piece = None

# Move the piece to the selected position
def move_piece(row, col):
    global selected_piece
    if selected_piece:
        piece = board[selected_piece[0]][selected_piece[1]]
        board[selected_piece[0]][selected_piece[1]] = ""
        board[row][col] = piece
        selected_piece = None
    window.fill((255, 255, 255))
    drawboard()
    gamepos()
    pygame.display.update()
        

# Handle mouse clicks
def handle_mouse_click(row, col):
    global selected_piece
    piece = board[row][col]
    if piece != "":
        selected_piece = (row, col)
    else:
        move_piece(row, col)



# Main game loop
gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse_pos(pos)
                handle_mouse_click(row, col)
