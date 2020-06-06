import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Space Invaders')

icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')
background1 = pygame.image.load('background1.png')
background2 = pygame.image.load('background2.png')
background2_change = pygame.transform.scale(background2, (800, 600))

backgrounds = random.choice([background, background1, background2_change])

mixer.music.load('background.wav')
mixer.music.play(-1)

space_ship = pygame.image.load('space-invaders.png')
space_shipX = 380
space_shipY = 480
space_shipX_change = 0
space_shipY_change = 50


def print_space_ship():
    screen.blit(space_ship, (space_shipX, space_shipY))


enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemys = 5

for i in range(num_of_enemys):
    enemy.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 200))
    enemyX_change.append(-5)
    enemyY_change.append(60)


def print_enemy(x, y, i):
    screen.blit(enemy[i], (x, y))


bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = -10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


def cheak_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))))
    if distance <= 27:
        return True
    else:
        return False


score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def print_score(x, y):
    score_print = score_font.render("Score:" + str(score), True, (255, 255, 255))
    screen.blit(score_print, (x, y))


game_over = pygame.font.Font('freesansbold.ttf', 64)
fontX = 200
fontY = 270


def print_game_over():
    game_over_ = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_, (fontX, fontY))


running = True

while running:
    screen.fill((2, 2, 255))
    screen.blit(backgrounds, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                space_shipX_change = 6
            elif event.key == pygame.K_LEFT:
                space_shipX_change = -6
            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = space_shipX
                    fire_bullet(bulletX, bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                space_shipX_change = 0
            elif event.key == pygame.K_LEFT:
                space_shipX_change = 0

    for i in range(num_of_enemys):
        if enemyY[i] >= 440:
            for j in range(num_of_enemys):
                enemyX[j] = 2000
                enemyY[j] = 2000
                print_game_over()
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 5
            enemyX[i] += enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -5
            enemyX[i] += enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        collision = cheak_collision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            bulletY = 480
            bullet_state = "ready"
            enemy_sound = mixer.Sound('explosion.wav')
            enemy_sound.play()
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 200)
            score += 1

        print_enemy(enemyX[i], enemyY[i], i)

    space_shipX += space_shipX_change

    if space_shipX <= 0:
        space_shipX = 0
    elif space_shipX >= 736:
        space_shipX = 736

    elif bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    elif bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    print_space_ship()
    print_score(textX, textY)
    pygame.display.update()
