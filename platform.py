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

   def shoot(self,di):
      global lives
      arrows={'right':[],'up':[],'left':[],'down':[]}
      if di == 'right':
         arrow = block('wood',self.x-1,self.y)
         arrows['right']+=[arrow]
         for i in arrows['right']:
            i.x-=1
            pl.world[i.y][i.x]='*'
      if di == 'left':
         arrow = block('wood',self.x+1,self.y)
         arrows['left']+=[arrow]
         for i in arrows['left']:
            i.x+=1
            pl.world[i.y][i.x]='*'
      if di == 'up':
         arrow = block('wood',self.x,self.y-1)
         arrows['up']+=[arrow]
         for i in arrows['up']:
            i.y-=1
            pl.world[i.y][i.x]='*'
      if di == 'down':
         arrow = block('wood',self.x,self.y+1)
         arrows['down']+=[arrow]
         for i in arrows['down']:
            i.y+=1
            pl.world[i.y][i.x]='*'
      for key in arrows:
         for arrow in arrows[key]:
            if pl.world[arrow.y][arrow.x]=='s':
               if lives == 1:
                  print('you died')
                  end = True
               else:
                  lives-=1
      upboard(pl.world)

   def move(self):
      global end,lives
      di=random.choice(['up','down','left','right'])
      if di == 'up':
         pl.world[self.y][self.x]=' '
         self.y-=1
         pl.world[self.y][self.x]=self.Type
      elif di == 'down':
         pl.world[self.y][self.x]=' '
         self.y+=1
         pl.world[self.y][self.x]=self.Type
      elif di == 'left':
         pl.world[self.y][self.x]=' '
         self.x+=1
         pl.world[self.y][self.x]=self.Type
      elif di == 'right':
         pl.world[self.y][self.x]=' '
         self.x-=1
         pl.world[self.y][self.x]=self.Type
      if self.Type == 'D':
         self.shoot(random.choice(['up','down','left','right']))
      if (self.h==True) and (pl.world[self.y][self.x]=='s'):
         if lives==1:
            print('you died')
            end = True
         else:
            lives-=1
      else:
         upboard(pl.world)
             

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

   def explosion(self,blast):
       for block in screen.blocks:
          if (block.x in blast) and (block.y in blast):
             pl.inv[block.Type]+=1
             pl.world[block.y][block.x]=' '

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
      elif self.name == 'TNT':
         blast=[]
         for i in range(4):
            blast+=[pl.x+i]
            blast+=[pl.x-i]
            blast+=[pl.y+i]
            blast+=[pl.y-i]
         self.explosion(blast)

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

   def terrain(self,board):
      middle=screen.height//2
      x=0
      for r in range(self.width):
         for i in range(self.height-middle):
            board[middle+i][x]='#'
            stone=block(random.choice(['stone','stone','stone','iron']),x,middle+i)
            self.blocks+=[stone]
         middle += random.randint(0,1)
         middle -= random.randint(0,1)
         x+=1
      upboard(board)

   def trees(self,amount,board):
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
            board[y-2][x] = '$'
            wood=block('wood',x,y-2)
            screen.blocks+=[wood]
            board[y-2][x+1] = '$'
            wood=block('wood',x+1,y-2)
            screen.blocks+=[wood]
            board[y-2][x-1] = '$'
            wood=block('wood',x-1,y-2)
            screen.blocks+=[wood]
            board[y-3][x] = '$'
            wood=block('wood',x,y-3)
            screen.blocks+=[wood]
            amount-=1
      upboard(board)
         
