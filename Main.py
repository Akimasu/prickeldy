import pygame
from pygame.locals import *
import pygame.gfxdraw
import sys
import time
from random import randint
import pandas as pd
import csv


#Setting
pygame.init()
pygame.mixer.quit()
SCREEN_WIDTH_Complete, SCREEN_HEIGHT = 800,600
screen = pygame.display.set_mode((SCREEN_WIDTH_Complete, SCREEN_HEIGHT))#, FULLSCREEN
SCREEN_WIDTH = SCREEN_WIDTH_Complete - 150
SCREEN_WIDTH_Complete = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
pygame.display.set_caption('Berry Buster')
clock = pygame.time.Clock()

#init
panel_x = 0
panel_y = SCREEN_HEIGHT*5.05/6
panel_width = SCREEN_WIDTH*9/63
panel_half_width = panel_width/2
panel_height = SCREEN_HEIGHT*1/60
panel_vel = 7
n_text = 0

# Main colors
PANEL_COLOR = (40, 30, 10)
BACK_COLOR = (90, 150, 70)
BALL_COLOR = (255, 0, 0)

# Some fonts
pygame.font.init()  # you have to call this at the start,
myfont = pygame.font.SysFont('Lobster Two', 30)

#Scores
score_pos = (SCREEN_WIDTH_Complete*(7.2/8), (SCREEN_HEIGHT-450))
mold_score_pos = (SCREEN_WIDTH_Complete*(7.2/8), (SCREEN_HEIGHT-260))

# Raspberry Images
rasperry_image = pygame.image.load("image/00 rasperry.png").convert()
transColor = rasperry_image.get_at((0, 0))
rasperry_image.set_colorkey(transColor)
rasperry_image = pygame.transform.scale(rasperry_image,(45, 45))

rasperry_image_2 = pygame.image.load("image/02 rasperry.png").convert()
transColor = rasperry_image_2.get_at((0, 0))
rasperry_image_2.set_colorkey(transColor)
rasperry_image_2 = pygame.transform.scale(rasperry_image_2,(45,45))

rasperry_image_4 = pygame.image.load("image/04 rasperry_gammel.png").convert()
transColor = rasperry_image_4.get_at((0, 0))
rasperry_image_4.set_colorkey(transColor)
rasperry_image_4 = pygame.transform.scale(rasperry_image_4,(45,45))



# restart after dying
def restart(current_score,restart_text):
    score(current_score)                                        # Add Score to Highscores
    screen.fill(pygame.Color(0, 0, 0))                          # Fill background with black
    re_image = pygame.image.load("image/Restart.png").convert() # Load Restart background
    re_image = pygame.transform.scale(re_image, (800, 600))     # Transform image to fit in screen
    screen.blit(re_image, [0, 0])  # Draw image

    text = myfont.render(restart_text, False, (50, 50, 50))
    screen.blit(text, (280, 300))

    key = pygame.key.get_pressed()                              # If Space gets pressed -> switch to menu
    if key[K_SPACE]:
        menu()

# function: defines how the panel moves
def panel_move():
    #Define panel movement
    global panel_x
    global panel_y
    key = pygame.key.get_pressed()
    if key[K_RIGHT]:
        if panel_x + panel_width <= SCREEN_WIDTH:
            panel_x += panel_vel
    if key[K_LEFT]:
        if panel_x >= 0:
            panel_x -= panel_vel

