import keys
import random
import os
import time

class sprite:
   def __init__(self,hostile,drops,t,x,y):
      self.h=hostile
      self.drops=drops
      self.x=x
      self.y=y
      self.Type=t

   def move(self):
      global end,lives
      di=random.choice(['up','down','left','right'])
      if di == 'up':
         board[self.y][self.x]=' '
         self.y-=1
         board[self.y][self.x]=self.Type
      elif (di == 'down') and (not board[self.y+1][self.x]=='#'):
         board[self.y][self.x]=' '
         self.y+=1
         board[self.y][self.x]=self.Type
      elif (di == 'left') and (not board[self.y][self.x+1] == '#'):
         board[self.y][self.x]=' '
         self.x+=1
         board[self.y][self.x]=self.Type
      elif (di == 'right') and (not board[self.y][self.x-1] == '#'):
         board[self.y][self.x]=' '
         self.x-=1
         board[self.y][self.x]=self.Type
      if (self.h==True) and ( board[self.x][self.x]==pl.player):
         if lives==1:
            print('you died')
            end = True
         else:
            lives-=1
      else:
         upboard()
             

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
      global t,lives
      v=0
      for i in self.crafting:
         pl.inv[self.crafting[v]]-=1
         v+=1
      self.got = True
      pl.inv[self.name]=1
      if self.name == 'matock':
         t-=2
      elif self.name == 'sapling':
         screen.trees(1)
      elif self.name == 'armour':
         lives+=1

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
      self.inv = {'wood':0,'stone':0,'iron':0,'warg hide':0}
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
      if (di == 'a') and (spear.got):
         board[self.y][self.x]=' '
         self.x+=1
         board[self.y][self.x]=self.player
         if board[self.y][self.x]=='b':
            for mob in mobs:
               if board[mob.y][mob.x]==self.player:
                  for i in mob.drops:
                     self.inv[i]+=1
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
   print('\33[H')
   for i in board:
      for r in i:
         print(coulors[r]+r+coulors['end'],end='')
      print()

def mob_pos():
   while True:
      x=random.randint(0,39)
      y=random.randint(0,39)
      if board[y][x]==' ':
         return x,y

print('\33[2J')
print('\33[?25l')
t=2
end=False
lives=1

coulors={'#':'\33[100m','b':'\33[92m','s':'\33[94m','^':'\33[38;5;94m','end':'\33[0m',' ':'\33[0m'}

pickaxe=item(False,['wood','iron'],'matock')
sapling=item(False,['wood'],'sapling')
spear=item(False,['wood','wood','iron','iron'],'spear')
armour=item(False,['warg hide'],'armour')

items = {'matock':pickaxe,'sapling':sapling,'spear':spear,'armour':armour}
mobs=[]

screen=screen(40,40)
board = screen.new_board()
screen.terrain()
screen.trees(random.randint(1,5))
pl=players(0,19,'s')

while not end:
   a = keys.read()
   if a == 'e':
      pl.inventry()
   elif a == 'c':
      os.system('clear')
      n=input('>')
      items[n].craft()
   elif random.choice([True,False]) and len(mobs)<3:
      x,y=mob_pos()
      mob = sprite(True,['iron','warg hide'],'b',x,y)
      mobs+=[mob]
   else:
      for mob in mobs:
         mob.move()
      pl.move(a)
      pl.do_gravity()

