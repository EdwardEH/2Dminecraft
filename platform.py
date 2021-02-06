import keys
import random
import os
import time

class block:
   def __init__(self,Type,x,y):
      self.Type=Type
      self.x=x
      self.y=y

class item:
   def __init__(self,got,crafting,n):
      self.got=got
      self.crafting=crafting
      self.name=n

   def craft(self):
      global t
      os.system('clear')
      name = input('>')
      if name == self.name:
         v=0
         for i in self.crafting:
            pl.inv[self.crafting[v]]-=1
            v+=1
         self.got = True
         pl.inv[self.name]=1
         if self.name == 'pickaxe':
            t-=2

class screen:
   def __init__(self,width,height):
      self.blocks=[]
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
            stone=block(random.choice(['stone','stone','stone','iron']),x,middle+i)
            self.blocks+=[stone]
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
            board[y][x] = '^'
            wood=block('wood',x,y)
            screen.blocks+=[wood]
            board[y-1][x] = '^'
            wood=block('wood',x,y-1)
            screen.blocks+=[wood]
            board[y-2][x] = '^'
            wood=block('wood',x,y-2)
            screen.blocks+=[wood]
            board[y-2][x+1] = '^'
            wood=block('wood',x+1,y-2)
            screen.blocks+=[wood]
            board[y-2][x-1] = '^'
            wood=block('wood',x-1,y-2)
            screen.blocks+=[wood]
            board[y-3][x] = '^'
            wood=block('wood',x,y-3)
            screen.blocks+=[wood]
            amount-=1
      upboard()
         
class players:
   def __init__(self,x,y,p):
      self.x = x
      self.y = y
      self.inv = {'wood':0,'stone':0,'iron':0}
      self.player = p

   def move(self,di):
      global time
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
         time.sleep(t)
         board[self.y][self.x]=' '
         self.y+=1
         board[self.y][self.x] =self.player
         for block in screen.blocks:
            if (block.x == self.x) and (block.y == self.y): 
               self.inv[block.Type]+=1
               break
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
      if board[self.y+1][self.x] == ' ':
         board[self.y][self.x]=' '
         self.y+=1
         board[self.y][self.x]=self.player

def upboard():
   os.system('clear')
   for i in board:
      for r in i:
         print(r,end='')
      print()

t=2

pickaxe=item(False,['wood','iron'],'pickaxe')

items = ['wood','stone','iron']

screen=screen(40,40)
board = screen.new_board()
screen.terrain()
screen.trees(random.randint(1,5))
pl=players(0,19,'s')
while True:
   a = keys.read()
   if a == 'e':
      pl.inventry()
   elif a == 'c':
      pickaxe.craft()
   else:
      pl.move(a)
      pl.do_gravity()