# defines features and methods for the ball used
class Ball:
    def __init__(self, rad = 5.0, pos_x = 150.0, pos_y = 150.0, diam = 11.0, vel_x = 0.0, vel_y = 5.0):
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.diam   = diam
        self.vel_x  = vel_x
        self.vel_y  = vel_y
        self.rad    = rad
        self.vel    = (vel_x**2 + vel_y**2)**(1/2)

    def move(self, panel_x, panel_y):
    # Define Ball movement
        global SCREEN_WIDTH; global SCREEN_HEIGHT
        global panel_width
        global panel_half_width

    # Rechter Rand
        if (self.pos_x + self.rad  >= SCREEN_WIDTH):
            self.vel_x = - self.vel_x   # Richtungswechsel: VZ pos_x

    # Linker Rand
        if self.pos_x - self.rad <= 0:
            self.vel_x = - self.vel_x

    # Oberer Rand
        if self.pos_y - self.rad <= 0:
            self.vel_y = - self.vel_y

    # Unterer Rand -> Quit
        #if (self.pos_y + self.rad >= panel_y + self.rad*20):
          #  restart()

    # Panel Collision
        if panel_y + self.vel_y >= self.pos_y + self.rad >= panel_y:
            if panel_x <= self.pos_x <= panel_x + panel_width:
                x_faktor = 8 * ((self.pos_x - panel_x - (panel_half_width)) / panel_width)
                self.vel_x = self.vel_x + x_faktor
                res_vel = (self.vel_x**2 + self.vel_y**2)**(1/2)
                vel_ratio = res_vel/ self.vel
                self.vel_x = self.vel_x / vel_ratio
                self.vel_y = -(self.vel_y / vel_ratio)

    # Brick Collision
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

# defines features of all Raspberries
class Rasperry:

    def __init__(self, pos_x, pos_y, rad):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rad = rad
        self.fall = False
        self.aussen = False
        #process_list = [(255, 182, 242), (255, 91, 185), (239, 0, 135)]
        #self.process = (random.choice(process_list))

    def r_fall(self):
        self.pos_y += 5

# defines starting conditions, so that the player doesn't continue the last game
def starting_phase(score_start,mold_score_start):
    list_rasp = []
    list_pos_rasp = []
    b1 = Ball()

# Kreiere Raspberries
    for i in range(0, 30):
        x = randint(1, 10)
        y = randint(1, 4)
        if (x, y) not in list_pos_rasp:
            list_pos_rasp.append((x, y))
            list_rasp.append(Rasperry(x * 60, 20 + y * 60, 23.5))

# Background green
    bg_image = pygame.image.load("image/background green score.png").convert()
    bg_image = pygame.transform.scale(bg_image, (800, 600))

# Foreground face
    fg_image = pygame.image.load("image/Background face only.png").convert()
    transColor = fg_image.get_at((0, 0))
    #transColor = (0, 255, 0)
    fg_image.set_colorkey(transColor)
    fg_image = pygame.transform.scale(fg_image, (800, 600))

# Rasperry
    global rasperry_image

# Tongue
    to_image = pygame.image.load("image/Zunge.png").convert()
    to_image.set_colorkey(transColor)
    to_image = pygame.transform.scale(to_image,(100,80))

    while True:
        msElapsed = clock.tick(100)
        screen.blit(bg_image, [0, 0])

    # Draw Raspberries
        for i in list_rasp:
            #pygame.draw.circle(screen, BALL_COLOR, (i.pos_x, i.pos_y), i.rad)
            screen.blit(rasperry_image, [i.pos_x-25, i.pos_y-30])


    #Panel and Ball
        panel_move()
        #pygame.draw.rect(screen, PANEL_COLOR, (panel_x, panel_y, panel_width, panel_height), 0)
        screen.blit(to_image, [panel_x-5, panel_y-5])
        b1.pos_x = panel_x + panel_half_width
        b1.pos_y = panel_y - 2 * b1.rad
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))
        #pygame.draw.circle(screen, BALL_COLOR2, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam), 3)

    # Draw Mouth
        screen.blit(fg_image, [0, 0])

    # Write score
        score = myfont.render( str(score_start), False, (200, 60, 100))
        screen.blit(score, score_pos)
        mold_score = myfont.render(str(mold_score_start), False, (80, 155, 220))
        screen.blit(mold_score, mold_score_pos)

        key = pygame.key.get_pressed()
        if key[K_BACKSPACE]:
            main_game(b1, list_rasp,rasperry_image,score_start,mold_score_start)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_q:
                    exit()
                if event.key == K_SPACE:
                    menu()

