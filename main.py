import pygame
from pygame import mixer
import random
import math

# IMPORTANT INFO
"""
Blit: blit means to draw an image of player onto screen. screen is surface of game
Global: Use global keyword so function can change variable that's out of its scope
pygame.display.update(): add after every game to update screen
"""

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Music
"""
put -1 so it plays on loop instead of just once

mixer.music for long sounds ex. background music
mixer.sound for short sounds ex. bullet
"""
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
"""
Ready - You can't see the bullet on the screen
Fire - The bullet is currently moving
"""
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = -1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('space_font.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('space_font.ttf', 64)
game_state = "continue"

# Explosion
explosionImg = pygame.image.load('explosion.png')
explosionY = 0
explosionX = 0

# Functions
"""
You render text first then blit it on the screen. You put True so it can show.
"""


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def explosion(x, y):
    screen.blit(explosionImg, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y)) # x+16, y+64


# use distance formula
def isCollision(aX, aY, bX, bY):
    distance = math.sqrt(math.pow((aX - bX), 2) + math.pow((aY - bY), 2))
    if distance < 27:
        return True
    return False


# Game Loop:
"""
Anything you want to be seen continuously must be placed inside the while loop.
Remember, Python executes top down.
"""
running = True
while running:

    # RGB of screen background
    screen.fill((63, 56, 168))

    # Background Image
    """
    Q: Why isn't is slower even though image is 886kb?
    If the image takes up a lot of space, each iteration may be slower.
    This means even  the enemy and player movement would be slower, so in that case, you'd have to increase their movements.
    """
    screen.blit(background, (0, 0))

    # Event for loop
    """
    This for-loop, loops through all the events.
    Event: anything happening inside game window like pressing keys, hitting the close button.
    
    The close button is a QUIT event
    pressed key(KEYDOWN), released key (KEYUP)
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3

            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3

            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                bulletX = playerX+16
                bulletY = playerY-64
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or pygame.K_DOWN:
                playerY_change = 0

    # Player Bounds and Movement
    playerX += playerX_change
    playerY += playerY_change
    if game_state is not "end":
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        if playerY <= 0:
            playerY = 0
        elif playerY >= 536:
            playerY = 536

    # Enemy Bounds and Movement
    for i in range(num_of_enemies):

        # Game Over
        player_collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)

        if enemyY[i] > 540:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        elif player_collision:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            explosionX = playerX
            explosionY = playerY
            playerY = 2000
            bullet_state = "over"
            game_state = "end"
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            explosion(explosionX, explosionY)
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision with bullet
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionX = enemyX[i]
            explosionY = enemyY[i]
            explosion_Sound = mixer.Sound('explosion.wav')
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            explosion_Sound.play()
            explosion(explosionX, explosionY)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    """
    Keeps the bullet on the screen after every iteration of while loop
    
    After bullet goes above screen, bullet_state resets.
    Then we can press Space again.
    """
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    # game_state
    if game_state is "end":
        explosion(explosionX,explosionY)

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()  # add after every game to update screen

# END OF GAME LOOP

"""
Contributions:
Freepik
Vitaly Gorbachev
Pixel Buddha
Smashicons
"""
