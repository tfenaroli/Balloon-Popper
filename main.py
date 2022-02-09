import pygame, sys, random

# initializes pygame display/screen
pygame.init()
pygame.display.set_caption("Balloon Popper")
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()

# global variables
playing = True
item_velocity = 1
score = 0
bird_velocity = 0
floor_x = 0

# background image
background = pygame.image.load("images/background.png").convert_alpha()

# creates bird objects
preflip_bird_surface = pygame.image.load("images/bird.png").convert_alpha()
bird_surface = pygame.transform.flip(preflip_bird_surface, True, False)
bird_rect = bird_surface.get_rect(center=(120, 360))

# creates balloon objects
balloons = []
balloon_locations = [110, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650]
balloon_surface = pygame.image.load("images/blueballoon.png").convert_alpha()

# creates kite objects
kites = []
kite_locations = [110, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650]
kite_surface = pygame.image.load("images/kite.png").convert_alpha()

# spawns item
SPAWNITEM = pygame.USEREVENT
pygame.time.set_timer(SPAWNITEM, 600)

# creates balloon
def create_balloon():
    balloon_rect = balloon_surface.get_rect(center=(740, random.choice(balloon_locations)))
    balloons.append(balloon_rect)

# creates kite
def create_kite():
    kite_rect = balloon_surface.get_rect(center=(740, random.choice(kite_locations)))
    kites.append(kite_rect)

# draws bird
def draw_bird():
    screen.blit(bird_surface, bird_rect)

# displays score
def display_score():
    # font
    font = pygame.font.Font("font/gamefont.ttf", 80)
    font.set_bold(True)

    # if playing game
    if playing:
        score_surface = font.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(360, 50))
        screen.blit(score_surface, score_rect)

    # if not playing game
    else:
        font = pygame.font.Font("font/gamefont.ttf", 60)
        font.set_bold(False)
        score_surface = font.render("Good BalloonPopper, your score was " + str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(360, 50))
        text_surface = font.render("Press R to play again!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(360, 450))
        screen.blit(score_surface, score_rect)
        screen.blit(text_surface, text_rect)

# draws items
def draw_items():
    # draws every balloon
    for balloon in balloons:
        if balloon.centerx < -20:
            balloons.remove(balloon)
            print("deleted")
        screen.blit(balloon_surface, balloon)
        if playing:
            balloon.centerx -= item_velocity

    # draws every kite
    for kite in kites:
        if kite.centerx < -20:
            kites.remove(kite)
            print("deleted")
        screen.blit(kite_surface, kite)
        if playing:
            kite.centerx -= item_velocity

# draws background
def draw_background():
    screen.blit(background, (0, 0))

# checks for collisions
def check_collision():
    global playing, score

    # checks for balloon collision
    for balloon in balloons:
        if bird_rect.colliderect(balloon):
            print("collision det")
            balloons.remove(balloon)
            score += 1

    # checks for kite collision
    for kite in kites:
        if bird_rect.colliderect(kite):
            playing = False

# game loop
while True:
    gravity = .1
    for event in pygame.event.get():
        # if quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if spawn item
        if event.type == SPAWNITEM and playing:
            if random.randint(0, 1) == 0:
                create_balloon()
            else:
                create_kite()

    keys = pygame.key.get_pressed()

    # if key pressed is space
    if keys[pygame.K_SPACE] and playing:
        gravity = -.1

    # if key pressed is 'r'
    elif keys[pygame.K_r] and not playing:
        playing = True
        balloons.clear()
        kites.clear()
        score = 0
        bird_velocity = 0
        bird_rect.centery = 360

    # draws components
    draw_background()
    draw_items()
    draw_bird()
    display_score()

    # check for collisions
    check_collision()

    # if playing
    if playing:
        bird_velocity += gravity
        bird_rect.centery += bird_velocity

    # update display and tick clock
    pygame.display.update()
    clock.tick(120)