# saves new score in csv file
def score(current_score):
    score = float(current_score)
    r = csv.reader(open('score_list.csv'))
    lines = list(r)

    if float(lines[1][1]) <= score:
        for x in range(10, 1, -1):
            lines[x][1] = lines[x - 1][1]
        lines[1][1] = str(int(score))
    elif float(lines[1][1]) > score:
        for i in range(10, 1, -1):
            if float(lines[i][1]) < score:
                if float(lines[i - 1][1]) >= score:
                    for x in range(10, i, -1):
                        lines[x][1] = lines[x - 1][1]
                    lines[i][1] = str(int(score))

    writer = csv.writer(open('score_list.csv', 'w'))
    writer.writerows(lines)

# score menu to view top 10 highscores
def highscore_menu():
    screen.fill(pygame.Color(0, 0, 0))
    re_image = pygame.image.load("image/score2.png").convert()
    re_image = pygame.transform.scale(re_image, (800, 600))

    screen.blit(re_image, [0, 0])
    screen_r = screen.get_rect()

    r = csv.reader(open('score_list.csv'))
    lines = list(r)
    lines_list = ["1.     "+str(lines[1][1]) +"         6.     "+str(lines[6][1])," "
                    , "2.     "+str(lines[2][1]) +"         7.     "+str(lines[7][1]), " "
                    , "3.     "+str(lines[3][1]) +"         8.     "+str(lines[8][1]), " "
                    , "4.     "+str(lines[4][1]) +"         9.     "+str(lines[9][1]), " "
                    , "5.     " + str(lines[5][1]) +"          10.    "+str(lines[10][1])]

    font = pygame.font.SysFont('Lobster Two', 25)
    texts = []

    for i, line in enumerate(lines_list):
        s = font.render(line, 1, (50, 50, 50))
        r = s.get_rect(centerx=screen_r.centerx-20, y=200 + i * 20)
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        for r, s in texts:
            screen.blit(s, r)

        key = pygame.key.get_pressed()
        if key[K_SPACE]:
            menu()

        pygame.display.update()
        clock.tick(60)

# main game function
def main_game(b1, list_rasp,rasperry_image,score_start,mold_score_start):
# Background green
    bg_image = pygame.image.load("image/background green score.png").convert()
    bg_image = pygame.transform.scale(bg_image, (800, 600))

# Foreground face
    fg_image = pygame.image.load("image/Background face only.png").convert()
    transColor = fg_image.get_at((0, 0))
    fg_image.set_colorkey(transColor)
    fg_image = pygame.transform.scale(fg_image, (800, 600))

# Tongue
    to_image = pygame.image.load("image/Zunge.png").convert()
    to_image.set_colorkey(transColor)
    to_image = pygame.transform.scale(to_image,(100,80))

