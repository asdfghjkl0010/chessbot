#pygame setup
import pygame
from pygame.locals import *
pygame.init()
window = pygame.display.set_mode((640, 640))
window.fill((255, 255, 255))

#chess board
x=0
y=0
for i in range(8):
    for j in range(8):
        if i%2!=j%2:
            pygame.draw.rect(window,(0, 0,0),[x, y, 80, 80], 0)
        x+=80
    x=0
    y+=80

#create chess pieces
class Piece:
    def __init__(self,color,name,image):
        self.color=color
        self.name=name
        self.image=pygame.image.load(image)

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

#setup board
def setup():
    x=0
    y=0
    for i in range(8):
        for j in range(8):
            if i%2!=j%2:
                pygame.draw.rect(window,(0, 0,0),[x, y, 80, 80], 0)
            x+=80
        x=0
        y+=80
    x=0
    y=0
    for i in range(8):
        for j in range(8):
            if i==0 or i==1 or i==6 or i==7:
                window.blit(board[i][j].image,(x+20,y+20))
            x+=80
        x=0
        y+=80

#call functions
setup()

#update display
pygame.display.update()


