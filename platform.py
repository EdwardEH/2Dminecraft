import keys
import random
import os

class screen:
   def __init__(self,width,height):
      self.width= width
      self.height= height

   def new_board(self):
      board = []
      for i in range(self.width):
         line = []
         for r in range(self.height):
            line +=[' ']
         board+=[line]
      return board

   def terrain(self):
      middle = self.height//2
      x=0
      for r in range(self.width):
         for i in range(self.height-middle):
            board[middle+i][x]='#'
         middle += random.randint(0,1)
         middle -= random.randint(0,1)
         x+=1
      upboard()

   def trees(self,amount):
      end=True
      while end:
         if amount == 0:
            end = False
         x = random.randint(1,self.width-1)
         y = random.randint(0,self.height-1)
         if (board[y][x] == ' ') and (board[y][x-1] == '#'):
            board[y][x] = '#'
            board[y-1][x] = '#'
            board[y-2][x] = '#'
            board[y-2][x-1] = '#'
            board[y-2][x+1] = '#'
            board[y-3][x] = '#'
            amount-=1
      upboard()
      print(x,y)
         
class players:
   def __init__(self,x,y,p):
      global wood,stone,iron
      self.x = x
      self.y = y
      self.inv = {'wood':wood,'stone':stone,'iron':iron}
      self.player = p

   def move(self,di):
      if di == keys.LEFT:
         if board[self.y][self.x-1] == ' ':
            board[self.y][self.x] = ' '
            self.x-=1
            board[self.y][self.x]=self.player
      if di == keys.RIGHT:
         if board[self.y][self.x+1] == ' ':
            board[self.y][self.x] = ' '
            self.x+=1
            board[self.y][self.x]=self.player
      if di == ' ':
         if board[self.y-1][self.x] == ' ':
            board[self.y][self.x] = ' '
            self.y-=2
            board[self.y][self.x]=self.player
      if di == keys.DOWN:
         board[self.y][self.x]=' '
         self.y+=1
         board[self.y][self.x] =self.player
         self.inv[random.choice(['stone','stone','stone','iron'])]+=1
      if di == keys.UP:
         if (self.inv['stone']>0):
            board[self.y][self.x]='#'
            self.y-=1
            board[self.y][self.x]=self.player
            self.inv['stone']-=1
         else:
            print('you have run out of stone')
      upboard()

   def inventry(self):
      os.system('clear')
      for i in self.inv:
         print(i+': '+str(self.inv[i]))

   def do_gravity(self):
      if board[self.y+1][self.x] == '#':
         return
      else:
         board[self.y][self.x]=' '
         self.y+=1
         board[self.y][self.x]=self.player

def upboard():
   os.system('clear')
   for i in board:
      for r in i:
         print(r,end='')
      print()

iron=0
stone=0
wood=0

items = ['wood','stone','iron']

screen=screen(40,40)
board = screen.new_board()
screen.terrain()
screen.trees(random.randint(0,5))
pl=players(0,19,'s')
while True:
   a = keys.read()
   if a == 'e':
      pl.inventry()
   else:
      pl.move(a)
      pl.do_gravity()

