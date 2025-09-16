import random 
import pygame
from pygame.locals import *


pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
fps = 50

screenwidth = 600
screenheight = 600


screen = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption("Flappy Bird by Sanyam Bhardwaj")

#Font and color for scoring
font = pygame.font.SysFont("Elephant", 40)
font1 = pygame.font.SysFont("Times New Roman", 30, bold=True, italic=True)
font2 = pygame.font.SysFont("Times New Roman", 30, italic=True)
gold = (255,215,0)
black = (0,0,0)




# game variables
gamescroll = 0
pipespeed = 10
scrollspeed = 4
pipegap = 135
pipefreq = 1500 #millisec
lastpipe = pygame.time.get_ticks() - pipefreq
score = 0
pipepass = False
 
# Game conditions
flying = False
gameover = False
startscreen = True

#background, ground and button img
bg = pygame.image.load("cg.png")
ground = pygame.image.load("ground.png")
bg2 = pygame.transform.scale(bg,(600,600))
buttonimg1 = pygame.image.load("restart.png")
buttonimg = pygame.transform.scale(buttonimg1, (100,70))
startbtn1 = pygame.image.load("start.png")
startbtn = pygame.transform.scale(startbtn1, (150,100))

#sounds
hitsfx = pygame.mixer.Sound("hit.wav") 
scoresfx = pygame.mixer.Sound("point.mp3")
flysfx = pygame.mixer.Sound("flapping.mp3")
hitplayed = False


try:
    with open("highscore.txt", "r") as file:
        highscore = int(file.read())
except:
    highscore = 0





def drawtext(text, font, textcol, x, y):
    img = font.render(text, True, textcol)
    screen.blit(img, (x, y))


def resetgame():
    pipegroup.empty()
    flappy.rect.x = 70
    flappy.rect.y = int(screenheight / 2)
    score = 0
    return score




class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f"bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
        

    def update(self):
            
            if flying == True:
                # gravity
                self.vel += 0.5
                if self.vel > 8:
                    self.vel = 8
                if self.rect.bottom < 500:
                    self.rect.y += int(self.vel)
            if gameover == False:
                #jump
                keys = pygame.key.get_pressed()
                if (pygame.mouse.get_pressed()[0] == 1 or keys[K_SPACE]) and self.clicked == False :
                    self.clicked = True
                    self.vel = -10
                if (pygame.mouse.get_pressed()[0] == 0 and not keys[K_SPACE]) and self.clicked == True :
                    self.clicked = False




                # for the animation
                self.counter += 1
                flap_cooldown = 5
                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                
                self.image = self.images[self.index]
            
            
                # rotating the bird 
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            # not mandatory
            else:
                
                self.image = pygame.transform.rotate(self.images[self.index],-90) 
                

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        # position 1 is for top and -1 is for bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - (pipegap/2)]
        if position == -1:
            self.rect.topleft = [x, y + (pipegap/2)]
        
    def update(self):
        self.rect.x -= pipespeed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image,(self.rect.x, self.rect.y))

        return action
        



birdgroup = pygame.sprite.Group()

pipegroup = pygame.sprite.Group()

flappy = Bird(70, int(screenheight/2))

birdgroup.add(flappy)

button = Button(screenwidth // 2 -50, screenheight // 2 -50, buttonimg)
startbutton = Button(screenwidth // 2 -100, screenheight // 2 -50, startbtn)
        



run = True
while run:

    clock.tick(fps)

    #drawing background 
    screen.blit(bg2,(0,0))
    birdgroup.draw(screen)
    birdgroup.update()
    pipegroup.draw(screen)
        
    #drawing ground
    screen.blit(ground,(gamescroll,500))

    if startscreen:
        # Draw start button
        if startbutton.draw():
            startscreen = False
            flying = True
            flysfx.play(-1)
        drawtext("Click or press Space to Start", font1, black, screenwidth // 2 - 170, screenheight // 2 - 150)
    


        

    #scoring
    if len(pipegroup) > 0:
        if birdgroup.sprites()[0].rect.left > pipegroup.sprites()[0].rect.left\
        and birdgroup.sprites()[0].rect.right < pipegroup.sprites()[0].rect.right\
        and pipepass == False:
            pipepass = True
        if pipepass == True:
            if birdgroup.sprites()[0].rect.left > pipegroup.sprites()[0].rect.right:
                score += 1
                pipepass = False
                scoresfx.set_volume(0.3)
                scoresfx.play()
    if startscreen == False:
        drawtext(f"Score: {score}", font2, black, 10, 20)
        drawtext(f"Highscore: {highscore}", font2, black, 400, 20)





    #for hitting the pipe
    if pygame.sprite.groupcollide(birdgroup, pipegroup, False, False) or flappy.rect.top < 0:
        gameover = True
        
        
        

    #for hitting the ground
    if flappy.rect.bottom > 500:
        gameover = True
        flying = False
        flysfx.stop()
        

    

    if gameover == False and flying == True:
        #scrolling pipe 
        timenow = pygame.time.get_ticks()
        if timenow - lastpipe > pipefreq:
            pipeheight = random.randint(-75, 75)
            btmpipe = Pipe(screenwidth +100, int(screenheight/2) + pipeheight, -1)
            toppipe = Pipe(screenwidth +100, int(screenheight/2) + pipeheight, 1)
            pipegroup.add(btmpipe)
            pipegroup.add(toppipe)

            lastpipe = timenow

        # scrolling ground
        
        gamescroll -= scrollspeed
        if abs(gamescroll) > 35 :
            gamescroll = 0

        pipegroup.update()


    if gameover == True:
        if not hitplayed:
         hitsfx.play()
         hitplayed = True
        
        restart_pressed = button.draw()
        keys = pygame.key.get_pressed()
        drawtext("Click or press Enter to Restart", font1, black, screenwidth//2 -150 , screenheight//2 +50)
        if restart_pressed or keys[K_RETURN]:
            gameover = False
            flying = False
            if score > highscore:
                highscore = score
                with open("highscore.txt", "w") as file:
                    file.write(str(highscore))
            score = resetgame()
            hitplayed = False





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flysfx.set_volume(1)
            flysfx.play(-1)
            flying = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and flying == False and gameover == False:
            flysfx.set_volume(1)
            flysfx.play(-1)
            flying = True 
            startscreen = False
            
            



    pygame.display.update()

pygame.mixer.quit()    
pygame.quit()


