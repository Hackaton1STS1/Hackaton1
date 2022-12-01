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
b= []
c= []
####Verify the last direction on undo
d=[]

# initializing the constructor
pygame.init()
clock = pygame.time.Clock()
mouse = pygame.mouse.get_pos()

# screen resolution
res = (1200,600)
screen = pygame.display.set_mode(res)

###################
#Button Properties#
###################
# # black color
# bcolor = (120,120,0)
# # light shade of the button
# bcolor_light = (170,170,170)
# # dark shade of the button
# bcolor_dark = (100,100,100)
# # width and height of the screen
# width = screen.get_width()
# height = screen.get_height()
# # defining a font
# smallfont = pygame.font.SysFont('Corbel',35)
# # rendering undo text
# text = smallfont.render('Undo' , True , bcolor)
# # rendering redo text
# text2 = smallfont.render('Redo' , True , bcolor)
# # create rectangle for textbox
# input_rect = pygame.Rect(700, 500, 140, 32)
# #check if textbox is active
# active = False
# # superimposing the text onto our button
# screen.blit(text , (width/2+50,height/2))
# screen.blit(text2 , (width/2+20,height/3))
# # if mouse is hovered on a button it
# # changes to lighter shade 
# if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
#     pygame.draw.rect(screen,bcolor_light,[width/2,height/2,140,40])
# else:
#     pygame.draw.rect(screen,bcolor_dark,[width/2,height/2,140,40])

# #Button 2
# if width/2 <= mouse[0] <= width/2+140 and height/3 <= mouse[1] <= height/3+40:
#     pygame.draw.rect(screen,bcolor_light,[width/2,height/3,140,40])
# else:
#     pygame.draw.rect(screen,bcolor_dark,[width/2,height/3,140,40])
# # clock.tick(60) means that for every second at most
# # 60 frames should be passed.
# clock.tick(60)
###################
  
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
  

