#!/usr/bin/env python
import pygame
from pygame.locals import *
import pygame.gfxdraw
import sys
import time
from random import randint


#Setting
pygame.init()
pygame.mixer.quit()
SCREEN_WIDTH_Complete, SCREEN_HEIGHT = 800,600
screen = pygame.display.set_mode((SCREEN_WIDTH_Complete, SCREEN_HEIGHT))#, FULLSCREEN
SCREEN_WIDTH = SCREEN_WIDTH_Complete - 150
SCREEN_WIDTH_Complete = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
pygame.display.set_caption('Brickledy Preake')
clock = pygame.time.Clock()

#init
panel_x = 0
panel_y = SCREEN_HEIGHT*5.05/6
panel_width = SCREEN_WIDTH*9/75
panel_half_width = panel_width/2
panel_height = SCREEN_HEIGHT*1/60
panel_vel = 7
n_text = 0
score_start = 0

#Farben
PANEL_COLOR = (40,30,10)
BACK_COLOR = (90,150,70)
BALL_COLOR = (255,0,0)

# Schreibkrams
pygame.font.init()  # you have to call this at the start,
myfont = pygame.font.SysFont('Lobster Two', 30)
score_pos = (SCREEN_WIDTH_Complete*(6.8/8), SCREEN_HEIGHT/3)

# Raspberry Images
rasperry_image = pygame.image.load("image/00 rasperry.png").convert()
transColor = rasperry_image.get_at((0, 0))
rasperry_image.set_colorkey(transColor)
rasperry_image = pygame.transform.scale(rasperry_image,(45,50))

rasperry_image_2 = pygame.image.load("image/02 rasperry.png").convert()
transColor = rasperry_image_2.get_at((0, 0))
rasperry_image_2.set_colorkey(transColor)
rasperry_image_2 = pygame.transform.scale(rasperry_image_2,(45,50))

rasperry_image_4 = pygame.image.load("image/04 rasperry.png").convert()
transColor = rasperry_image_4.get_at((0, 0))
rasperry_image_4.set_colorkey(transColor)
rasperry_image_4 = pygame.transform.scale(rasperry_image_4,(45,50))


def restart():
    screen.fill(pygame.Color(0, 0, 0))
    re_image = pygame.image.load("image/Restart.png").convert()
    re_image = pygame.transform.scale(re_image, (800, 600))
    screen.blit(re_image, [0, 0])
    #texts = [("You killed me"), ("I'm... dead"), ("Not again..."), ("Why ?"),
     #        ("Please let me live"), ("Bye bye")]
    #tr = random.choice(texts)
    #text_surface = myfont.render(tr, False, (50, 50, 50))
    #screen.blit(text_surface, (250, 300))
    # FOR und BREAK könnte gehen; return
    key = pygame.key.get_pressed()
    if key[K_SPACE]:
        menu()


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


class Ball:
    def __init__(self, rad = 5.0, pos_x = 150.0, pos_y = 150.0, diam = 10.0, vel_x = 0.0, vel_y = 5.0):
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


def starting_phase():
    list_rasp = []
    list_pos_rasp = []
    b1 = Ball()

# Kreiere Raspberries
    for i in range(0, 30):
        x = randint(1, 11)
        y = randint(1, 3)
        if list_pos_rasp.count != (x, y):
            list_pos_rasp.append((x, y))
            list_rasp.append(Rasperry(x * 50, y * 75, 20))

# Background green
    bg_image = pygame.image.load("image/Background green only.png").convert()
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

