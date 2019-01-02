import pygame, os, math
from pygame.locals import *

WIDTH, HEIGHT = 600, 600
BACKGROUND = (105, 105, 105)
FRAMERATE = 60

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage('paddle.png')
        self.rect.x = 250
        self.rect.y = 550
        self.speed = 5

    def moveLeft(self):
        self.rect.x -= self.speed

    def moveRight(self):
        self.rect.x += self.speed

    def checkRestrictions(self):
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)

    def update(self):
        self.checkRestrictions()

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage('brick.png')
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage('ball.png')
        self.rect.x = 285
        self.rect.y = 300
        self.speed = 3
        self.angle = 0

    def move(self):
        self.rect.y += self.speed

    def update(self):
        self.move()

def getEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key = pygame.key.get_pressed()
    if key[K_LEFT]:
        paddle.moveLeft()
    if key[K_RIGHT]:
        paddle.moveRight()

def draw():
    screen.fill(BACKGROUND)
    paddleSprites.draw(screen)
    brickSprites.draw(screen)
    ballSprites.draw(screen)
    paddleSprites.update()
    brickSprites.update()
    ballSprites.update()
    pygame.display.flip()

def setupBricks():
    rowAmount = 7
    colAmount = 5
    rowGap = 80
    colGap = 25
    xStart = 20
    x = 20
    y = 10
    brickSprites = pygame.sprite.RenderPlain()
    for col in range(colAmount):
        for row in range(rowAmount):
            brick = Brick(x, y)
            brickSprites.add((brick))
            x += rowGap
        x = xStart
        y += colGap
    return brickSprites

def collisionCheck():
    if pygame.sprite.groupcollide(paddleSprites, ballSprites, 0, 0):
        ball.speed *= -1
    if pygame.sprite.groupcollide(brickSprites, ballSprites, 1, 0):
        ball.speed *= -1

def loadImage(name, colorkey=None):
    fullname = os.path.join('graphics', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND)
    paddle = Paddle()
    paddleSprites = pygame.sprite.RenderPlain((paddle))
    ball = Ball()
    ballSprites = pygame.sprite.RenderPlain((ball))
    brickSprites = setupBricks()
    clock = pygame.time.Clock()
    while True:
        clock.tick(FRAMERATE)
        getEvents()
        draw()
        collisionCheck()
