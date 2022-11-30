# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 17:04:58 2022

@author: younn
"""

import pygame
import sys
import time
from undo import Undo
myUndo = Undo()
a = []

  
# initializing the constructor
pygame.init()
clock = pygame.time.Clock()
  
# screen resolution
res = (720,720)
  
# opens up a window
screen = pygame.display.set_mode(res)
  
# white color
color = (255,255,255)

#title of game
pygame.display.set_caption('pygame')
  
# light shade of the button
color_light = (170,170,170)
  
# dark shade of the button
color_dark = (100,100,100)
  
# stores the width of the
# screen into a variable
width = screen.get_width()
  
# stores the height of the
# screen into a variable
height = screen.get_height()
  
# defining a font
smallfont = pygame.font.SysFont('Corbel',35)
# text writted on textbox
user_text = ''
# create rectangle for textbox
input_rect = pygame.Rect(200, 200, 140, 32)
  
# rendering a text written in
# this font
text = smallfont.render('Select' , True , color)
  
# rendering a text written in
# this font
text2 = smallfont.render('Move to' , True , color)

# rendering a text written in
# this font
text3 = smallfont.render('Test' , True , color)

#check if textbox is active
active = False

while True:

    
    for ev in pygame.event.get():
        
        # if user types QUIT then the screen will close
        if ev.type == pygame.QUIT:
            pygame.quit()
            
        #check if keyboard button is clicked
        if ev.type == pygame.KEYDOWN and active is True:
            # Check for backspace
            if ev.key == pygame.K_BACKSPACE:
  
                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]
                
            # Unicode standard is used for string
            # formation
            else:
                user_text += ev.unicode
                myUndo(a.append, [user_text], [], "letters", a.pop)
            
            if ev.key == pygame.K_RETURN:
                    pygame.quit()
              
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONUP:
              
            #if the mouse is clicked on the
            # button the game is terminated
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                pygame.quit()
                
            #if the mouse is clicked on the
            # button the game is terminated
            if width/2 <= mouse[0] <= width/2+140 and height/3 <= mouse[1] <= height/3+40:
                #pygame.quit()
                myUndo.redo()
                user_text = a[(myUndo.redoCount())-1]
            #if the mouse is clicked on the
            # button the game is terminated
            if width/2 <= mouse[0] <= width/2+140 and height/4 <= mouse[1] <= height/4+40:
                myUndo.undo()
                user_text = a[(myUndo.undoCount())-1]
            #Verify if textbox is active
            if input_rect.collidepoint(ev.pos):
                active = True
            else:
                active = False
        
                  
    # fills the screen with a color
    screen.fill((60,25,60))
      
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])
    else:
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])

    #Button 2
    if width/2 <= mouse[0] <= width/2+140 and height/3 <= mouse[1] <= height/3+40:
        pygame.draw.rect(screen,color_light,[width/2,height/3,140,40])
    else:
        pygame.draw.rect(screen,color_dark,[width/2,height/3,140,40])
        
    #Button 3
    if width/2 <= mouse[0] <= width/2+140 and height/4 <= mouse[1] <= height/4+40:
        pygame.draw.rect(screen,color_light,[width/2,height/4,140,40])
    else:
        pygame.draw.rect(screen,color_dark,[width/2,height/4,140,40])
        
    # draw rectangle and argument passed which should
    # be on screen
    pygame.draw.rect(screen, color, input_rect)
    text_surface = smallfont.render(user_text, True, (0, 0, 0))
      
    # superimposing the text onto our button
    screen.blit(text , (width/2+50,height/2))
    screen.blit(text2 , (width/2+20,height/3))
    screen.blit(text3 , (width/2+20,height/4))
    #and textbox
    #render at position stated in arguments
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    
    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect.w = max(100, text_surface.get_width()+10)
    
    # clock.tick(60) means that for every second at most
    # 60 frames should be passed.
    clock.tick(60)
    
    # updates the frames of the game
    pygame.display.flip()
    
