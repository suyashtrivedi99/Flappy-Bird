import pygame as pg
import glob

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

scr_height = 504
scr_width = 500

win = pg.display.set_mode((scr_width, scr_height))
pg.display.set_caption("Flappy Bird")

bg = pg.image.load(r'Images\BG\bg.png')

flaprate = 4

frames = [None] * (flaprate * 4)

i = 0
for file in glob.glob(r'Images\Bird\*.png'):
    for j in range(flaprate):
        frames[i] = pg.image.load(file)
        i += 1
            

clock = pg.time.Clock()

x = 50
y = 50
vel = 5
time = 0
rollbg = scr_width
rollbg2 = 0 
run = True
isjump = False

pg.mixer.music.load(r'Sounds\jump.mp3')
yj = 0
xj = -16
ystore = 0

def winUpdate():
    global time, rollbg, rollbg2
    
    win.blit(bg, (rollbg, 0))
    win.blit(bg, (rollbg2, 0))
    
    if isjump == True:
        cur_image = pg.transform.rotate(frames[time], (-yj)/4)
       
    else:
        cur_image = frames[time] 
    
    win.blit(cur_image , (x, y))
    pg.display.update()
    
    time = (time + 1) % (flaprate * 4)
    rollbg = (rollbg - 1)
    rollbg2 = (rollbg2 - 1)
    if rollbg2 == -scr_width:
        rollbg2 = 0
        
    if rollbg == 0:
        rollbg = scr_width
    
while run:
    clock.tick(60)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            #pg.mixer.music.stop()
    
    keys = pg.key.get_pressed()
    
    if keys[pg.K_LEFT]:
        x = (x - vel) % scr_width
      
    if keys[pg.K_RIGHT]:
        x = (x + vel) % scr_width
    
    if isjump == False:
        if keys[pg.K_UP]:
            y = (y - vel) % scr_height 
            
        if keys[pg.K_DOWN]:    
            y = (y + vel) % scr_height
            
        if keys[pg.K_SPACE]:
            isjump = True
            ystore = y
           
            pg.mixer.music.play(0)
        
    else:
        if xj == 17:
            isjump = False
            yj = 0
            xj = -16
            
            pg.mixer.music.stop()
            
        yj = (xj * xj) - 256 
        y = (ystore + yj) % scr_height
        
        xj += 1
    
    winUpdate()
pg.quit()    