# Score
    global score_start

    while True:
        msElapsed = clock.tick(100)
        screen.blit(bg_image, [0, 0])

    # Draw Raspberries
        for i in list_rasp:
            #pygame.draw.circle(screen, BALL_COLOR, (i.pos_x, i.pos_y), i.rad)
            screen.blit(rasperry_image, [i.pos_x-25, i.pos_y-30])


    #Panel and Ball
        panel_move()
        pygame.draw.rect(screen, PANEL_COLOR, (panel_x, panel_y, panel_width, panel_height), 0)
        screen.blit(to_image, [panel_x-8, panel_y-5])
        b1.pos_x = panel_x + panel_half_width
        b1.pos_y = panel_y - 2 * b1.rad
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))

    # Draw Mouth
        screen.blit(fg_image, [0, 0])

    # Write score
        score = myfont.render("Score:" + str(score_start), False, (150, 50, 50))
        screen.blit(score, score_pos)

        key = pygame.key.get_pressed()
        if key[K_BACKSPACE]:
            main_game(b1, list_rasp,rasperry_image)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()


def main_game(b1, list_rasp,rasperry_image):
# Background green
    bg_image = pygame.image.load("image/Background green only.png").convert()
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

    global score_start

# Time
    gametime = 0

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
                list_rasp.remove(i)     # Remove Object i, if it's under y=600
                score_start += 1

    # Rasperry: draw and mold

        #Write time to check in developement
        time_game = myfont.render("Time:" + str(round(gametime / 1000, 0)), False, (50, 150, 50))
        screen.blit(time_game, (500, 500))

        # for each rasp, check time and update image after specific time passing
        for i in list_rasp:
            # pygame.draw.circle(screen, BALL_COLOR, (i.pos_x, i.pos_y), i.rad)
            if time_passed <= 10:
                screen.blit(rasperry_image, [i.pos_x - 25, i.pos_y - 30])
            elif 10 < time_passed <= 20:
                screen.blit(rasperry_image_2, [i.pos_x - 25, i.pos_y - 30])
            elif 20 < time_passed <= 30:
                screen.blit(rasperry_image_4, [i.pos_x - 25, i.pos_y - 30])
            #elif 30 <= time_passed:        #Transfer to end -> would be overlayered by mouth
            #    screen.fill((0,0,0))
            #    restart()

    # Panel
        panel_move()
        #pygame.draw.rect(screen, PANEL_COLOR, (panel_x, panel_y, panel_width, panel_height), 0)
        screen.blit(to_image,[panel_x-8,panel_y-5])

    # Ball: Draw and move ball via ball class function
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))
        b1.move(panel_x, panel_y)

    # Draw Mouth
        screen.blit(fg_image, [0, 0])

    # Write score
        score = myfont.render("Score:" + str(score_start), False, (150, 50, 50))
        screen.blit(score, score_pos)

    # End game if specific time is reached
        if 30 <= time_passed:
            restart()

    # End game if ball is under the panel
        if (b1.pos_y + b1.rad >= panel_y + b1.rad*20):
            score_start = 0
            restart()

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


def credits():
    screen_r = screen.get_rect()
    font = pygame.font.SysFont("Arial", 25) #FreeMono

    credit_list = [ "BERRY BUSTER", " "," ", "Developer - Rike & Jenny", " ","Developer - Rike & Jenny"
                    ," ", "Lead Graphic Designer - Rike & Jenny", " ","Graphic Designer - Rike & Jenny"," "
                    , "Menu System - Rike & Jenny", " ", "Music - Rike & Jenny", " ", "Motion Designer - Rike & Jenny"
                    , " ", " ", "Special Thanks to friends :)"]

    texts = []
    # Text rendering for efficiancy

    green = pygame.image.load("image/Background green only.png").convert()
    green = pygame.transform.scale(green, (800, 600))

    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (255, 10, 10))
        # we also create a Rect for each Surface.
        # whenever you use rects with surfaces, it may be a good idea to use sprites instead
        # we give each rect the correct starting position
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
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


def menu():
    menu_image = pygame.image.load("image/menu.png").convert()
    menu_image = pygame.transform.scale(menu_image, (800, 600))

    while True:
        screen.blit(menu_image, [0, 0])

        key = pygame.key.get_pressed()
        if key[K_s]:
            starting_phase()

        if key[K_c]:
            credits()

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



menu()

