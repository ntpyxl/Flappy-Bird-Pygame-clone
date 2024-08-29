import pygame
from sys import exit
import random

pygame.init()
clock = pygame.time.Clock() # allows to control game framerate

birdImages = [pygame.image.load("game assets/bird_up.png"),
              pygame.image.load("game assets/bird_mid.png"),
              pygame.image.load("game assets/bird_down.png")]
backgroundImage = pygame.image.load("game assets/background.png")
groundImage = pygame.image.load("game assets/ground.png")
topPipeImage = pygame.image.load("game assets/pipe_top.png")
bottomPipeImage = pygame.image.load("game assets/pipe_bottom.png")
gameOverImage = pygame.image.load("game assets/game_over.png")
startImage = pygame.image.load("game assets/start.png")

# game variables
windowHeight = 720
windowWidth = 551
window = pygame.display.set_mode((windowWidth, windowHeight))

scrollSpeed = 1
birdStartPosition = (100, 250)
playerScore = 0
font = pygame.font.SysFont('Segoe', 30)
gameStopped = True

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = birdImages[0]
        self.rect = self.image.get_rect()
        self.rect.center = birdStartPosition
        self.imageIndex = 0
        self.velocity = 0
        self.flap = False
        self.alive = True

    def update(self, userInput):
        # bird physics
        if self.alive:
            self.velocity += 0.5
        if self.velocity > 7:
            self.velocity = 7
        if self.rect.y < 500:
            self.rect.y += int(self.velocity)
        if self.velocity == 0: # player can't jump before reaching jump climax
            self.flap = False

        # animates the bird
        self.imageIndex += 1
        if self.imageIndex >= 30:
            self.imageIndex = 0
        self.image = birdImages[self.imageIndex // 10]
        self.image = pygame.transform.rotate(self.image, self.velocity * -7)

        # bird controls
        if userInput[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.velocity = -7

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipeType):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipeType = pipeType

    def update(self): 
        # animates the pipe motion
        self.rect.x -= scrollSpeed
        if self.rect.x <= -windowWidth:
            self.kill()

        # score system
        global playerScore
        if self.pipeType == "bottom":
            if birdStartPosition[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if birdStartPosition[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                playerScore += 1

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = groundImage
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self): # animates the ground motion
        self.rect.x -= scrollSpeed
        if self.rect.x <= -windowWidth:
            self.kill()

def quitGame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    global playerScore

    # instantiate ground
    groundPosition_X, groundPosition_Y = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(groundPosition_X, groundPosition_Y))

    # instantiate pipes
    pipeTimer = 0
    pipes = pygame.sprite.Group()
    
    #instantiate bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    while True: # loops every frame
        quitGame()
        
        userInput = pygame.key.get_pressed()

        window.blit(backgroundImage, (0, 0))

        if len(ground) <= 2: # continuously creates more ground at the right of the screen
            ground.add(Ground(windowWidth, groundPosition_Y))

        # draw objects
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        # score system
        scoreText = font.render("Score: " + str(playerScore), True, pygame.Color(255, 255, 255))
        window.blit(scoreText, (30, 30))

        # update objects
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(userInput)

        # collision detection
        pipeCollision = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        groundCollision = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if pipeCollision or groundCollision:
            bird.sprite.alive = False
            bird.sprite.velocity = 7
            if groundCollision:
                window.blit(gameOverImage, (windowWidth // 2 - gameOverImage.get_width() // 2,
                                            windowHeight // 2 - gameOverImage.get_height() // 2))
                if userInput[pygame.K_r]: # r key on keyboard
                    playerScore = 0
                    break

        # spawn pipes
        if pipeTimer <= 0 and bird.sprite.alive:
            PipesPosition_X = 550
            TopPipesPosition_Y = random.randint(-600, -480)
            BottomPipesPosition_Y = TopPipesPosition_Y + random.randint(90, 130) + bottomPipeImage.get_height()
            pipes.add(Pipe(PipesPosition_X, TopPipesPosition_Y, topPipeImage, "top"))
            pipes.add(Pipe(PipesPosition_X, BottomPipesPosition_Y, bottomPipeImage, "bottom"))
            pipeTimer = random.randint(180, 250)
        pipeTimer -= 1

        clock.tick(60) # limits game framerate to 60
        pygame.display.update()

# main menu
def menu():
    global gameStopped

    while gameStopped:
        quitGame()

        # draw the menu
        window.blit(backgroundImage, (0, 0))
        window.blit(groundImage, Ground(0, 520))
        window.blit(birdImages[0], (100, 250))
        window.blit(startImage, (windowWidth // 2 - startImage.get_width() // 2, 
                                 windowHeight // 2 - startImage.get_height() // 2))
        
        # user input
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_SPACE]:
            main()

        pygame.display.update()

menu()