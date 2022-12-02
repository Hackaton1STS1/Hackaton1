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


# initializing the constructor
pygame.init()
mouse = pygame.mouse.get_pos()

# screen resolution
res = (600,600)
screen = pygame.display.set_mode(res)
  
# colors & fonts
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
color_red = (255,0,0)
color_red_hovered = (200,0,0)
color_green = (0,255,0)
color_green_hovered = (0,200,0)
color_blue = (0,0,255)
color_blue_hovered = (0,0,200)
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

# Item class
class Item:
    def __init__(self,id):
        self.id = id
        self.surface = items[id]
    
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
    print("test")
    items[xy[0]][xy[1]] = None

  #add an item/s
  def Add(self,Item,xy):
      x, y = xy
      if self.items[x][y]:
            print(self.foreignIdIncrement)
            self.items[x][y][1] = self.foreignIdIncrement
            temp = self.items[x][y]
            self.items[x][y] = Item
            return temp
      else:
          self.items[x][y] = Item
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
    return (selectedMoves, elementCoordinates)
  
  #check whether the mouse in in the grid
  def In_grid(self,x,y):
    #print(self.col, self.rows, x, y)
    if 0 > x or x > self.col-1:
      return False
    if 0 > y or y > self.rows-1:
      return False
    return True




# returns if in dimension
def isInDimension(screenX, screenY, boxWidth, boxHeight, mouseX, mouseY):
  if (screenX <= mouseX <= screenX + boxWidth and screenY <= mouseY <= screenY+boxHeight):
    return True
  else:
    return False

# Specific-Use Variables
inventory = Inventory()
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
          # Check if clicked Button4
          if isInDimension(button5['screenX'], button5['screenY'], button5['boxWidth'], button5['boxHeight'], mouse[0], mouse[1]):
            print("Entered Button")
            
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
        if selectedMove != None:
          if ev.key == pygame.K_RIGHT:
            #inventory.Del(selected,posInv)
            inventory.items[posInv[0]][posInv[1]] = None
            my_list = list(posInv)
            my_list[0] +=1
            my_tuple = tuple(my_list)
            posInv = my_tuple
            selectedMoves = inventory.Check_adjacent(posInv[0], posInv[1])
            if (len(selectedMoves[0])-1 > 0):
              for i in range(len(selectedMoves[0])-1):
                inventory.Add(selectedMoves[0][0],selectedMoves[1])
            else:
              inventory.Add(selectedMove,posInv)
            print(selectedMoves)
            #selected= None
          if ev.key == pygame.K_LEFT:
            inventory.items[posInv[0]][posInv[1]] = None
            my_list = list(posInv)
            my_list[0] -=1
            my_tuple = tuple(my_list)
            posInv = my_tuple
            selectedMoves = inventory.Check_adjacent(posInv[0], posInv[1])
            if (len(selectedMoves[0])-1 > 0):
              for i in range(len(selectedMoves[0])-1):
                inventory.Add(selectedMoves[0][0],selectedMoves[1])
            else:
              inventory.Add(selectedMove,posInv)
            print(selectedMoves)
            #selected= None
          if ev.key == pygame.K_DOWN:
            inventory.items[posInv[0]][posInv[1]] = None
            my_list = list(posInv)
            my_list[1] +=1
            my_tuple = tuple(my_list)
            posInv = my_tuple
            selectedMoves = inventory.Check_adjacent(posInv[0], posInv[1])
            if (len(selectedMoves[0])-1 > 0):
              for i in range(len(selectedMoves[0])-1):
                inventory.Add(selectedMoves[0][0],selectedMoves[1])
            else:
              inventory.Add(selectedMove,posInv)
            print(selectedMoves)
            #selected= None
          if ev.key == pygame.K_UP:
            inventory.items[posInv[0]][posInv[1]] = None
            my_list = list(posInv)
            my_list[1] -=1
            my_tuple = tuple(my_list)
            posInv = my_tuple
            selectedMoves = inventory.Check_adjacent(posInv[0], posInv[1])
            if (len(selectedMoves[0])-1 > 0):
              for i in range(len(selectedMoves[0])-1):
                inventory.Add(selectedMoves[0][0],selectedMoves[1])
            else:
              inventory.Add(selectedMove,posInv)
            print(selectedMoves)
            
          if ev.key == pygame.K_RETURN:
            selectedMove = None

                
            
                # print(inventory.Get_pos())
            # TODO: Selectionner la goutte de la grille
            # Puis de déplacer les gouttes avec les flèches
            # Droite, Gauche, bas et haut
          
            #     selected = inventory.Add(selected,posInv)
            # elif inventory.items[posInv[0]][posInv[1]]:
            #     selected = inventory.items[posInv[0]][posInv[1]]
            #     inventory.items[posInv[0]][posInv[1]] = None
                    
    ## Out of the event detector
    #-
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # creates pressable boxes in specific areas
    button1 = {'screenX': 0, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button1['screenX'], button1['screenY'], button1['boxWidth'], button1['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_red,[button1['screenX'],button1['screenY'],button1['boxWidth'],button1['boxHeight']])
    else:
        pygame.draw.rect(screen,color_red_hovered,[button1['screenX'],button1['screenY'],button1['boxWidth'],button1['boxHeight']])

    button2 = {'screenX': 60, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button2['screenX'], button2['screenY'], button2['boxWidth'], button2['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_green,[button2['screenX'],button2['screenY'],button2['boxWidth'],button2['boxHeight']])
    else:
        pygame.draw.rect(screen,color_green_hovered,[button2['screenX'],button2['screenY'],button2['boxWidth'],button2['boxHeight']])

    button3 = {'screenX': 120, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button3['screenX'], button3['screenY'], button3['boxWidth'], button3['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_blue,[button3['screenX'],button3['screenY'],button3['boxWidth'],button3['boxHeight']])
    else:
        pygame.draw.rect(screen,color_blue_hovered,[button3['screenX'],button3['screenY'],button3['boxWidth'],button3['boxHeight']])

    button4 = {'screenX': 180, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button4['screenX'], button4['screenY'], button4['boxWidth'], button4['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_yellow,[button4['screenX'],button4['screenY'],button4['boxWidth'],button4['boxHeight']])
    else:
        pygame.draw.rect(screen,color_yellow_hovered,[button4['screenX'],button4['screenY'],button4['boxWidth'],button4['boxHeight']])

    button5 = {'screenX': 240, 'screenY': 400, 'boxWidth': 40, 'boxHeight': 40}
    if isInDimension(button5['screenX'], button5['screenY'], button5['boxWidth'], button5['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_dark,[button5['screenX'],button5['screenY'],button5['boxWidth'],button5['boxHeight']])
    else:
        pygame.draw.rect(screen,color_dark,[button5['screenX'],button5['screenY'],button5['boxWidth'],button5['boxHeight']])




    # updates the frames of the game
    pygame.display.update()