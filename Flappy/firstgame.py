import pygame as pg
import glob
import os

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
"""

pg.init()

pg.mixer.Channel(0).play(pg.mixer.Sound('Sounds\game.wav'), -1)
pg.mixer.Channel(2).set_volume(0.5)

scr_height = 504
scr_width = 900

bird_width = 60
bird_height = 51

win = pg.display.set_mode((scr_width, scr_height))
pg.display.set_caption("Flappy Bird")
bg = pg.image.load(r'Images\BG\bg.png')

roll_cur = 0
roll_next = scr_width

clock = pg.time.Clock()

class bird(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.change = 5
        self.acc = 0.2
        self.vel = 0
        self.time = 0
        
        self.isjump = False
        self.jumpsize = 12
        self.xjump = -self.jumpsize
        self.yjump = 0
        self.ystore = 0
        
        self.flaprate = 4
        self.frames = [None] * (self.flaprate * 4) 
    
    def createFrames(self):
        i = 0
        
        for file in glob.glob(r'Images\Bird\*.png'):
            for j in range(self.flaprate):
                self.frames[i] = pg.image.load(file)
                i += 1
    
    def draw(self, win):
        if self.isjump == True:
            cur_image = pg.transform.rotate(self.frames[self.time], (-self.yjump)/4)
       
        else:
            if self.y == scr_height - bird_height:
                cur_image = self.frames[self.time]
                
            else:    
                cur_image = pg.transform.rotate(self.frames[self.time], -min(self.vel * 10, 90)) 
    
        win.blit(cur_image , (self.x, self.y))
        self.time = (self.time + 1) % (self.flaprate * 4)
        
        if self.isjump == False: 
            if self.y + self.vel <= scr_height - bird_height:
                self.y += self.vel
                self.vel += self.acc
            
            else:
                self.y = scr_height - bird_height
                self.vel = 0

class projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8
        
    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius) 

        
run = True

blue = bird(50, 50, 60, 51)
blue.createFrames()

bullets = []

def winUpdate():
    global roll_cur, roll_next
    
    win.blit(bg, (roll_cur, 0))
    win.blit(bg, (roll_next, 0))
    
    roll_cur = (roll_cur - 1)
    roll_next = (roll_next - 1)
    
    if roll_cur == -scr_width:
        roll_cur = scr_width
        
    if roll_next == -scr_width:
        roll_next = scr_width
    
    blue.draw(win)
    
    for bullet in bullets:
        bullet.draw(win)
    
    pg.display.update()
    

while run:
   
    clock.tick(60)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    for bullet in bullets:
        if bullet.x < scr_width and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        
       
    keys = pg.key.get_pressed()
    
    if keys[pg.K_x]:
        if len(bullets) < 5 and blue.time % 4 == 0:
            bullets.append(projectile(round(blue.x + blue.width // 2), round(blue.y + blue.height // 2), 6, (0,0,0)))
    
    if keys[pg.K_LEFT]:
        blue.x = (blue.x - blue.change) % scr_width
      
    if keys[pg.K_RIGHT]:
        blue.x = (blue.x + blue.change) % scr_width
    
    if blue.isjump == False:
        if keys[pg.K_UP]:
            blue.vel = 0
            
            if blue.y > 0: 
                blue.y -= blue.change
                
            else:
                blue.y = 0
                
        if keys[pg.K_DOWN]:
            blue.vel = 0
            
            if blue.y < scr_height - blue.height:
                blue.y += blue.change
            
            else:
                y = scr_height - bird_height    
            
        if keys[pg.K_SPACE]:
            pg.mixer.Channel(2).play(pg.mixer.Sound('Sounds\jump.wav'))

            blue.vel = 0
            blue.isjump = True
            blue.ystore = blue.y        
            
    else:
        if blue.xjump == blue.jumpsize + 1:
            blue.isjump = False
            blue.yjump = 0
            blue.xjump = -blue.jumpsize
            blue.vel = 0
            
        blue.yjump = (blue.xjump ** 2) - (blue.jumpsize ** 2)
        
        if blue.y > 0:
            blue.y = blue.ystore + blue.yjump
        
        else:
            blue.y = 0
        
        blue.xjump += 1
    
    winUpdate()
    
pg.quit()
