from random import randint
from Tkinter import *
from _tkinter import TclError


colors = ["black","white"]

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

class Player(object):
  def __init__(self, white):
    self.white = white
    self.piece = None
    self.x = 0
    self.y = 0
    self.timer = movetime

  def size(self):
    if self.piece == None: return 0
    return len(self.piece)

  def time(self):
    self.timer -= 1
    ret = self.timer
    if self.timer == 0: self.timer = movetime
    return ret

  def leftShift(self, board):
    pass

  def rightShift(self, board):
    pass

  def hardDrop(self, board):
    pass

  def softDrop(self, board):
    pass

  def rotate(self, board):
    pass

  def isIllegal(self, board):
    for i in xrange(self.size()):
      for j in xrange(self.size()):
        if self.piece[j][i] == self.white:
          bx = i + self.x
          by = j + self.y
          if bx < 0 or by < 0 or bx >= board.w or by >= board.h: return False
          if board.data[by][bx] == self.white: return False

  def update(self, board):
    if not self.time():
      if self.piece == None:
        self.createPiece(board)

  def createPiece(self, board):
    self.piece = [[x==1 for x in y] for y in pieces[randint(0, len(pieces)-1)]]
    self.x = (board.w - len(self.piece))/2
    self.y = [0,board.h-len(self.piece)][not self.white]

class Board(object):
  def __init__(self, h, w):
    if h%2 != 0: raise Exception("Board is not fair.")
    self.h = h
    self.w = w
    self.data = [[y > h/2 for x in xrange(w)] for y in xrange(h)]
    self.players = [Player(True), Player(False)]

  def update(self):
    for p in self.players:
      p.update(self)

  def paint(self, canvas):
    for x in xrange(self.w):
      for y in xrange(self.h):
        b = self.data[y][x]
        for p in self.players:
          if x >= p.x and x < p.x+p.size() and y >= p.y and y < p.y+p.size() and p.piece[y-p.y][x-p.x]:
           # print "hi"
            b = not b
        canvas.itemconfig(str(x)+'x'+str(y)+'y', fill=colors[b], outline=colors[not b])


def main():
  board = Board(30,10)
  master = Tk()
  size = 18
  bord = 1
  total = size+bord*2
  canvas = Canvas(master, width=board.w*total, height=board.h*total)
  canvas.pack()
  for x in xrange(board.w):
    for y in xrange(board.h):
      b = board.data[y][x]
      canvas.create_rectangle(x*total+1, y*total+1, x*total+1+size, y*total+1+size, fill=colors[b], outline=colors[not b], tag=str(x)+'x'+str(y)+'y')

  while True:
    canvas.after(20)
    canvas.update()
    board.paint(canvas)

    board.update()
  master.mainloop()

try:
  if __name__ == "__main__": main()
except TclError, e:
  pass