# Time
    gametime = 0
    end_time = 60
    mold_time = 20

    while True:
    # Set clock and measure time in seconds
        msElapsed = clock.tick(100)             # fps set on 60 frames for secondy
        gametime += msElapsed                   # Count While cycles to track time
        time_passed = round(gametime / 1000, 0) # save time in seconds (millisencondy times 1000)

    # Fill screen_ black
        screen.blit(bg_image, [0, 0])

    # Raspberries-Ball collision and fall
        # Check only for collision, if ball is under 320 pixel
        for i in list_rasp:                 # Check all raspberries
            # Check if distance between rasp. and ball is smaller than the sum of both radiuses
            if b1.pos_y < 300:
                if int((((b1.pos_x - i.pos_x)**2) + ((b1.pos_y - i.pos_y)**2))**(1/2)) <= i.rad + b1.rad:
                    i.fall = True
            # If collision, then let raspberries fall by function
            if i.fall == True:
                i.r_fall()
            # If raspberries fall over 600 pixel, the object gets removed from the list
            if i.pos_y > 600:
                list_rasp.remove(i)  # Remove Object i, if it's under y=600
                if time_passed <= mold_time:
                    score_start += 1
                else:
                    mold_score_start += 1

    # Rasperry: draw and mold
        # for each rasp, check time and update image after specific time passing
        for i in list_rasp:
            # pygame.draw.circle(screen, BALL_COLOR, (i.pos_x, i.pos_y), i.rad)
            if time_passed <= 10:
                screen.blit(rasperry_image, [i.pos_x - 25, i.pos_y - 30])
            elif 10 < time_passed <= mold_time:
                screen.blit(rasperry_image_2, [i.pos_x - 25, i.pos_y - 30])
            elif mold_time < time_passed <= end_time:
                screen.blit(rasperry_image_4, [i.pos_x - 25, i.pos_y - 30])

    # Panel
        panel_move()
        screen.blit(to_image, [panel_x-5, panel_y-5])

    # Ball: Draw and move ball via ball class function
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))
        b1.move(panel_x, panel_y)

    # Draw Mouth
        screen.blit(fg_image, [0, 0])

    # Write score
        score = myfont.render(str(score_start), False, (200, 60, 100))
        screen.blit(score, score_pos)
        mold_score = myfont.render(str(mold_score_start), False, (80, 155, 220))
        screen.blit(mold_score, mold_score_pos)

    # End game if ball is under the panel or more than 30s passed; Win game if all list_rasp is empty
        if 80 <= time_passed:
            current_score = score_start
            score_start = 0
            restart_text = ("Watch your time!")
            restart(current_score, restart_text)
        if not list_rasp:
            time.sleep(0.1)
            starting_phase(score_start, mold_score_start)
        if (b1.pos_y  >= panel_y + b1.rad + 10):
            current_score = score_start
            score_start = 0
            restart_text = ("Bye bye ball")
            restart(current_score,restart_text)
        if mold_score_start >= 10:
            current_score = score_start
            score_start = 0
            restart_text = ("molding death")
            restart(current_score, restart_text)

    # Update frames each run through
        pygame.display.update()

    # Quit game if x sign or esc is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    exit()
                if event.key == K_SPACE:
                    menu()

# credit menu
def credits():
    screen_r = screen.get_rect()
    font = pygame.font.SysFont('Lobster Two', 25, bold = True) #FreeMono

    credit_list = [ "BERRY BUSTER", " "," ","Developer - Rike & Jenny"
                    ," ", "Lead Graphic Designer - Rike & Jenny", " ","Graphic Designer - Rike & Jenny"," "
                    , "Menu System - Rike & Jenny", " ", "Music - Rike & Jenny", " ", "Motion Designer - Rike & Jenny"
                    , " ", " ", "Special Thanks to friends :)"]

    texts = []
    # Text rendering for efficiancy

    green = pygame.image.load("image/credits.png").convert()
    green = pygame.transform.scale(green, (800, 600))

    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (150, 30, 20))
        # we also create a Rect for each Surface.
        # whenever you use rects with surfaces, it may be a good idea to use sprites instead
        # we give each rect the correct starting position
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 30)
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        screen.blit(green, [0, 0])

        for r, s in texts:
            # now we just move each rect by one pixel each frame
            r.move_ip(0, -1)
            # and drawing is as simple as this
            screen.blit(s, r)

        # if all rects have left the screen, we exit
        if not screen_r.collidelistall([r for (r, _) in texts]):
            menu()

        key = pygame.key.get_pressed()
        if key[K_SPACE]:
            menu()

        # only call this once so the screen does not flicker
        pygame.display.update()

        # cap framerate at 60 FPS
        clock.tick(60)

