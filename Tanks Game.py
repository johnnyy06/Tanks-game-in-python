import pygame
import random
import time
import os
import sys

# screen dimensions
WIN_WIDTH = 1000
WIN_HEIGHT = 800

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Tanks")

icon = pygame.image.load(os.path.join('images','icon.jpg'))
pygame.display.set_icon(icon)

pygame.init()

# colors array
colors = [
    (0, 0, 0), #0 colors[0]
    (255, 255, 255), #1 colors[1]
    (200, 0, 0), #2 RED
    (200, 200, 0), #3 YELLOW
    (34, 177, 76), #4 GREEN
    (190, 169, 255), #5 PAUSE MENU COLOR
    (102, 145, 60), #6 PALE GREEN 
    (255, 255, 102), #7 LIGHT YELLOW
    (102, 255, 102), #8 LIGHT GREEN
    (255, 102, 102), #9 LIGHT RED
    (255, 153, 0), #10 EXPLODE 1
    (255, 102, 0), #11 EXPLODE 2
    (255, 204, 0), #12 EXPLODE 3
    (255, 204, 153), #13 EXPLODE 4
    (255, 128, 0) #14 POWER BAR
]

# tanks dimensions and colors
tankupper = (0, 165, 92)
tankrect = (0, 252, 169)
tankwheels = (0, 165, 92)
tankbottom = (0, 165, 92)

e_tankupper = (204, 0, 0)
e_tankrect = (255, 51, 51)
e_tankwheels = (204, 0, 0)
e_tankbottom = (204, 0, 0)

tankWidth = 40
tankHeight = 20

turretWidth = 5
wheelWidth = 5

# sounds
boom_sound = pygame.mixer.Sound('explosion1.wav')
shot_sound = pygame.mixer.Sound('shot.wav')
movement_sound = pygame.mixer.Sound('tank_movement.wav')

# fonts for text
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("Yu Mincho Demibold", 85)
vsmallfont = pygame.font.SysFont("Yu Mincho Demibold", 25)

# initializing clock
CLOCK = pygame.time.Clock()

# battle field components
ground = pygame.image.load(os.path.join('images', 'ground.png'))
ground_rect = ground.get_rect()

sky = pygame.image.load(os.path.join('images', 'imag2.png'))

wall_1 = pygame.image.load(os.path.join('images', 'wall.png'))
wall_1_rect = wall_1.get_rect()
wall_2 = pygame.image.load(os.path.join('images', 'wall.png'))
wall_2_rect = wall_2.get_rect()
wall_3 = pygame.image.load(os.path.join('images', 'wall.png'))
wall_3_rect = wall_3.get_rect()

def battle_field():
        WIN.blit(sky, (-400,0))
        WIN.blit(ground,(0,650))
        WIN.blit(wall_1, (450, 608))
        WIN.blit(wall_2, (450, 545))
        WIN.blit(wall_3, (450, 481))



def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    if size == "vsmall":
        textSurface = vsmallfont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(WIN_WIDTH / 2), int(WIN_HEIGHT / 2) + y_displace)
    WIN.blit(textSurf, textRect)

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="vsmall"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    WIN.blit(textSurf, textRect)

def game_controls():
    gcont = True

    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill(colors[0])
        message_to_screen("Controls", colors[1], -100, size="large")
        message_to_screen("Fire: Spacebar", colors[6], -30)
        message_to_screen("Move Turret: Up and Down arrows", colors[6], 10)
        message_to_screen("Move Tank: Left and Right arrows", colors[6], 50)
        message_to_screen("Press D to raise power  AND Press A to lower power  ", colors[6], 140)
        message_to_screen("Pause: P", colors[6], 90)

        button("Play", 250, 620, 100, 50, colors[4], colors[8], action="play")
        button("Main", 450, 620, 100, 50, colors[3], colors[7], action="main")
        button("Quit", 650, 620, 100, 50, colors[2], colors[9], action="quit")

        pygame.display.update()

        CLOCK.tick(15)

