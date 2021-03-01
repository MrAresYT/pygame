import math
import random

import pygame
from pygame import mixer

# ИНициализация
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("music.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemy_X = []
enemy_Y = []
enemy_X_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemy_X.append(random.randint(0, 736))
    enemy_Y.append(random.randint(50, 150))
    enemy_X_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

HeroImg = pygame.image.load('bullet.png')
HeroX = 0
HeroY = 480
HeroX_change = 0
HeroY_change = 10
Hero_state = "ready"

# Score

score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_sc(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global Hero_state
    Hero_state = "fire"
    screen.blit(HeroImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if Hero_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    HeroX = playerX
                    fire_bullet(HeroX, HeroY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemy_Y[i] > 440:
            for j in range(num_of_enemies):
                enemy_Y[j] = 2000
            game_over_text()
            break

        enemy_X[i] += enemy_X_change[i]
        if enemy_X[i] <= 0:
            enemy_X_change[i] = 4
            enemy_Y[i] += enemyY_change[i]
        elif enemy_X[i] >= 736:
            enemy_X_change[i] = -4
            enemy_Y[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemy_X[i], enemy_Y[i], HeroX, HeroY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            HeroY = 480
            Hero_state = "ready"
            score_val += 1
            enemy_X[i] = random.randint(0, 736)
            enemy_Y[i] = random.randint(50, 150)

        enemy(enemy_X[i], enemy_Y[i], i)

    # Bullet Movement
    if HeroY <= 0:
        HeroY = 480
        Hero_state = "ready"

    if Hero_state is "fire":
        fire_bullet(HeroX, HeroY)
        HeroY -= HeroY_change

    player(playerX, playerY)
    show_sc(textX, testY)
    pygame.display.update()
