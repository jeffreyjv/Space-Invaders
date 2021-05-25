import pygame
import random
import math

# initializes the pygame
pygame.init()

# creation of screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('background.png')

# Title & Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('ufo.png'))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 150))
    alienX_change.append(1.2)
    alienY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = False

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_ren = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_ren, (200, 250))


def show_score(x, y):
    score_ren = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_ren, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = True
    # ensure bullet comes from center of spaceship
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(alienX, alienY, playerX, playerY):
    distance = math.sqrt((math.pow(alienX - playerX, 2)) + (math.pow(alienY - playerY, 2)))
    if distance <= 30:
        return True
    else:
        return False


# screen loop to keep window/game running
running = True
while running:
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movement
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -1
        if event.key == pygame.K_RIGHT:
            playerX_change = 1
        if event.key == pygame.K_UP:
            playerY_change = -1
        if event.key == pygame.K_DOWN:
            playerY_change = 1
        if event.key == pygame.K_SPACE:
            if bullet_state:
                bulletX = playerX
                screen.blit(bulletImg, (bulletX + 30, bulletY + 10))

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            playerY_change = 0

    # Spaceship boundary
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Alien movement
    for i in range(num_of_aliens):

        # GameOver
        if alienY[i] > 200:
            for j in range(num_of_aliens):
                alienY[j] = 1500
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 1.2
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -1.2
            alienY[i] += alienY_change[i]

        # collision
        collision = isCollision(alienX[i], alienY[i], playerX, playerY)
        if collision:
            score += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 0

    if bullet_state:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