def pause():
    paused = True
    message_to_screen("Paused", colors[5], -100, size="large")
    message_to_screen("Press C to continue playing or Q to quit", colors[6], 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        CLOCK.tick(5)

def button(text, x, y, width, height, inactive_color, active_color, action=None,size=" "):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(WIN, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "controls":
                game_controls()

            if action == "play":
                GameLoop()

            if action == "main":
                game_intro()

    else:
        pygame.draw.rect(WIN, inactive_color, (x, y, width, height))

    text_to_button(text, colors[0], x, y, width, height)

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:

                    pygame.quit()
                    quit()
        WIN.fill(colors[0])
        message_to_screen("Welcome to Tanks!", colors[5], -100, size="large")
        message_to_screen("Shoot and destroy the enemy tank", colors[6], 15)
        message_to_screen("before they destroy you.", colors[6], 60)        

        button("Play", 230, 600, 100, 50, colors[6], colors[8], action="play",size="vsmall")
        button("Controls", 430, 600, 100, 50, colors[6], colors[7], action="controls",size="vsmall")
        button("Quit", 630, 600, 100, 50, colors[6], colors[9], action="quit",size="vsmall")

        pygame.display.update()
        CLOCK.tick(15)



def fireShell(xy, tankx, tanky, turPos, gun_power, wall_location, wall_width, wall_height, enemyTankX, enemyTankY):
    fire = True
    damage = 0

    startingShell = list(xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(WIN, colors[10], (startingShell[0], startingShell[1]), 5)

        startingShell[0] -= (12 - turPos) * 2

        startingShell[1] += int(
            (((startingShell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (turPos + turPos / (12 - turPos)))

        if startingShell[1] > WIN_HEIGHT - 100:
            hit_x = int((startingShell[0] * WIN_HEIGHT - 200) / startingShell[1])
            hit_y = int(WIN_HEIGHT - 150)

            if enemyTankX + 10 > hit_x > enemyTankX - 10:
                damage = 25
            elif enemyTankX + 12 > hit_x > enemyTankX - 12:
                damage = 21
            elif enemyTankX + 15 > hit_x > enemyTankX - 15:
                damage = 18
            elif enemyTankX + 18 > hit_x > enemyTankX - 18:
                damage = 15
            elif enemyTankX + 25 > hit_x > enemyTankX - 25:
                damage = 10
            elif enemyTankX + 28 > hit_x > enemyTankX - 28:
                damage = 8
            elif enemyTankX + 35 > hit_x > enemyTankX - 35:
                damage = 5

            boom_sound.play()
            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = startingShell[0] <= wall_location + wall_width
        check_x_2 = startingShell[0] >= wall_location

        check_y_1 = startingShell[1] <= WIN_HEIGHT
        check_y_2 = startingShell[1] >= WIN_HEIGHT - wall_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            explosion(hit_x, hit_y)
            fire = False

        pygame.display.update()
        CLOCK.tick(60)
    return damage

def e_fireShell(xy, tankx, tanky, turPos, gun_power, wall_location, wall_width, wall_height, ptankx, ptanky):
    damage = 0
    currentPower = 1
    power_found = False

    while not power_found:
        currentPower += 1
        if currentPower > 100:
            power_found = True

        fire = True
        startingShell = list(xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            startingShell[0] += (12 - turPos) * 2
            startingShell[1] += int(
                (((startingShell[0] - xy[0]) * 0.015 / (currentPower / 50)) ** 2) - (turPos + turPos / (12 - turPos)))

            if startingShell[1] > WIN_HEIGHT - ground_rect.h:
                hit_x = int((startingShell[0] * WIN_HEIGHT - ground_rect.h) / startingShell[1])
                hit_y = int(WIN_HEIGHT - ground_rect.h)
                if ptankx + 15 > hit_x > ptankx - 15:
                    power_found = True
                fire = False

            check_x_1 = startingShell[0] <= wall_location + wall_width
            check_x_2 = startingShell[0] >= wall_location

            check_y_1 = startingShell[1] <= WIN_HEIGHT
            check_y_2 = startingShell[1] >= WIN_HEIGHT - wall_height

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int((startingShell[0]))
                hit_y = int(startingShell[1])
                fire = False

    fire = True
    startingShell = list(xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.draw.circle(WIN, colors[10], (startingShell[0], startingShell[1]), 5)

        startingShell[0] += (12 - turPos) * 2

        gun_power = random.randrange(int(currentPower * 0.90), int(currentPower * 1.10))

        startingShell[1] += int(
            (((startingShell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (turPos + turPos / (12 - turPos)))

        if startingShell[1] > WIN_HEIGHT - 100:
            hit_x = int((startingShell[0] * WIN_HEIGHT + 100) / startingShell[1]) - 120
            hit_y = int(WIN_HEIGHT - 150)
         

            if ptankx + 10 > hit_x > ptankx - 10:
                damage = 25
            elif ptankx + 15 > hit_x > ptankx - 15:
                damage = 18
            elif ptankx + 25 > hit_x > ptankx - 25:
                damage = 10
            elif ptankx + 35 > hit_x > ptankx - 35:
                damage = 5

            boom_sound.play()
            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = startingShell[0] <= wall_location + wall_width
        check_x_2 = startingShell[0] >= wall_location

        check_y_1 = startingShell[1] <= WIN_HEIGHT
        check_y_2 = startingShell[1] >= WIN_HEIGHT - wall_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            explosion(hit_x, hit_y)
            fire = False

        pygame.display.update()
        CLOCK.tick(60)
    return damage

def explosion(x, y, size=50):
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        startPoint = x, y

        colorChoices = [colors[10], colors[11], colors[12], colors[13]]

        magnitude = 1

        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1 * magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)

            pygame.draw.circle(WIN, colorChoices[random.randrange(0, 4)], (exploding_bit_x, exploding_bit_y),
                               random.randrange(1, 5))
            magnitude += 1

            pygame.display.update()
            CLOCK.tick(120)

        explode = False



def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = colors[4]
    elif player_health > 50:
        player_health_color = colors[3]
    else:
        player_health_color = colors[2]

    if enemy_health > 75:
        enemy_health_color = colors[4]
    elif enemy_health > 50:
        enemy_health_color = colors[3]
    else:
        enemy_health_color = colors[2]

    pygame.draw.rect(WIN, player_health_color, (860, 20, player_health, 40))
    pygame.draw.rect(WIN, enemy_health_color, (40, 20, enemy_health, 40))



def tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x - 27, y - 2),
                       (x - 26, y - 5),
                       (x - 25, y - 8),
                       (x - 24, y - 10),
                       (x - 23, y - 12),
                       (x - 20, y - 14),
                       (x - 18, y - 15),
                       (x - 15, y - 17),
                       (x - 13, y - 19),
                       (x - 11, y - 21)
                       ]

    pygame.draw.circle(WIN, tankupper, (x, y), int(tankHeight / 2))
    pygame.draw.rect(WIN, tankrect, (x - tankHeight, y, tankWidth, tankHeight))

    pygame.draw.line(WIN, tankupper, (x, y), possibleTurrets[turPos], turretWidth)

    pygame.draw.circle(WIN, tankbottom, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(WIN, tankbottom, (x - 10, y + 20), wheelWidth)

    pygame.draw.circle(WIN, tankbottom, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(WIN, tankbottom, (x - 10, y + 20), wheelWidth)
    pygame.draw.circle(WIN, tankbottom, (x - 5, y + 20), wheelWidth)
    pygame.draw.circle(WIN, tankbottom, (x, y + 20), wheelWidth)
    pygame.draw.circle(WIN, tankbottom, (x + 5, y + 20), wheelWidth)
    pygame.draw.circle(WIN, tankbottom, (x + 10, y + 20), wheelWidth)
    pygame.draw.circle(WIN, tankbottom, (x + 15, y + 20), wheelWidth)

    return possibleTurrets[turPos]

def enemy_tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x + 27, y - 2),
                       (x + 26, y - 5),
                       (x + 25, y - 8),
                       (x + 24, y - 10),
                       (x + 23, y - 12),
                       (x + 20, y - 14),
                       (x + 18, y - 15),
                       (x + 15, y - 17),
                       (x + 13, y - 19),
                       (x + 11, y - 21)
                       ]

    pygame.draw.circle(WIN, e_tankupper, (x, y), int(tankHeight / 2))
    pygame.draw.rect(WIN, e_tankrect, (x - tankHeight, y, tankWidth, tankHeight))

    pygame.draw.line(WIN, e_tankupper, (x, y), possibleTurrets[turPos], turretWidth)

    pygame.draw.circle(WIN, e_tankbottom, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(WIN, e_tankbottom, (x - 10, y + 20), wheelWidth)

    pygame.draw.circle(WIN, e_tankbottom, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(WIN, e_tankbottom, (x - 10, y + 20), wheelWidth)
    pygame.draw.circle(WIN, e_tankbottom, (x - 5, y + 20), wheelWidth)
    pygame.draw.circle(WIN, e_tankbottom, (x, y + 20), wheelWidth)
    pygame.draw.circle(WIN, e_tankbottom, (x + 5, y + 20), wheelWidth)
    pygame.draw.circle(WIN, e_tankbottom, (x + 10, y + 20), wheelWidth)
    pygame.draw.circle(WIN, e_tankbottom, (x + 15, y + 20), wheelWidth)

    return possibleTurrets[turPos]

def power(level):
    pygame.draw.rect(WIN, colors[14], (400, 40, level*2, 40))
    text = smallfont.render("Power: " + str(level) + "%", True, colors[0])
    WIN.blit(text, [WIN_WIDTH / 2.4, 0])

def fuel(tank_fuel):
    text = smallfont.render("Moves: " + str(tank_fuel), True, colors[0])
    WIN.blit(text, [WIN_WIDTH / 1.5, 0])


def game_over():
    game_over = True

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill(colors[0])
        message_to_screen("Game Over", colors[1], -100, size="large")
        message_to_screen("You died.", colors[6], -30)

        button("Play Again", 250, 500, 150, 50, colors[6], colors[8], action="play")
        button("Controls", 450, 500, 100, 50, colors[6], colors[7], action="controls")
        button("Quit", 650, 500, 100, 50, colors[6], colors[9], action="quit")

        pygame.display.update()

        CLOCK.tick(15)

def you_win():
    win = True

    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill(colors[0])
        message_to_screen("You won!", colors[1], -100, size="large")
        message_to_screen("Congratulations!", colors[6], -30)

        button("Play Again", 250, 500, 150, 50, colors[6], colors[8], action="play")
        button("Controls", 475, 500, 100, 50, colors[6], colors[7], action="controls")
        button("Quit", 650, 500, 100, 50, colors[6], colors[9], action="quit")

        pygame.display.update()

        CLOCK.tick(15)



def GameLoop():
    run = True
    gameOver = False
    FPS = 15

    player_health = 100
    enemy_health = 100

    wall_width = wall_3_rect.w

    mainTankX = WIN_WIDTH * 0.9
    mainTankY = WIN_HEIGHT * 0.81
    tankMove = 0
    currentTurPos = 0
    changeTur = 0

    enemyTankX = WIN_WIDTH * 0.1
    enemyTankY = WIN_HEIGHT * 0.81

    tank_fuel = 4

    fire_power = 50
    power_change = 0

    wall_location = 450
    wall_height = 320

    while run:
        if gameOver == True:
            message_to_screen("Game Over!", colors[2], -50, size="large")
            message_to_screen("Press C to play again or Q to exit", colors[0], 50)
            pygame.display.update()
            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        gameOver = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            GameLoop()
                        elif event.key == pygame.K_q:
                            run = False
                            gameOver = False
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and tank_fuel > 0:
                    movement_sound.play()
                    tankMove = -5
                    tank_fuel -= 1

                elif event.key == pygame.K_RIGHT and tank_fuel>0:
                    movement_sound.play()
                    tankMove = 5
                    tank_fuel -= 1

                elif event.key == pygame.K_UP:
                    changeTur = 1

                elif event.key == pygame.K_DOWN:
                    changeTur = -1

                elif event.key == pygame.K_p:
                    pause()

                elif event.key == pygame.K_SPACE:

                    shot_sound.play()
                    damage = fireShell(gun, mainTankX, mainTankY, currentTurPos, fire_power, wall_location, wall_width,
                                       wall_height, enemyTankX, enemyTankY)
                    enemy_health -= damage

                    possibleMovement = ['front', 'rear']
                    moveIndex = random.randrange(0, 2) #picks front or rear, where the enemy tank should move (random)

                    for x in range(random.randrange(0, 10)):

                        if WIN_WIDTH * 0.3 > enemyTankX > WIN_WIDTH * 0.03:
                            if possibleMovement[moveIndex] == "front":
                                enemyTankX += 5
                            elif possibleMovement[moveIndex] == "rear":
                                enemyTankX -= 5


                            battle_field()
                            health_bars(player_health, enemy_health)
                            gun = tank(mainTankX, mainTankY, currentTurPos)
                            enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
                            fire_power += power_change

                            power(fire_power)

                            pygame.display.update()

                            CLOCK.tick(FPS)

                    shot_sound.play()
                    damage = e_fireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, wall_location, wall_width,
                                         wall_height, mainTankX, mainTankY)
                    player_health -= damage

                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    movement_sound.stop()
                    tankMove = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0

                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0

        mainTankX += tankMove

        currentTurPos += changeTur

        if currentTurPos > 9:
            currentTurPos = 9
        elif currentTurPos < 0:
            currentTurPos = 0

        if mainTankX - (tankWidth / 2) < wall_location + wall_width:
            mainTankX += 5

        battle_field()
        health_bars(player_health, enemy_health)
        gun = tank(mainTankX, mainTankY, currentTurPos)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)

        fire_power += power_change

        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1

        power(fire_power)
        fuel(tank_fuel)

        pygame.display.update()

        if player_health < 1:
            game_over()
        elif enemy_health < 1:
            you_win()
        CLOCK.tick(FPS)

    pygame.quit()
    quit()

game_intro()
GameLoop()