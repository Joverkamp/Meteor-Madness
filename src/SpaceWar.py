import pygame
from pygame.locals import *
from random import randint

pygame.init()

white  = (255, 255, 255)
black  = (  0,   0,   0)
red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
purple = (180,   0, 180)
yellow = (255, 255,   0)


screenWidth = 450
screenHeight = 550
screenSize = [screenWidth, screenHeight]
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("WINDOW TITLE HERE")

clock = pygame.time.Clock()
velocity = 10
pspeed = 1
chance = 1

playerx = 200 
playery = 460

fire = pygame.mixer.Sound("laser.wav")
boost = pygame.mixer.Sound("metdoor.wav")
explode = pygame.mixer.Sound("explosion.wav")




#bulletwidth = 10
#bulletheight = 20



def check_keys():
    global playerx, playery
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player.rect.x >= 5:
        player.rect.x -= 4
    if keys[K_RIGHT] and player.rect.x <= 390:
        player.rect.x += 4
    if keys[K_SPACE] and bullet.rect.y < 0:
        bullet.rect.x = player.rect.x+20
        bullet.rect.y = player.rect.y-50
        fire.play()
        allsprites.add(bullet)
        
       

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ship.jpg")
        self.rect = self.image.get_rect()
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,75])
        self.image.fill(green)
        self.rect = self.image.get_rect()
        
class Pellet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("meteor2.png")
        self.rect = self.image.get_rect()
        
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15,15])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        

        

    
 
    
player = Player()
bullet = Bullet()

player.rect.x = playerx
player.rect.y = playery
    
allsprites = pygame.sprite.Group()
allsprites.add(player)

pellets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

done = False
score = 0
level = 1
lives = 5


while not done:
    # 1. Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    check_keys()

    # 2. Program logic, change variables, etcmovebullets()   
   
   
    collideList = pygame.sprite.spritecollide(bullet, pellets, True)
    for pellet in collideList:
        score += 1
        allsprites.remove(pellet)
        pellets.remove(pellet)
        explode.play()
        
    collideList = pygame.sprite.spritecollide(player, powerups, True)
    for powerup in collideList:
        boost.play()
        if velocity < 50:
            velocity +=5
        allsprites.remove(powerup)
        powerups.remove(powerup)
    
    collideList = pygame.sprite.spritecollide(player, pellets, True)
    for pellet in collideList:
        lives -= 1
        #noise
        allsprites.remove(pellet)
        pellets.remove(pellet)
        clock.tick(2)
        
    dieRoll = randint(1,40)
    if dieRoll <= chance:
        pellet = Pellet()
        pellet.rect.x = randint(35, screenWidth - 35)
        pellet.rect.y = 0
        pellets.add(pellet)
        allsprites.add(pellet)
    for pellet in pellets:
        pellet.rect.y += pspeed
        
    dieRoll = randint(1,1000)
    if dieRoll <= 1:
        powerup = PowerUp()
        powerup.rect.x = randint(35, screenWidth - 35)
        powerup.rect.y = 0
        powerups.add(powerup)
        allsprites.add(powerup)
    for powerup in powerups:
        powerup.rect.y += pspeed
        
        
    bullet.rect.y -= velocity
    
    if score == 10:
        level = 2
        pspeed = 1
        chance = 2
    if score == 25:
        level = 3
        pspeed = 2
    if score == 50:
        level = 4
        pspeed = 3
    if score == 100:
        level = 5
        pspeed = 3
        chance = 4
    if score == 200:
        level = 6
        pspeed = 4
    if score == 300:
        level = 7
        pspeed = 4
        chance = 5
    if score == 500:
        level = 8
        pspeed = 5
    if score == 750:
        level = 9
        pspeed = 5
        chance = 6
    if score == 1000:
        level = 10
        pspeed = 6

    # 3. Draw stuff
    bgSurface = pygame.image.load("background.png")
    screen.blit(bgSurface, [0,0])
    
    #screen.fill(white)
    allsprites.draw(screen)
    #pygame.draw.line(screen, green, [100, 200], [150, 300], 3)
    #pygame.draw.line(screen, green, [150, 300], [200, 200], 3)
    font = pygame.font.Font(None, 40)
    text = font.render("Score: %d" % score, True, black)
    screen.blit(text, [3, 525])
    
    text = font.render("Level: %d" % level, True, black)
    screen.blit(text, [173, 525])
    
    text = font.render("Lives: %d" % lives, True, black)
    screen.blit(text, [343, 525])
    
    if lives < 1:
        font = pygame.font.Font(None, 100)
        text = font.render("GAME OVER", True, red)
        screen.blit(text, [15, 400])
        break
    clock.tick(10000)
    pygame.display.flip()
    
pygame.display.flip()
clock.tick(1/5)
pygame.quit()
