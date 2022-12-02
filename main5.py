# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 12:27:42 2022

@author: younn
"""

import sys, os
import pygame
import sys
import time
from modules.undo import Undo
myUndo = Undo()
a = []
b = []
c = []

# Verifies last direction of undo
d = []
# Verifies last direction of redo
e = []

# initializing the constructor
pygame.init()
clock = pygame.time.Clock()
mouse = pygame.mouse.get_pos()

# screen resolution
res = (390,450)
screen = pygame.display.set_mode(res)
  
# colors & fonts
color = (255,255,255)
color_light = (255,255,255)
color_gray = (170,170,170)
color_dark = (100,100,100)
color_red = (255,0,0)
color_red_hovered = (200,0,0)
color_green = (0,255,0)
color_green_hovered = (0,200,0)
color_blue = (200,200,255)
color_blue_hovered = (100,100,200)
color_yellow = (255,255,0)
color_yellow_hovered = (200,200,0)
font = pygame.font.Font(pygame.font.match_font("calibri"),26)
  
# width and height of the screen
width = screen.get_width()
height = screen.get_height()

#these are the images that get shown as items, different color circle for each item
items = [pygame.Surface((50,50),pygame.SRCALPHA) for x in range(4)]
pygame.draw.circle(items[0],color_red,(25,25),25)
pygame.draw.circle(items[1],color_green,(25,25),25)
pygame.draw.circle(items[2],color_blue,(25,25),25)
pygame.draw.circle(items[3],color_yellow,(25,25),25)

squares = [pygame.Surface((50,50),pygame.SRCALPHA) for x in range(4)]
pygame.draw.rect(squares[0],color_red, pygame.Rect(25,25, 25, 25))
pygame.draw.rect(squares[1],color_green,pygame.Rect(25,25, 25, 25))
pygame.draw.rect(squares[2],color_blue,pygame.Rect(25,25, 25, 25))
pygame.draw.rect(squares[3],color_yellow,pygame.Rect(25,25, 25, 25))

# Dropdown class
class DropDown():
  def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
      self.color_menu = color_menu
      self.color_option = color_option
      self.rect = pygame.Rect(x, y, w, h)
      self.font = font
      self.main = main
      self.options = options
      self.draw_menu = False
      self.menu_active = False
      self.active_option = -1

  def draw(self, surf):
      pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
      msg = self.font.render(self.main, 1, (0, 0, 0))
      surf.blit(msg, msg.get_rect(center = self.rect.center))

      if self.draw_menu:
          for i, text in enumerate(self.options):
              rect = self.rect.copy()
              rect.y += (i+1) * self.rect.height
              pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
              msg = self.font.render(text, 1, (0, 0, 0))
              surf.blit(msg, msg.get_rect(center = rect.center))

  def update(self, event_list):
      mpos = pygame.mouse.get_pos()
      self.menu_active = self.rect.collidepoint(mpos)
      
      self.active_option = -1
      for i in range(len(self.options)):
          rect = self.rect.copy()
          rect.y += (i+1) * self.rect.height
          if rect.collidepoint(mpos):
              self.active_option = i
              break

      if not self.menu_active and self.active_option == -1:
          self.draw_menu = False

      for event in event_list:
          if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
              if self.menu_active:
                  self.draw_menu = not self.draw_menu
              elif self.draw_menu and self.active_option >= 0:
                  self.draw_menu = False
                  return self.active_option
      return -1

# Block class
class Block:
  def __init__(self, x_pos, y_pos):
    self.x = x_pos
    self.y = y_pos
    self.surface = squares[0]

# Item class
class Item:
    def __init__(self,id):
        self.id = id
        self.surface = items[id]
    
    def resize(self,size):
        return pygame.transform.scale(self.surface,(size,size))

# Square class
class Square:
  def __init__(self,id):
      self.id = id
      self.surface = squares[id]
  
  def resize(self,size):
      return pygame.transform.scale(self.surface,(size,size))

# Inventory class holding items
class Inventory:
  def __init__(self):
      self.rows = 9
      self.col = 9
      self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
      self.box_size = 40
      self.foreignIdIncrement = 0
      self.x = 0
      self.y = 0
      self.border = 3
      self.block = Block(self.x, self.y)
      self.body = [Block(40, 80), Block(80, 80), Block(120, 80), Block(40, 120), Block(80, 120), Block(120, 120), Block(40, 160), Block(80, 160), Block(120, 160)]
  
  #draw everything
  def draw(self):
      #print(self.rows,
      # self.col,
      # self.items,
      # self.box_size,
      # self.x,
      # self.y,
      # self.border)
      
      #draw background
      pygame.draw.rect(screen,(100,100,100),
        (self.x,self.y,(self.box_size + self.border)*self.col + self.border,(self.box_size + self.border)*self.rows + self.border))
      for x in range(self.col):
          for y in range(self.rows):
              rect = (self.x + (self.box_size + self.border)*x + self.border,self.x + (self.box_size + self.border)*y + self.border,self.box_size,self.box_size )
              pygame.draw.rect(screen,(180,180,180),rect)
              if self.items[x][y]:
                  screen.blit(self.items[x][y][0].resize(self.box_size),rect)
                  obj = font.render(str(self.items[x][y][1]),True,(0,0,0))
                  screen.blit(obj,(rect[0] + self.box_size//2, rect[1] + self.box_size//2))
      for block in self.body:
        block_rect = pygame.Rect( block.x+6, block.y+9, self.box_size+6, self.box_size+6)
        draw_rect_alpha(screen, (255, 0, 0, 60), block_rect)

  #get the square that the mouse is over
  def Get_pos(self):
      mouse = pygame.mouse.get_pos()
      
      x = mouse[0] - self.x
      y = mouse[1] - self.y
      x = x//(self.box_size + self.border)
      y = y//(self.box_size + self.border)
      return (x,y)

  #delete selectionned item last position
  def Del(self,Item,xy):
    print("test delete")
    items[xy[0]][xy[1]] = None

  #add an item/s
  def Add(self,Item,xy):
      x, y = xy
      if self.items[x][y] != None:
            self.items[x][y][1] = self.foreignIdIncrement
            temp = self.items[x][y]
            self.items[x][y] = Item
            return temp
      else:
          self.items[x][y] = Item
          print(self.items[x])
          self.items[x][y][1] = self.foreignIdIncrement
  
  #checks whether there are drops around itself
  def Check_adjacent(self,x,y):
    elementCoordinates = []
    selectedMoves = []
    if x < self.rows-1 and self.items[x+1][y] != None:
      elementCoordinates.append([x+1,y])
    if x < self.rows-1 and self.items[x-1][y] != None:
      elementCoordinates.append([x-1,y])
    if y < self.col-1 and self.items[x][y+1] != None:
      elementCoordinates.append([x,y+1])
    if y < self.col-1 and self.items[x][y-1] != None:
      elementCoordinates.append([x,y-1])
    if len(elementCoordinates) != 0:
      self.foreignIdIncrement += 1
      for elementCoord in elementCoordinates:
        self.items[elementCoord[0]][elementCoord[1]][1] = self.foreignIdIncrement
        selectedMoves.append(self.items[elementCoord[0]][elementCoord[1]])
      if (self.items[x][y] != None):
        self.items[x][y][1] = self.foreignIdIncrement
      #self.Check_adjacent(x,y)
    return (selectedMoves, elementCoordinates)
  
  #check whether the mouse in in the grid
  def In_grid(self,x,y):
    #print(self.col, self.rows, x, y)
    if 0 > x or x > self.col-1:
      return False
    if 0 > y or y > self.rows-1:
      return False
    return True


def move_direction(dirNum, posInv):
  uColor = inventory.items[posInv[0]][posInv[1]]
  inventory.items[posInv[0]][posInv[1]] = None
  my_list = list(posInv)
  # Left
  if dirNum == 4:
    my_list[0] +=1
  # Right
  elif dirNum == 3:
    my_list[0] -=1
  # Down
  elif dirNum == 2:
    my_list[1] +=1
  # Up
  elif dirNum == 1:
    my_list[1] -=1
  my_tuple = tuple(my_list)
  posInv = my_tuple
  selectedMoves = inventory.Check_adjacent(posInv[0], posInv[1])
  
  #if (len(selectedMoves[0]) > 0):
    #for i in range(len(selectedMoves[0])-1):
      #print(selectedMoves[0][0])
      #inventory.Add(selectedMoves[0][0],tuple(selectedMoves[1][i]))
  #else:

  # Undo Redo
  myUndo(a.append, [posInv], [], "last position", a.pop)
  b.append(uColor)
  c.append(selectedMove)
  d.append( dirNum )

  inventory.Add(selectedMove,posInv)
  print(selectedMoves)
  #selected= None
  return posInv, selectedMoves

def draw_rect_alpha(surface, color, rect):
  shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
  pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
  surface.blit(shape_surf, rect)

# returns if in dimension
def isInDimension(screenX, screenY, boxWidth, boxHeight, mouseX, mouseY):
  if (screenX <= mouseX <= screenX + boxWidth and screenY <= mouseY <= screenY+boxHeight):
    return True
  else:
    return False

# Specific-Use Variables
inventory = Inventory()
selectedMoves = ([],[])
selectedMove = None
selected = None
optique = False
running = True

# Loop of the app
while running:
    # fills the screen with a color
    screen.fill((255,255,255))
    inventory.draw()

    #if holding something, draw it next to mouse
    if selected:
        mousex, mousey = pygame.mouse.get_pos()
        screen.blit(selected[0].resize(30),(mousex,mousey))
        obj = font.render(str(selected[1]),True,(0,0,0))
        screen.blit(obj,(mousex + 15, mousey + 15))  
    if selectedMove:
      if inventory.In_grid(posInv[0],posInv[1]):
          mousex, mousey = pygame.mouse.get_pos()
          pygame.draw.rect(screen, color_green, pygame.Rect((posInv[0]*40)+(posInv[0]*3)+2, (posInv[1]*40)+(posInv[1]*3)+2, 42, 42), 2)
    if selectedMoves and selectedMoves != ([], []) :
      if inventory.In_grid(posInv[0],posInv[1]):
        for selectedElement in selectedMoves[1]:
            mousex, mousey = pygame.mouse.get_pos()
            pygame.draw.rect(screen, color_green, pygame.Rect((selectedElement[0]*40)+(selectedElement[0]*3)+2, (selectedElement[1]*40)+(selectedElement[1]*3)+2, 42, 42), 2)

    for ev in pygame.event.get():
      if ev.type == pygame.QUIT:
          pygame.quit()

      ## MAIN AREA
      if ev.type == pygame.MOUSEBUTTONUP:
        posInv = inventory.Get_pos()
        # If Buttondown is Mouse1
        if ev.button == 1:
          # Check if clicked Button1
          if isInDimension(button1['screenX'], button1['screenY'], button1['boxWidth'], button1['boxHeight'], mouse[0], mouse[1]):
            selected = [Item(0),0]
          # Check if clicked Button2
          if isInDimension(button2['screenX'], button2['screenY'], button2['boxWidth'], button2['boxHeight'], mouse[0], mouse[1]):
            selected = [Item(1),0]
          # Check if clicked Button3
          if isInDimension(button3['screenX'], button3['screenY'], button3['boxWidth'], button3['boxHeight'], mouse[0], mouse[1]):
            selected = [Item(2),0]
          # Check if clicked Button4
          if isInDimension(button4['screenX'], button4['screenY'], button4['boxWidth'], button4['boxHeight'], mouse[0], mouse[1]):
            selected = [Item(3),0]

          # Check if clicked Button6
          if isInDimension(button6['screenX'], button6['screenY'], button6['boxWidth'], button6['boxHeight'], mouse[0], mouse[1]):
            if myUndo.undoCount()>=2 :
                myUndo.undo()
                undoC = (myUndo.undoCount())-1
                a1 = a[undoC-1][0]
                a2 = a[undoC-1][1]
                posInvUndo = (a1,a2)
                my_list = list(posInvUndo)
						   
                if inventory.In_grid(my_list[0],my_list[1]):
                  if len(b)>=2 and len(c)>=0 and len(d)>=0:
                    # selectedMove2 = inventory.items[my_list[0]][my_list[1]]
                    selectedMove2 = b[0]
                    selectedMove = inventory.Add(selectedMove2,a[(myUndo.undoCount())-1])
                    #delete last item depending on direction choosed
                    #Up
                    if(d[-1]==1):
                        inventory.items[a[(myUndo.undoCount())-1][0]][(a[(myUndo.undoCount())-1][1])-1] = None
                        e.append(1)
                        del d[-1]
                    #Down
                    elif (d[-1]==2):
                        inventory.items[a[(myUndo.undoCount())-1][0]][(a[(myUndo.undoCount())-1][1])+1] = None
                        e.append(2)
                        del d[-1]
                    #Left
                    elif (d[-1]==3):
                        inventory.items[(a[(myUndo.undoCount())-1][0])-1][a[(myUndo.undoCount())-1][1]] = None
                        e.append(3)
                        del d[-1]
                    #Right
                    elif (d[-1]==4):
                        inventory.items[(a[(myUndo.undoCount())-1][0])+1][a[(myUndo.undoCount())-1][1]] = None
                        e.append(4)
                        del d[-1]
                    # print((a[(myUndo.undoCount())-1][0])+1,(a[(myUndo.undoCount())-1][0]))
                    #inventory.items[a[(myUndo.undoCount())][0]][a[(myUndo.undoCount())][1]] = None
                    my_tuple = tuple(my_list)
                  
            else:
                print("Aucune action à annuler")

      if ev.type == pygame.MOUSEBUTTONDOWN:
          posInv = inventory.Get_pos()
          # If Buttondown is Mouse1
          if optique:
            print("test")
          else: 
            if ev.button == 1:
              # Check if click is in the grid and does stuff
              if inventory.In_grid(posInv[0],posInv[1]):
                if selected:
                    selected = inventory.Add(selected,posInv)
                elif inventory.items[posInv[0]][posInv[1]]:
                    selected = inventory.items[posInv[0]][posInv[1]]
                    inventory.items[posInv[0]][posInv[1]] = None
                    
            if ev.button == 3:
              if inventory.In_grid(posInv[0],posInv[1]):
                if inventory.items[posInv[0]][posInv[1]]:
                  selectedMove = inventory.items[posInv[0]][posInv[1]]
      if ev.type == pygame.KEYDOWN:
        if selectedMoves != ([], []):
          if ev.key == pygame.K_RIGHT:
            for selectedElement, selectedCoord in zip(selectedMoves[0], selectedMoves[1]):
              inventory.items[selectedCoord[0]][selectedCoord[1]] = None
              my_list = list(selectedCoord)
              my_list[0] +=1
              my_tuple = tuple(my_list)
              selectedMoves = inventory.Check_adjacent(my_tuple[0], my_tuple[1])
              inventory.Add(selectedElement,my_tuple)
            (posInv, selectedMoves) = move_direction(4, posInv)

          if ev.key == pygame.K_LEFT:
            for selectedElement, selectedCoord in zip(selectedMoves[0], selectedMoves[1]):
              inventory.items[selectedCoord[0]][selectedCoord[1]] = None
              my_list = list(selectedCoord)
              my_list[0] -=1
              my_tuple = tuple(my_list)
              selectedMoves = inventory.Check_adjacent(my_tuple[0], my_tuple[1])
              inventory.Add(selectedElement,my_tuple)
            (posInv, selectedMoves) = move_direction(3, posInv)

          if ev.key == pygame.K_DOWN:
            for selectedElement, selectedCoord in zip(selectedMoves[0], selectedMoves[1]):
              inventory.items[selectedCoord[0]][selectedCoord[1]] = None
              my_list = list(selectedCoord)
              my_list[1] +=1
              my_tuple = tuple(my_list)
              selectedMoves = inventory.Check_adjacent(my_tuple[0], my_tuple[1])
              inventory.Add(selectedElement,my_tuple)
            (posInv, selectedMoves) = move_direction(2, posInv)

          if ev.key == pygame.K_UP:
            for selectedElement, selectedCoord in zip(selectedMoves[0], selectedMoves[1]):
              inventory.items[selectedCoord[0]][selectedCoord[1]] = None
              my_list = list(selectedCoord)
              my_list[1] -=1
              my_tuple = tuple(my_list)
              selectedMoves = inventory.Check_adjacent(my_tuple[0], my_tuple[1])
              inventory.Add(selectedElement,my_tuple)
            (posInv, selectedMoves) = move_direction(1, posInv)

        elif selectedMove != None:
          if ev.key == pygame.K_RIGHT:
            (posInv, selectedMoves) = move_direction(4, posInv)

          if ev.key == pygame.K_LEFT:
            (posInv, selectedMoves) = move_direction(3, posInv)

          if ev.key == pygame.K_DOWN:
            (posInv, selectedMoves) = move_direction(2, posInv)

          if ev.key == pygame.K_UP:
            (posInv, selectedMoves) = move_direction(1, posInv)

          if ev.key == pygame.K_RETURN:
            selectedMove = None

    mouse = pygame.mouse.get_pos()
    #####################################################
    #(Buttons) creates pressable boxes in specific areas#
    #####################################################

    button1 = {'screenX': 10, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button1['screenX'], button1['screenY'], button1['boxWidth'], button1['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_red,[button1['screenX'],button1['screenY'],button1['boxWidth'],button1['boxHeight']])
    else:
        pygame.draw.rect(screen,color_red_hovered,[button1['screenX'],button1['screenY'],button1['boxWidth'],button1['boxHeight']])

    button2 = {'screenX': 70, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button2['screenX'], button2['screenY'], button2['boxWidth'], button2['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_green,[button2['screenX'],button2['screenY'],button2['boxWidth'],button2['boxHeight']])
    else:
        pygame.draw.rect(screen,color_green_hovered,[button2['screenX'],button2['screenY'],button2['boxWidth'],button2['boxHeight']])

    button3 = {'screenX': 130, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button3['screenX'], button3['screenY'], button3['boxWidth'], button3['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_blue,[button3['screenX'],button3['screenY'],button3['boxWidth'],button3['boxHeight']])
    else:
        pygame.draw.rect(screen,color_blue_hovered,[button3['screenX'],button3['screenY'],button3['boxWidth'],button3['boxHeight']])

    button4 = {'screenX': 190, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button4['screenX'], button4['screenY'], button4['boxWidth'], button4['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_yellow,[button4['screenX'],button4['screenY'],button4['boxWidth'],button4['boxHeight']])
    else:
        pygame.draw.rect(screen,color_yellow_hovered,[button4['screenX'],button4['screenY'],button4['boxWidth'],button4['boxHeight']])

#    button5 = {'screenX': 250, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
#    if isInDimension(button5['screenX'], button5['screenY'], button5['boxWidth'], button5['boxHeight'], mouse[0], mouse[1]):
#        pygame.draw.rect(screen,color_dark,[button5['screenX'],button5['screenY'],button5['boxWidth'],button5['boxHeight']])
#    else:
#        pygame.draw.rect(screen,color_dark,[button5['screenX'],button5['screenY'],button5['boxWidth'],button5['boxHeight']])

    button6 = {'screenX':260, 'screenY': 400, 'boxWidth': 100, 'boxHeight': 40}
    if isInDimension(button6['screenX'],button6['screenY'], button6['boxWidth'], button6['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_gray,[button6['screenX'],button6['screenY'],button6['boxWidth'],button6['boxHeight']])
        screen.blit(font.render('Undo', True, (0, 0, 0)), (button6['screenX'], button6['screenY']))
    else:
        pygame.draw.rect(screen,color_light,[button6['screenX'], button6['screenY'], button6['boxWidth'], button6['boxHeight']])
        screen.blit(font.render('Undo', True, (0, 0, 0)), (button6['screenX'], button6['screenY']))

# Redo Button    
#    button7 = {'screenX':500, 'screenY': 500, 'boxWidth': 100, 'boxHeight': 40}
#    if isInDimension(button7['screenX'],button7['screenY'], button7['boxWidth'], button7['boxHeight'], mouse[0], mouse[1]):
#        pygame.draw.rect(screen,color_red,[button7['screenX'],button7['screenY'],button7['boxWidth'],button7['boxHeight']])
#        screen.blit(font.render('Redo', True, (0, 0, 0)), (button7['screenX'], button7['screenY']))
#    else:
#        pygame.draw.rect(screen,color_yellow,[button7['screenX'], button7['screenY'], button7['boxWidth'], button6['boxHeight']])
#        screen.blit(font.render('Redo', True, (0, 0, 0)), (button7['screenX'], button7['screenY']))


    # updates the frames of the game
    pygame.display.update()