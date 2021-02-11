# imports
from pygame.locals import *
import sys , pygame , os , random , time
from colors import *

# initalization
pygame.init()
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

#game window
global fired
fired = False
score = 0
global lost
lost = False
win = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Rock Combat")
win.fill(black)

#images and font
spaceship =  pygame.transform.scale(pygame.image.load('spaceship.png').convert() , (75 , 75))
star = pygame.transform.scale(pygame.image.load('star.png') , (35 , 35))
spell = pygame.transform.scale(pygame.image.load('spell.png') , (75 , 75))
spelled = pygame.transform.rotate(spell, 90)
asteroid = pygame.transform.scale(pygame.image.load("asteroid.png") , (40 ,40))
font = pygame.font.Font('Bitty.ttf', 24)
explosive = pygame.transform.scale(pygame.image.load("explosion.png") , (240,240))

# definations
def move(x):
    win.blit(spaceship , (350+x,350))  
win.blit(spaceship , (350,350)) 

def starinst():
    if lost == False:
        pygame.time.delay(30)
        win.fill(black)
        for i in range (35):
            xpos = random.randint(1 , 800)
            ypos = random.randint(1,600)
            win.blit(star , (xpos , ypos))
            move(xspeed) 

def asterinst():
    if lost == False:
        if len(enemies) < 80:
            xpos = random.randint(1,800)
            enemy = win.blit(asteroid , (xpos,0))
            enemies.append(enemy)

def fire(offset = 0):
    if fired and len(spells) < 10:
        cast = win.blit(spelled ,  (xspeed + offset + 350 , 350))
        return cast

def destroy(num):
    enemies.pop(num)
    xpos = random.randint(1,800)
    enemy = win.blit(asteroid , (xpos,0))
    enemies.append(enemy)

#spaceship
speed = 30
xspeed = 0
move(xspeed)
spells = []
enemies = []

#main loop
while True:
    if lost == False:
        starinst()
        asterinst()
        scoretext = font.render(str(score), 1, white)
        win.blit(scoretext, (400 , 0))
        for i in range(len(enemies)-5):
            if enemies[i].y >= 600:
                enemies.pop(i)
            else:
                if xspeed + 350 + 50 >= enemies[i].x and xspeed + 350 -50 <= enemies[i].x and 350 >= enemies[i].y and 350 <= enemies[i].y:
                    win.blit(explosive , (xspeed + 275 ,275))
                    lost = True
                newpos = enemies[i].y + 10
                newpos_x = enemies[i].x
                enemy = win.blit(asteroid , (newpos_x , newpos))
                enemies[i] = enemy
        for i in range(len(spells)-3):
            if spells[i].y <= 0:
                spells.pop(i)
            else:
                for j in range(len(enemies)-20):
                    if spells[i].x + 75 >= enemies[j].x and spells[i].x - 75 <= enemies[j].x and spells[i].y + 75 >= enemies[j].y and spells[i].y - 75 <= enemies[j].y:
                        spells.pop(i)
                        destroy(j)
                        score += 1
                newpos = spells[i].y - 20
                newpos_x = spells[i].x
                proj = win.blit(spelled , (newpos_x , newpos))
                spells[i] = proj
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                fired = True
                proj = fire(-25)
                proj2 = fire(25)
                spells.append(proj)
                spells.append(proj2)
            if event.type == QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == KEYDOWN:
                if event.key == K_LEFT and xspeed + 350 > 0 and lost == False:
                    xspeed -= speed
                    move(xspeed)
                elif event.key == K_RIGHT and xspeed + 350 < 730 and lost == False:
                    xspeed += speed
                    move(xspeed)
        pygame.display.update() 