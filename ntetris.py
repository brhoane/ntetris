from random import randint
from Tkinter import *

pieces = [[[0,0,1,0],
           [0,0,1,0],
           [0,0,1,0],
           [0,0,1,0]],
          [[1,1],
           [1,1]],
          [[0,0,0],
           [0,1,0],
           [1,1,1]],
          [[0,0,1],
           [0,0,1],
           [0,1,1]],
          [[0,1,1],
           [0,0,1],
           [0,0,1]],
          [[0,0,1],
           [0,1,1],
           [0,1,0]],
          [[0,1,0],
           [0,1,1],
           [0,0,1]]]

pieces = [[[x==1 for x in y] for y in z] for z in pieces]

movetime = 10

class Player:
    def __init__(self, upper):
        self.upper = True
        self.piece = None
        self.timer = movetime
        

class Board:
    def __init__(self, h, w):
        if h%2 != 0: raise Exception("Board is not fair.")
        self.h = h
        self.w = w
        self.data = [[y > h/2 for x in xrange(w)] for y in xrange(h)]

def createPiece(player):
    piece = randint(0, len(pieces)-1)
    player.piece = [[x != player.upper for x in y] for y in piece]
    

def mainloop():
                 


board = Board(30,10)
master = Tk()
size = 18
bord = 1
total = size+bord*2
w = Canvas(master, width=board.w*total, height=board.h*total)
w.pack()
board.data[10][8] = True
for x in xrange(board.w):
    for y in xrange(board.h):
        b = board.data[y][x]
        a = ["black","white"]
        w.create_rectangle(x*total+1, y*total+1, x*total+1+size, y*total+1+size, fill=a[b], outline=a[not b])

mainloop()