class players:
   def __init__(self,x,y,p):
      self.x = x
      self.y = y
      self.inv = {'wood':0,'stone':0,'iron':0,'warg hide':0,'dimond':0,'gold':0,'gun powder':0}
      self.player = p
      self.world=worlds[0]

   def move(self,di):
      global time
      if di == keys.LEFT:
         if self.world[self.y][self.x-1] == ' ':
            self.world[self.y][self.x] = ' '
            self.x-=1
            self.world[self.y][self.x]=self.player
      if di == keys.RIGHT:
         if self.world[self.y][self.x+1] == ' ':
            self.world[self.y][self.x] = ' '
            self.x+=1
            self.world[self.y][self.x]=self.player
      if di == ' ':
         if self.world[self.y-1][self.x] == ' ':
            self.world[self.y][self.x] = ' '
            self.y-=2
            self.world[self.y][self.x]=self.player
      if di == keys.DOWN:
         time.sleep(t)
         self.world[self.y][self.x]=' '
         self.y+=1
         self.world[self.y][self.x] =self.player
         for block in screen.blocks:
            if (block.x == self.x) and (block.y == self.y): 
               self.inv[block.Type]+=1
               break
      if di == keys.UP:
         if (self.inv['stone']>0):
            self.world[self.y][self.x]='#'
            self.y-=1
            self.world[self.y][self.x]=self.player
            self.inv['stone']-=1
         else:
            print('you have run out of stone')
      if (di == 'a') and (spear.got):
         self.world[self.y][self.x]=' '
         self.x+=1
         self.world[self.y][self.x]=self.player
         if 'b' in self.world[self.y]:
            for mob in mobs:
               if self.y==mob.y:
                  for i in mob.drops:
                     self.inv[i]+=1
                  mob.Type = ' '
      upboard(self.world)

   def inventry(self):
      os.system('clear')
      for i in self.inv:
         print(i+': '+str(self.inv[i]))

   def do_gravity(self):
      if self.world[self.y+1][self.x] == ' ':
         self.world[self.y][self.x]=' '
         self.y+=1
         self.world[self.y][self.x]=self.player

def upboard(board):
   print('\33[H')
   for i in board:
      for r in i:
         print(coulors[r]+r+coulors['end'],end='')
      print()

def trade():
   os.system('clear')
   trades={'gold':'wood','warg hide':'gold','iron':'warg hide','dimond':'gold'}
   for key in trades:
      print(key+': '+trades[key])
   thing=input('>')
   pl.inv[trades[thing]]-=1
   pl.inv[thing]+=1

def setup():
   global worlds,mobs
   board = screen.new_board()
   screen.terrain(board)
   screen.trees(random.randint(1,5),board)
   worlds+=[board]
   upboard(board)
   x,y=mob_pos()
   dragon=sprite(True,['gun powder'],'D',x,y)
   mobs+=[dragon]

def mob_pos():
   while True:
      x=random.randint(0,(screen.width//2)-1)
      y=random.randint(0,(screen.height//2)-1)
      if pl.world[y][x]==' ':
         return x,y

print('\33[2J')
print('\33[?25l')

t=2
end=False
lives=1
z=0
worlds=[]

coulors={'#':'\33[100m','b':'\33[92m','s':'\33[94m','^':'\33[43m','end':'\33[0m',' ':'\33[0m','T':'\33[43m','$':'\33[42m','D':'\33[31m','*':'\33[103m'}

pickaxe=item(False,['wood','iron'],'matock')
sapling=item(False,['wood'],'sapling')
spear=item(True,['wood','wood','iron','iron'],'spear')
armour=item(False,['warg hide'],'armour')
crystal=item(False,['dimond','dimond','warg hide','gold','gold','dimond'],'crystal')
TNT=item(False,['gun powder'],'TNT')

items = {'matock':pickaxe,'sapling':sapling,'spear':spear,'armour':armour,'crystal':crystal,'TNT':TNT}
mobs=[]

screen=screen(40,40)
board = screen.new_board()
worlds+=[board]
pl=players(0,19,'s')
screen.terrain(pl.world)
screen.trees(random.randint(1,5),board)

while not end:
   a = keys.read()
   if a == 'e':
      pl.inventry()
   elif a == 'c':
      os.system('clear')
      n=input('>')
      items[n].craft()
   elif (a == 't') and (trader in mobs):
      trade()
   elif random.choice([True,False]) and len(mobs)<3:
      x,y=mob_pos()
      mob = sprite(True,['iron','warg hide'],'b',x,y)
      mobs+=[mob]
      x,y=mob_pos()
      trader = sprite(False,[],'T',x,y)
      mobs+=[trader]
   elif (a=='g') and (crystal.got == True):
      for row in pl.world:
         for s in row:
            if (s == 's') or (s == 'b') or (s == 'T'):
               s=' '
      setup()
      z+=1
      pl.world=worlds[z]
   elif a=='b':
      for row in pl.world:
         for s in row:
            if (s == 's') or (s == 'b') or (s == 'T'):
               s=' '
      z-=1
      pl.world=worlds[z]
   else:
      pl.move(a)
      for mob in mobs:
         mob.move()
      pl.do_gravity()

