import pygame as pg
import glob
import os
import numpy as np
from PIL import Image
from time import sleep

#For resizing frame images while maintaining the aspect ratio
"""
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
#pg.mixer.Channel(2).set_volume(0.5) #channel for flap sound

scr_height = 550
scr_width = 336
g_height = 100

pipe_length = 320
pipe_width = 52
pipe_diff = 100
pipe_lower = scr_height - g_height - pipe_length  #if y coordinate of lower pipe is lesser than this, the image of lower pipe will come out of ground
pipe_upper = pipe_length + pipe_diff              #if y coordinate of upper pipe is greater than this, image of upper pipe will come out from top
pipes_num = 2

bird_width = 60
bird_height = 51
bird_x = 100
bird_y = 100

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
        
        y_cord = self.y + 20
        x_cord = self.x + 20
        w = self.width - 20
        h = self.height - 20
        
        self.hitbox = (x_cord, y_cord, w, h)
        
    def createFrames(self): 
        i = 0
        
        for file in glob.glob(r'Images\Bird\*.png'):
            for j in range(self.flaprate):
                self.frames[i] = pg.image.load(file)
                i += 1
    
    def draw(self, win):
        if self.y == scr_height - bird_height - g_height:
                self.cur_image = self.frames[self.time]
                
        else:    
            self.cur_image = pg.transform.rotate(self.frames[self.time], max(self.cur_angle - (self.vel * 10), -90))  
        
        win.blit(self.cur_image , (self.x, self.y))
        
        self.time = (self.time + 1) % (self.flaprate * 4)   #for changing frames of character
        
        self.y += self.vel
        self.vel += self.acc    #downward acceleration
           
        y_cord = self.y + self.cur_angle - self.vel - 15
        x_cord = self.x + self.cur_angle - self.vel - 5
        w = self.width - self.cur_angle + self.vel + 5
        h = self.height - self.cur_angle + self.vel + 10
        
        self.hitbox = (x_cord, y_cord, w, h)
        pg.draw.rect(win, (0, 255, 0), self.hitbox, 2)

pipe_img = pg.image.load(r'Images\Pipe\pipe.png').convert()

class Pipe(object):                             #Pipe class 
    def __init__(self, x):
        self.x = x 
        self.y = np.random.randint(pipe_lower, pipe_upper)
        self.width = pipe_width
        self.length = pipe_length
        
        self.vel = g_vel
        
        self.hitbox_lower = (self.x, self.y, self.width, self.length)
        self.hitbox_upper = (self.x, self.y - pipe_diff - self.length, self.width, self.length)
        
    def draw(self, win):
        win.blit(pipe_img, (self.x, self.y))
        win.blit(pg.transform.rotate(pipe_img, 180), (self.x, self.y - pipe_diff - pipe_length))
        
        self.hitbox_lower = (self.x, self.y, self.width, self.length)
        self.hitbox_upper = (self.x, self.y - pipe_diff - self.length, self.width, self.length)
        
        pg.draw.rect(win, (255, 0, 0), self.hitbox_lower, 2)
        pg.draw.rect(win, (255, 0, 0), self.hitbox_upper, 2)
     
    def hit(self):
        print('HIT')

run = True              #main loop run variable

blue = bird(bird_x, bird_y, bird_width, bird_height)   #creating bluebird character
blue.createFrames()             #creating bluebird frames

pipe1 = Pipe(scr_width)          
pipe2 = Pipe((scr_width * 1.6))          

cur_pipe = [pipe1, pipe2]
pipe_pos = 0

score = 0

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

def roll_pipe(pipe):
    if pipe.x < -(pipe_width):
        pipe.x = scr_width
        pipe.y = np.random.randint(pipe_lower, pipe_upper) 
        
    else:
        pipe.x -= pipe.vel

font_name = pg.font.match_font('algerian')

def draw_score(win, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 230, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    win.blit(text_surface, text_rect)
    
def winUpdate():
    global score
    
    roll_bg()
    draw_bg(win)
    
    pipe1.draw(win)
    pipe2.draw(win)
    
    roll_g()
    draw_g(win)
    
    blue.draw(win)
   
    draw_score(win, str(score), 50, scr_width / 2, 0)
    
    pg.display.update()
    
    roll_pipe(pipe1)
    roll_pipe(pipe2)
    
def collision():
    
    global run
    
    if pipe1.hitbox_lower[1] < blue.hitbox[1] + blue.hitbox[2] - 8\
    or blue.hitbox[1] < pipe1.hitbox_upper[1] + pipe1.hitbox_upper[3] \
    or blue.hitbox[1] + blue.hitbox[3] - 8 < pipe1.hitbox_upper[1] + pipe1.hitbox_upper[3]:
            
        if blue.hitbox[0] < pipe1.hitbox_lower[0]:
            if blue.hitbox[0] + blue.hitbox[2] > pipe1.hitbox_lower[0]:
                #BANG
                #sleep(0.5)
                run = False
        elif blue.hitbox[0] <= pipe1.hitbox_lower[0] + pipe1.width:
            #BANG
            #sleep(0.5)
            run = False
            
    if pipe2.hitbox_lower[1] < blue.hitbox[1] + blue.hitbox[2] - 8 \
    or blue.hitbox[1] < pipe2.hitbox_upper[1] + pipe2.hitbox_upper[3]\
    or blue.hitbox[1] + blue.hitbox[3] - 8 < pipe2.hitbox_upper[1] + pipe2.hitbox_upper[3]:
            
        if blue.hitbox[0] < pipe2.hitbox_lower[0]:
            if blue.hitbox[0] + blue.hitbox[2] > pipe2.hitbox_lower[0]:
                #BANG
                #sleep(0.5)
                run = False
        elif blue.hitbox[0] <= pipe2.hitbox_lower[0] + pipe2.width:
            #BANG
            #sleep(0.5)
            run = False
            
    if blue.y + blue.vel > scr_height - bird_height - g_height:        #to ensure character doesnt go below the screen height
        run = False       
    
def main_game(): 
    
    global run, pipe_pos, score
    
    while run:
       
        clock.tick(60)      #setting fps
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
    
        keys = pg.key.get_pressed()         #storing current state of all keys
        
        if keys[pg.K_UP]:                   #if up arrow is pressed
            blue.vel = 0
            blue.cur_angle = 30
            blue.isup = True
                
            if blue.y > 0:                  #to ensure character remains in the screen 
                blue.y -= blue.change
                    
            else:
                blue.y = 0
        
        if(blue.x + 15 >= cur_pipe[pipe_pos].x + pipe_width):
            score += 1
            pipe_pos = (pipe_pos + 1) % pipes_num
        
        collision()
        winUpdate()
    
main_game()

trans = 0
while trans < 1:
    if run == False:
        sleep(2)
        run = True
        
        blue = bird(bird_x, bird_y, bird_width, bird_height)   #creating bluebird character
        blue.createFrames()             #creating bluebird frames
        
        pipe1 = Pipe(scr_width)          
        pipe2 = Pipe((scr_width * 1.6))          
        
        cur_pipe = [pipe1, pipe2]
        pipe_pos = 0
        
        roll_cur_bg = 0            #roll variables for rolling the background
        roll_next_bg = scr_width
        
        roll_cur_g = 0            #roll variables for rolling the ground
        roll_next_g = scr_width
        trans += 1
        
        main_game()
  
pg.quit()


