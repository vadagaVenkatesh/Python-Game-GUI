import math
import random
import pygame


# manually Intialization the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('spaceimage.png')

# Caption and Icon
pygame.display.set_caption("Space Invader")
Icon = pygame.image.load('devil-32.png')
pygame.display.set_icon(Icon)

# Player
playerImg = pygame.image.load('spaceshuttle.png')
player_X = 370
player_Y = 480
player_X_change = 0

# Enemy
enemy_Img = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemy_Y_change = []
enemy_count = 11

for i in range(enemy_count):
    enemy_Img.append(pygame.image.load('enemy.png'))
    enemy_X.append(random.randint(0, 750))
    enemy_Y.append(random.randint(50, 100))
    enemyX_change.append(5)
    enemy_Y_change.append(45)

# Bullet

# Ready - loaded
# Fire - move bullet

bulletImg = pygame.image.load('bullet.png')
bullet_X = 0
bullet_Y = 480
bullet_X_change = 0
bullet_Y_change = 10
bullet_state = "ready"

# Score

scored = 0
font = pygame.font.Font('freesansbold.ttf', 32)

testX = 10
testY = 10

# Game Over
font_basic= pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(scored), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font_basic.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_Img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 15, y + 11))

class collisionCheck:

    def isCollision(enemy_X, enemy_Y, bullet_X, bullet_Y) :
        distance = math.sqrt(math.pow(enemy_X - bullet_X, 2) + (math.pow(enemy_Y - bullet_Y, 2)))
        if distance < 27:
            return True
        else:
            return False


# Main Game Loop
keeprunning = True
while keeprunning:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keeprunning = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_X_change = -5
            if event.key == pygame.K_RIGHT:
                player_X_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":


                    # Get the current x coordinate of the spaceship
                    bullet_X = player_X
                    fire_bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_X_change = 0

    #player boundaries

    player_X += player_X_change
    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736

    # Enemy Movement
    for i in range(enemy_count):

        # Game Over condition
        if enemy_Y[i] > 440:
            for j in range(enemy_count):
                enemy_Y[j] = 2000
            game_over_text()
            break
        #enemy boundary
        enemy_X[i] += enemyX_change[i]
        if enemy_X[i] <= 0:
            enemyX_change[i] = 4
            enemy_Y[i] += enemy_Y_change[i]
        elif enemy_X[i] >= 750:
            enemyX_change[i] = -4
            enemy_Y[i] += enemy_Y_change[i]

        # call class Collision
        collision = collisionCheck.isCollision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if collision:

            bullet_Y = 480
            bullet_state = "ready"
            scored += 1
            enemy_X[i] = random.randint(0, 736)
            enemy_Y[i] = random.randint(50, 150)

        enemy(enemy_X[i], enemy_Y[i], i)

    # Bullet Movement
    if bullet_Y <= 0:
        bullet_Y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_change

    player(player_X, player_Y)
    show_score(testX, testY)
    pygame.display.update()

    #refrences in ppt