# tutorial: instructions and how to play
def tutorial():
    gametime = 0
    list_tut = ["image/00 rasperry.png","image/02 rasperry.png", "image/03 rasperry.png", "image/01 rasperry.png"]
    lastclick = 0
    click = 0
    image = pygame.image.load(list_tut[click]).convert()  # Load Restart background
    image = pygame.transform.scale(image, (800, 600))  # Transform image to fit in screen


    while True:
        msElapsed = clock.tick(100)  # fps set on 60 frames for secondy
        gametime += msElapsed  # Count While cycles to track time
        screen.blit(image, [0, 0])

        key = pygame.key.get_pressed()  # If Space gets pressed -> switch to menu
        if key[K_1]:
            if lastclick + 1000 < gametime:
                lastclick = gametime
                click += 1
                if click == 4:
                    click = 0
                #screen.fill(pygame.Color(0, 0, 0))
                image = pygame.image.load(list_tut[click]).convert()  # Load Restart background
                image = pygame.transform.scale(image, (800, 600))  # Transform image to fit in screen


        key = pygame.key.get_pressed()                              # If Space gets pressed -> switch to menu
        if key[K_SPACE]:
            menu()

        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        pygame.display.update()

# menu: let's player choose between main game, credit, scores and quit
def menu():
    menu_image = pygame.image.load("image/menu.png").convert()
    menu_image = pygame.transform.scale(menu_image, (800, 600))

    score_start = 0
    mold_score_start = 0

    while True:
        screen.blit(menu_image, [0, 0])

        key = pygame.key.get_pressed()
        if key[K_s]:
            starting_phase(score_start,mold_score_start)

        if key[K_c]:
            credits()

        if key[K_r]:
            highscore_menu()

        if key[K_t]:
            tutorial()

        if key[K_q]:
            exit()


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()

# Welcome animation
def welcome_opening():
    global SCREEN_WIDTH_Complete
    width = SCREEN_WIDTH_Complete

    green_image = pygame.image.load("image/green.png").convert()
    green_image = pygame.transform.scale(green_image, (800, 600))

    rasperry_image_2 = pygame.image.load("image/02 rasperry.png").convert()
    transColor = rasperry_image_2.get_at((0, 0))
    rasperry_image_2.set_colorkey(transColor)
    rasperry_image_2 = pygame.transform.scale(rasperry_image_2, (45, 45))

    # Define falling raspberries
    r1 = Rasperry(20, -20, 23.5)
    r2 = Rasperry(50, -20, 23.5)
    r3 = Rasperry(150, -20, 23.5)
    r4 = Rasperry(300, -20, 23.5)
    r5 = Rasperry(450, -20, 23.5)
    r6 = Rasperry(620, -20, 23.5)
    r7 = Rasperry(760, -20, 23.5)

    gametime = 0
    time_passed = 550

    def anim_fall(rasp, time):
        if i >= time:
            rasp.fall = True
        if rasp.fall == True:
            rasp.r_fall()
        screen.blit(rasperry_image_2, [rasp.pos_x - 25, rasp.pos_y - 30])


    for i in range(0, time_passed):
        screen.fill((0, 0, 0))
        screen.blit(green_image, [0, 0])

        anim_fall(r1, 1)
        anim_fall(r2, 400)
        anim_fall(r3, 50)
        anim_fall(r4, 100)
        anim_fall(r5, 250)
        anim_fall(r6, 350)
        anim_fall(r7, 200)

        time.sleep(0.005)
        pygame.display.update()

    list_name = ["b", "e", "r", "r2", "y", "b2", "u", "s", "t", "e2", "r3"]
    for i in range(0, 11):
        image = ("image/"+str(list_name[i])+".png")
        image = pygame.image.load(image).convert()
        image = pygame.transform.scale(image, (800, 600))
        screen.blit(image, (0, 0))
        
        time.sleep(0.2)
        pygame.display.update()

    time.sleep(1)
    menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)


welcome_opening()



