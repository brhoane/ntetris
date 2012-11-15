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
          [[0,1,0],
           [0,1,1],
           [0,1,0]],
          [[0,1,1],
           [0,1,0],
           [0,1,0]],
          [[0,1,0],
           [0,1,0],
           [0,1,1]],
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

  def lock(self, board):
    if self.piece == None: return
    for i in xrange(self.size()):
      for j in xrange(self.size()):
        if self.piece[j][i]:
          board.data[j + self.y][i + self.x] = self.white
    toDelete = []
    for j in xrange(self.size()):
      for i in xrange(board.w):
        if board.data[j+self.y][i] != self.white: break
      else: toDelete += [j]
    self.piece = None
    for d in toDelete:
      board.deleteRow(self.y+d)

  def fall(self, board):
    if self.piece == None: return
    if self.white: self.y += 1
    else: self.y -= 1

  def shift(self, board, left):
    def callback(event):
      if self.piece == None: return
      self.x -= [-1,1][left]
      if self.isIllegal(board):
        self.x += [-1,1][left]
      else:
        pass
        #if self.isTouching(board): self.timer = movetime
    return callback

  def hardDrop(self, board):
    def callback(event):
      if self.piece == None: return
      while not self.isTouching(board):
        self.fall(board)
    return callback

  def softDrop(self, board):
    def callback(event):
      if self.piece == None: return
      if not self.isTouching(board):
        self.fall(board)
      else:
        self.lock(board)
      self.timer = movetime
    return callback

  def rotateLeft(self, board):
    def callback(event):
      if self.piece == None: return
      oldpiece = self.piece
      self.piece = [[self.piece[self.size()-i-1][j] for i in xrange(self.size())] for j in xrange(self.size())]
      if self.isIllegal(board):
        self.piece = oldpiece
    return callback

  def rotateRight(self, board):
    if self.piece == None: return
    if self.isTouching(board): self.timer = movetime

  def isIllegal(self, board):
    for i in xrange(self.size()):
      for j in xrange(self.size()):
        if self.piece[j][i]:
          bx = i + self.x
          by = j + self.y
          if bx < 0 or by < 0 or bx >= board.w or by >= board.h: return True
          if board.data[by][bx] == self.white: return True
    return False

  def isTouching(self, board):
    for i in xrange(self.size()):
      for j in xrange(self.size()):
        if self.piece[j][i]:
          bx = i + self.x
          by = j + self.y
          if self.white: by += 1
          else: by -= 1
          if by == board.h: return True
          if board.data[by][bx] == self.white: return True
    return False

  def update(self, board):
    if self.isIllegal(board): return False
    if not self.time():
      if self.piece == None:
        self.createPiece(board)
      elif not self.isTouching(board):
        self.fall(board)
      else:
        self.lock(board)
        pass
    return True

  def createPiece(self, board):
    self.piece = [[x==1 for x in y] for y in pieces[randint(0, len(pieces)-1)]]
    self.x = (board.w - len(self.piece))/2
    self.y = [0,board.h-len(self.piece)][not self.white]

class Board(object):
  def __init__(self, h, w):
    if h%2 != 0: raise Exception("Board is not fair.")
    self.h = h
    self.w = w
    self.data = [[y >= h/2 for x in xrange(w)] for y in xrange(h)]
    self.players = [Player(False), Player(True)]

  def deleteRow(self, y):
    color = self.data[y][0]
    d = [1,-1][color]
    s = [self.h-1,0][color]
    for i in xrange(y, s, d):
      self.data[i] = self.data[i+d]
    self.data[s-d] = [not color]*self.w
    self.players[not color].y += d
 #   print self.players[not color].piece

  def update(self):
    for p in self.players:
      if not p.update(self):
        print colors[not p.white]+" won!"
        return False
    return True

  def paint(self, canvas):
    for x in xrange(self.w):
      for y in xrange(self.h):
        b = self.data[y][x]
        for p in self.players:
          if x >= p.x and x < p.x+p.size() and y >= p.y and y < p.y+p.size() and p.piece[y-p.y][x-p.x]:
            b = not b
        canvas.itemconfig(str(x)+'x'+str(y)+'y', fill=colors[b], outline=colors[not b])

def testing(board):
  def callback(event):
    board.deleteRow(10)
  return callback

def main():
  board = Board(40,10)
  master = Tk()
  size = 18
  bord = 1
  total = size+bord*2
  canvas = Canvas(master, width=board.w*total, height=board.h*total)
  master.bind("<Left>", board.players[0].shift(board, True))
  master.bind("<Right>", board.players[0].shift(board, False))
  master.bind("<Up>", board.players[0].softDrop(board))
  master.bind("<Down>", board.players[0].rotateLeft(board))
  master.bind("<space>", board.players[1].hardDrop(board))
  master.bind("a", board.players[1].shift(board, True))
  master.bind("d", board.players[1].shift(board, False))
  master.bind("w", board.players[1].rotateLeft(board))
  master.bind("s", board.players[1].softDrop(board))
  master.bind("<KP_0>", board.players[0].hardDrop(board))
  canvas.pack()
  for x in xrange(board.w):
    for y in xrange(board.h):
      b = board.data[y][x]
      canvas.create_rectangle(x*total+1, y*total+1, x*total+1+size, y*total+1+size, fill=colors[b], outline=colors[not b], tag=str(x)+'x'+str(y)+'y')

  while board.update():
    canvas.after(20)
    canvas.update()
    board.paint(canvas)
  master.mainloop()

try:
  if __name__ == "__main__": main()
except TclError, e:
  pass
