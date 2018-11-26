import pygame
from pygame.locals import *
import pygame.gfxdraw
import sys


#Setting
pygame.init()
pygame.mixer.quit()
SCREEN_WIDTH_Complete, SCREEN_HEIGHT = 800,600
screen = pygame.display.set_mode((SCREEN_WIDTH_Complete, SCREEN_HEIGHT), FULLSCREEN)
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
PANEL_COLOR = (40 ,30 ,10)
BACK_COLOR = (90 ,150 ,70)
BALL_COLOR = (255,0,0)

# Schreibkrams
pygame.font.init()  # you have to call this at the start,
myfont = pygame.font.SysFont('Arial', 20)
score_pos = (SCREEN_WIDTH_Complete*(6.8/8), SCREEN_HEIGHT/3)


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
        starting_phase()


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


def starting_phase():
    list_rasp = []
    list_posx_rasp = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    list_posy_rasp = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
    b1 = Ball()

# Kreiere Raspberries
    for i in range(0, 22):
        list_rasp.append(Rasperry(list_posx_rasp[i], list_posy_rasp[i], 20))

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
    rasperry_image = pygame.image.load("image/01 rasperry.png").convert()
    transColor = rasperry_image.get_at((0, 0))
    rasperry_image.set_colorkey(transColor)
    rasperry_image = pygame.transform.scale(rasperry_image,(45,50))


# Tongue
    to_image = pygame.image.load("image/Zunge.png").convert()
    to_image.set_colorkey(transColor)
    to_image = pygame.transform.scale(to_image,(94,80))

# Score
    global score_start

    while True:
        msElapsed = clock.tick(100)
        screen.blit(bg_image, [0, 0])

    # Draw Raspberries
        for i in list_rasp:
            pygame.draw.circle(screen, BALL_COLOR, (i.pos_x, i.pos_y), i.rad)
            screen.blit(rasperry_image, [i.pos_x-25, i.pos_y-30])


    #Panel and Ball
        panel_move()
        pygame.draw.rect(screen, PANEL_COLOR, (panel_x, panel_y, panel_width, panel_height), 0)
        screen.blit(to_image, [panel_x-2, panel_y-5])
        b1.pos_x = panel_x + panel_half_width
        b1.pos_y = panel_y - 2 * b1.rad
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))
        #pygame.draw.circle(screen, BALL_COLOR, (int(panel_x + panel_half_width), int(panel_y - 2 * b1.rad)), int(b1.diam))


    # Draw Mouth
        screen.blit(fg_image, [0, 0])

    # Write score
        score = myfont.render("Score:" + str(score_start), False, (50, 150, 50))
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
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                surface = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)


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
    to_image = pygame.transform.scale(to_image,(94,80))

    global score_start

    while True:
        msElapsed = clock.tick(100)
        screen.blit(bg_image, [0, 0])

    # Rasperrie collision and fall
        for i in list_rasp:
            if int((((b1.pos_x - i.pos_x)**2) + ((b1.pos_y - i.pos_y)**2))**(1/2)) <= i.rad + b1.rad:
                i.fall = True
            if i.fall == True:
                i.pos_y += 5
            if i.pos_y > 600:
                list_rasp.remove(i)     # Remove Object i, if it's under y=600
                score_start += 1

        # Draw Raspberries
        for i in list_rasp:
            pygame.draw.circle(screen, BALL_COLOR, (i.pos_x, i.pos_y), i.rad)
            screen.blit(rasperry_image, [i.pos_x-25, i.pos_y-30])
        #pygame.Surface.blit(rasp, screen, (rasp_x,rasp_y))

    # Panel
        panel_move()
        pygame.draw.rect(screen, PANEL_COLOR, (panel_x, panel_y, panel_width, panel_height), 0)
        screen.blit(to_image,[panel_x-2,panel_y-5])

    # Ball
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))
        b1.move(panel_x, panel_y)

    # Draw Mouth
        screen.blit(fg_image, [0, 0])

    # Write score
        score = myfont.render("Score:" + str(score_start), False, (50, 150, 50))
        screen.blit(score, score_pos)

    #Restart
        if (b1.pos_y + b1.rad >= panel_y + b1.rad*20):
            score_start = 0
            restart()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()



starting_phase()

