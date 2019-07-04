import pygame as pg
import glob
import os
import numpy as np
from PIL import Image

#For resizing frame images while maintaining the aspect ratio
"""
from PIL import Image

newwidth = 60

for file in glob.glob(r'Images\*.png'):
    img = Image.open(file)
    wpercent = ( newwidth / float(img.size[0]) )
    newheight = int( ( float(img.size[1]) * float(wpercent) ) )
    img = img.resize( (newwidth, newheight), Image.ANTIALIAS )
    img.save(file)  
        
# resizing the pipe image    
pipe_img = Image.open(r'Images\Pipe\pipe.png')
pipe_img = pipe_img.resize((100, 614))
pipe_img.save(r'Images\Pipe\pipe.png') 
"""    

pg.init()   #initiating the game

pg.mixer.Channel(0).play(pg.mixer.Sound('Sounds\game.wav'), -1) #maingame sound
pg.mixer.Channel(2).set_volume(0.5) #channel for flap sound

scr_height = 550
scr_width = 336
g_height = 100

pipe_length = 320        #upper limit of pipe
pipe_down = scr_height - g_height     #lower limit of pipe
pipe_up = pipe_down - pipe_length - 1 
pipe_diff = 100

bird_width = 60
bird_height = 51

win = pg.display.set_mode((scr_width, scr_height))  #Setting the display screen
pg.display.set_caption("Flappy Bird")
bg = pg.image.load(r'Images\BG\bg.png')
ground = pg.image.load(r'Images\BG\ground.png')

roll_cur_bg = 0            #roll variables for rolling the background
roll_next_bg = scr_width
bg_vel = 0.4

roll_cur_g = 0            #roll variables for rolling the ground
roll_next_g = scr_width
g_vel = 3  

clock = pg.time.Clock() 

class bird(object):                             #character class
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.change = 6         #upward velocity when flapped
        self.acc = 0.2          #normal downward acceleration 
        self.vel = 0            #downward velocity that increases with downward acceleration
        self.time = 0           #for frame change
        self.cur_angle = 0      #angle of rotation of character image
        self.isup = False       #true when character is flapped upwards
        
        self.flaprate = 4       
        self.frames = [None] * (self.flaprate * 4) 
        self.cur_image = pg.image.load(r'Images\Bird\frame1.png')   #current image of character to be blitted
        
    def createFrames(self): 
        i = 0
        
        for file in glob.glob(r'Images\Bird\*.png'):
            for j in range(self.flaprate):
                self.frames[i] = pg.image.load(file)
                i += 1
    
    def draw(self, win):
        win.blit(self.cur_image , (self.x, self.y))

pipe_img = pg.image.load(r'Images\Pipe\pipe.png').convert()
pipe_width = 100

class Pipe(object):                             #Pipe class 
    def __init__(self):
        self.x = scr_width 
        self.y = np.random.randint(pipe_up, pipe_down + 1)
        
        while pipe_length < scr_height - g_height - self.y:         #To prevent drawing of pipes of length more than the available pipe_length
            self.y = np.random.randint(pipe_up, pipe_down + 1)
        
        self.vel = g_vel
        
    def draw(self, win):
        win.blit(pipe_img, (self.x, self.y))
        win.blit(pg.transform.rotate(pipe_img, 180), (self.x, self.y - 100 - pipe_length))
       
run = True              #main loop run variable

blue = bird(100, 100, 60, 51)   #creating bluebird character
blue.createFrames()             #creating bluebird frames

green = Pipe()          

def roll_bg():                              #Handles rolling of background
    global roll_cur_bg, roll_next_bg
    
    roll_cur_bg = (roll_cur_bg - bg_vel)
    roll_next_bg = (roll_next_bg - bg_vel)
    
    if roll_cur_bg <= -scr_width:
        roll_cur_bg = scr_width
        
    if roll_next_bg <= -scr_width:
        roll_next_bg = scr_width

def draw_bg(win):                           #Blits the rolling background
    global roll_cur_bg, roll_next_bg
     
    win.blit(bg, (roll_cur_bg, 0))
    win.blit(bg, (roll_next_bg, 0))

def roll_g():                               #Handles rolling of Ground
    global roll_cur_g, roll_next_g
    
    roll_cur_g = (roll_cur_g - g_vel)
    roll_next_g = (roll_next_g - g_vel)
    
    if roll_cur_g <= -scr_width:
        roll_cur_g = scr_width
        roll_next = 0
        
    if roll_next_g <= -scr_width:
        roll_next_g = scr_width
        roll_cur = 0
    
def draw_g(win):                            #Blits the rolling Ground
    global roll_cur_g, roll_next_g
    
    win.blit(ground, (roll_cur_g, scr_height - g_height))
    win.blit(ground, (roll_next_g, scr_height - g_height))
    
def winUpdate():
    roll_bg()
    draw_bg(win)
    
    green.draw(win)
    
    roll_g()
    draw_g(win)
    
    blue.draw(win)
   
    pg.display.update()
    
while run:
   
    clock.tick(60)      #setting fps
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    keys = pg.key.get_pressed()         #storing current state of all keys
    
    if keys[pg.K_UP]:                   #if up arrow is pressed
        #pg.mixer.Channel(2).play(pg.mixer.Sound('Sounds\jump.wav'))
        blue.vel = 0
        blue.cur_angle = 30
        blue.isup = True
            
        if blue.y > 0:                  #to ensure character remains in the screen 
            blue.y -= blue.change
                
        else:
            blue.y = 0
                
      
    if blue.isup == True:
        blue.cur_image = pg.transform.rotate(blue.frames[blue.time], (blue.cur_angle))
       
    else:
        if blue.y == scr_height - bird_height - ground_height:
            blue.cur_image = blue.frames[blue.time]
                
        else:    
            blue.cur_image = pg.transform.rotate(blue.frames[blue.time], max(blue.cur_angle - (blue.vel * 10), -90))             
        
    winUpdate()
    
    blue.isup = False;
    
    blue.time = (blue.time + 1) % (blue.flaprate * 4)   #for changing frames of character
        
   
    if blue.y + blue.vel <= scr_height - bird_height - g_height:   #to ensure character doesnt go below the screen height
        blue.y += blue.vel
        blue.vel += blue.acc    #downward acceleration
            
    else:
        #run = False
        blue.y = scr_height - bird_height - g_height
        blue.vel = 0    
        
        
    if green.x < -(pipe_width):
        green.x = scr_width
        
        green.y = np.random.randint(pipe_up, pipe_down + 1) 
        
        while green.y - pipe_diff > pipe_length:                              #To prevent drawing of pipes of length more than the available pipe_length
            green.y = np.random.randint(pipe_up, pipe_down + 1)
        
    else:
        green.x -= green.vel
        


  
pg.quit()
