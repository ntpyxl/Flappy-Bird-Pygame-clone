import pygame
from sys import exit

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

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = birdImages[0]
        self.rect = self.image.get_rect()
        self.rect.center = birdStartPosition
        self.imageIndex = 0
        self.velocity = 0
        self.flap = False

    def update(self, userInput):
        # bird physics
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
        if userInput[pygame.K_SPACE] and not self.flap and self.rect.y > 0:
            self.flap = True
            self.velocity = -7

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
    # instantiate ground
    groundPosition_X, groundPosition_Y = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(groundPosition_X, groundPosition_Y))

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
        ground.draw(window)
        bird.draw(window)

        # update objects
        ground.update()
        bird.update(userInput)

        clock.tick(60) # limits game framerate to 60
        pygame.display.update()

main()
