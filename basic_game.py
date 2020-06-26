import pygame
import sys

pygame.init()

#Variables
scWidth = 1280
scHeight = 640
clock = pygame.time.Clock()
score = 0
screen = pygame.display.set_mode((scWidth, scHeight))
pygame.display.set_caption("Game")

# Image loading


walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')

bg1 = pygame.image.load('bg.jpg')
character = pygame.image.load('standing.png')

bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.mp3')
#pygame.mixer.music.play(-1)


#Player Class
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60)

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y, 28, 60)
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    def hit(self):
        if self.isJump is True:
            self.isJump = False
        self.x = 60
        self.y = 505
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        screen.blit(text, ((scWidth - text.get_width())/2, scHeight/2))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

#Projectile Class
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

#class ground(object):
class background(object): #total of five images
    ground = [pygame.image.load('ground.png'), pygame.image.load('ground.png'), pygame.image.load('ground.png'), pygame.image.load('ground.png'), pygame.image.load('ground.png')]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

        self.screenCounter = 0

    def draw(self, screen):
        self.move()
        if self.screenCounter < 4:
            screen.blit(self.ground[self.screenCounter], (self.x, self.y))
            screen.blit(self.ground[self.screenCounter + 1], (scWidth + self.x, self.y))
        else:
            screen.blit(self.ground[self.screenCounter], (self.x,self.y))
            print(self.screenCounter)

    def move(self):
        if c.x > 950 and c.right is True and c.standing is False:
            self.x -= self.speed
            c.vel = 0
            goblin.vel = 8
            if self.x <= scWidth * -1:
                self.x = 0
        else:
            c.vel = self.speed
            goblin.vel = 4

#Enemy Class
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 4
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 10
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel < 0:
                screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10)*(10-self.health)), 10))
            self.hitbox = (self.x + 20, self.y, 28, 60)
        if self.x < 0:
            self.x = scWidth
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def move(self):
        self.x -= self.vel

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')


#Draw everything here
def redrawGameWindow():
    #screen.blit(bg, (0, 0))
    bg.draw(screen)
    #screen.blit(ground, (bgx,bgy))
    #screen.blit(ground1, (bg1x, bg1y))
    text = font.render(f"Score: {score}", 1, (0,0,0))
    screen.blit(text, (390, 10))
    c.draw(screen)
    goblin.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()

#variables for main loop
c = player(300, 505, 64, 64)
bg = background(0, 0)
game_over = False
bullets = []
goblin = enemy(scWidth, 505, 64, 64, 450)
shootLoop = 0
font = pygame.font.SysFont('comicsans', 30, True)
bgx = 0
bgy = 365
bg1x = scWidth - 1
bg1y = 365
move = 0
#mainloop
while not game_over:
    clock.tick(27)

    if c.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and c.hitbox[1] + c.hitbox[3] > goblin.hitbox[1]:
        if c.hitbox[0] + c.hitbox[2] > goblin.hitbox[0] and c.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            c.hit()
            score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                hitSound.play()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < scWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if c.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 6:
            bullets.append(projectile(round(c.x + c.width //2), round(c.y + c.height //2), 6, (0, 0, 0), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and c.x > c.vel:
        c.x -= c.vel
        c.left = True
        c.right = False
        c.standing = False
    elif keys[pygame.K_RIGHT] and c.x < scWidth - c.width - c.vel:
        c.x += c.vel
        c.right = True
        c.left = False
        c.standing = False
    else:
        c.standing = True
        c.walkCount = 0

    if not (c.isJump):
        if keys[pygame.K_UP]:
            c.isJump = True
            c.right = False
            c.left = False
            c.walkCount = 0
    else:
        if c.jumpCount >= -10:
            neg = 1
            if c.jumpCount < 0:
                neg = -1
            c.y -= (c.jumpCount ** 2) * 0.5 * neg
            c.jumpCount -= 1
        else:
            c.isJump = False
            c.jumpCount = 10
    redrawGameWindow()