#these are the images that get shown as items, different color circle for each item
items = [pygame.Surface((50,50),pygame.SRCALPHA) for x in range(4)]
pygame.draw.circle(items[0],color_red,(25,25),25)
pygame.draw.circle(items[1],color_green,(25,25),25)
pygame.draw.circle(items[2],color_blue,(25,25),25)
pygame.draw.circle(items[3],color_yellow,(25,25),25)

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
  def Delete(self,Item,xy):
    print("test")
    items[xy[0]][xy[1]] = None

  #add an item/s
  def Add(self,Item,xy):
      x, y = xy
      if self.items[x][y]:
          if self.items[x][y][0].id == Item[0].id:
              self.items[x][y][1] += Item[1]
          else:
              temp = self.items[x][y]
              self.items[x][y] = Item
              return temp
      else:
          self.items[x][y] = Item
  
  
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
selected = None
selectedMove = None
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
            selected = [Item(0),1]
          # Check if clicked Button2
          if isInDimension(button2['screenX'], button2['screenY'], button2['boxWidth'], button2['boxHeight'], mouse[0], mouse[1]):
            selected = [Item(1),1]
          # Check if clicked Button3
          if isInDimension(button3['screenX'], button3['screenY'], button3['boxWidth'], button3['boxHeight'], mouse[0], mouse[1]):
            selected = [Item(2),1]
          # Check if clicked Button4
          if isInDimension(button4['screenX'], button4['screenY'], button4['boxWidth'], button4['boxHeight'], mouse[0], mouse[1]):
            selected = [Item(3),1]
          # Check if clicked Button4
          if isInDimension(button5['screenX'], button5['screenY'], button5['boxWidth'], button5['boxHeight'], mouse[0], mouse[1]):
            print("Entered Button")
          # Check if clicked Button6
          if isInDimension(button6['screenX'], button6['screenY'], button6['boxWidth'], button6['boxHeight'], mouse[0], mouse[1]):
            myUndo.undo()
            undoC = (myUndo.undoCount())-1
            a1 = a[undoC-1][0]
            a2 = a[undoC-1][1]
            posInvUndo = (a1,a2)
            my_list = list(posInvUndo)
            print (c[0][0])
            if inventory.In_grid(my_list[0],my_list[1]):
              if len(b)>=2 and len(c)>=0 and len(d)>=0:
                # selectedMove2 = inventory.items[my_list[0]][my_list[1]]
                selectedMove2 = b[0]
                inventory.Add(selectedMove2,a[(myUndo.undoCount())-1])
                #delete last item depending on direction choosed
                #Up
                print(d)
                print(d[-1])
                if(d[-1]==1):
                    inventory.items[a[(myUndo.undoCount())-1][0]][(a[(myUndo.undoCount())-1][1])+1] = None
                    del d[-1]
                #Down
                elif (d[-1]==2):
                    inventory.items[a[(myUndo.undoCount())-1][0]][(a[(myUndo.undoCount())-1][1])-1] = None
                    del d[-1]
                #Left
                elif (d[-1]==3):
                    inventory.items[(a[(myUndo.undoCount())-1][0])+1][a[(myUndo.undoCount())-1][1]] = None
                    del d[-1]
                #Right
                elif (d[-1]==4):
                    inventory.items[(a[(myUndo.undoCount())-1][0])-1][a[(myUndo.undoCount())-1][1]] = None
                    del d[-1]
                # print((a[(myUndo.undoCount())-1][0])+1,(a[(myUndo.undoCount())-1][0]))
                #inventory.items[a[(myUndo.undoCount())][0]][a[(myUndo.undoCount())][1]] = None
                my_tuple = tuple(my_list)
                
                
            # selectedMove2 = inventory.items[posInv[0]][posInv[1]]
            # inventory.items[posInv[0]][posInv[1]] = None
            # my_list = list(posInv)
            # my_list[0] +=1
            # my_tuple = tuple(my_list)
            # myUndo(a.append, [posInv], [], "last position", a.pop)
            # posInv = my_tuple
            # posInv = a[(myUndo.undoCount())]
            # myUndo.undo()
            # selectedMove = None
            # inventory.items[posInv[0]][posInv[1]] = a[(myUndo.undoCount())]
            # print(a[(myUndo.undoCount())-1])
          # if isInDimension(button7['screenX'], button7['screenY'], button7['boxWidth'], button7['boxHeight'], mouse[0], mouse[1]):
          #   # myUndo.undo()
          #   # inventory.items[posInv[0]][posInv[1]] = a[(myUndo.undoCount())]
          #   print(a[(myUndo.undoCount())-1])
            
      if ev.type == pygame.MOUSEBUTTONDOWN:
          posInv = inventory.Get_pos()
          # If Buttondown is Mouse1
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
            uColor = inventory.items[posInv[0]][posInv[1]]
            inventory.items[posInv[0]][posInv[1]] = None
            my_list = list(posInv)
            my_list[0] +=1
            my_tuple = tuple(my_list)
            myUndo(a.append, [posInv], [], "last position", a.pop)
            b.append(uColor)
            c.append(selectedMove)
            posInv = my_tuple
            d.append(4)
            inventory.Add(selectedMove,posInv)
            #selected= None
          if ev.key == pygame.K_LEFT:
            uColor = inventory.items[posInv[0]][posInv[1]]
            inventory.items[posInv[0]][posInv[1]] = None
            my_list = list(posInv)
            my_list[0] -=1
            my_tuple = tuple(my_list)
            myUndo(a.append, [posInv], [], "last position", a.pop)
            b.append(uColor)
            c.append(selectedMove)
            d.append(3)
            posInv = my_tuple
            inventory.Add(selectedMove,posInv)
            #selected= None
          if ev.key == pygame.K_DOWN:
            uColor = inventory.items[posInv[0]][posInv[1]]
            inventory.items[posInv[0]][posInv[1]] = None
            my_list = list(posInv)
            my_list[1] +=1
            my_tuple = tuple(my_list)
            myUndo(a.append, [posInv], [], "last position", a.pop)
            b.append(uColor)
            c.append(selectedMove)
            d.append(2)
            posInv = my_tuple
            inventory.Add(selectedMove,posInv)
            #selected= None
          if ev.key == pygame.K_UP:
            uColor = inventory.items[posInv[0]][posInv[1]]
            inventory.items[posInv[0]][posInv[1]] = None
            my_list = list(posInv)
            my_list[1] -=1
            my_tuple = tuple(my_list)
            myUndo(a.append, [posInv], [], "last position", a.pop)
            b.append(uColor)
            c.append(selectedMove)
            d.append(1)
            posInv = my_tuple
            inventory.Add(selectedMove,posInv)
            
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
      
    #####################################################
    #(Buttons) creates pressable boxes in specific areas#
    #####################################################
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
    
    button6 = {'screenX':500, 'screenY': 400, 'boxWidth': 100, 'boxHeight': 40}
    if isInDimension(button6['screenX'],button6['screenY'], button6['boxWidth'], button6['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_red,[button6['screenX'],button6['screenY'],button6['boxWidth'],button6['boxHeight']])
        screen.blit(font.render('Undo', True, (0, 0, 0)), (button6['screenX'], button6['screenY']))
    else:
        pygame.draw.rect(screen,color_yellow,[button6['screenX'], button6['screenY'], button6['boxWidth'], button6['boxHeight']])
        screen.blit(font.render('Undo', True, (0, 0, 0)), (button6['screenX'], button6['screenY']))
    button7 = {'screenX':500, 'screenY': 500, 'boxWidth': 100, 'boxHeight': 40}
    if isInDimension(button7['screenX'],button7['screenY'], button7['boxWidth'], button7['boxHeight'], mouse[0], mouse[1]):
        pygame.draw.rect(screen,color_red,[button7['screenX'],button7['screenY'],button7['boxWidth'],button7['boxHeight']])
        screen.blit(font.render('Redo', True, (0, 0, 0)), (button7['screenX'], button7['screenY']))
    else:
        pygame.draw.rect(screen,color_yellow,[button7['screenX'], button7['screenY'], button7['boxWidth'], button6['boxHeight']])
        screen.blit(font.render('Redo', True, (0, 0, 0)), (button7['screenX'], button7['screenY']))



    # updates the frames of the game
    pygame.display.update()