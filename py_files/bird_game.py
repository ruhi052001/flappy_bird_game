import pygame
import random
from pygame import mixer

#pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
mixer.init()
pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# load images
background = pygame.image.load('bg.png')
background = pygame.transform.scale(background, (1000, 600))
base = pygame.image.load('base.png')
base = pygame.transform.scale2x(base)
bird = pygame.image.load('bird.png').convert_alpha()
bird = pygame.transform.scale(bird, (40, 40))
bird_rect = bird.get_rect(center=(100, 300))
pipe_surface = pygame.image.load('pipe.png')
pipe_surface = pygame.transform.scale(pipe_surface, (80, 700))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [450, 400, 390]

game_over_surface = pygame.image.load('game_over.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(500, 300))

# game variable
base_pos = 0
gravity = 0.10
bird_movement = 0
game_on = True
score = 0
high_score = 0
#score_sound_countdown = 100

# load sound
flap_sound = pygame.mixer.Sound('sound_sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound_sfx_hit.wav')
#score_sound = pygame.mixer.Sound('sound_sfx_point.wav')

# background sound
mixer.music.load('Illusory-Realm-MP3.mp3')
mixer.music.play(-1, 0.0, 6000)


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render('SCORE : ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(100, 20))
        screen.blit(score_surface, score_rect)

    elif game_state == 'game_over':
        score_surface = game_font.render('SCORE : ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(100, 20))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render('HIGH SCORE : ' + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(500, 500))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 530:
        return False

    return True


def draw_base():
    screen.blit(base, (base_pos, 530))
    screen.blit(base, (base_pos + 1000, 530))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(1000, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(1000, random_pipe_pos - 250))

    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def rotate_bird(birds):
    new_bird = pygame.transform.rotozoom(birds, -bird_movement * 7, 1)
    return new_bird


run = True

while run:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_on:
                flap_sound.play()
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and game_on == False:
                game_on = True
                pipe_list.clear()
                bird_rect.center = (100, 300)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            # print(pipe_list)

    if game_on:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_on = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
        #score_sound_countdown -= 1
        #if score_sound_countdown <= 0:
            #score_sound.play()
            #score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # base movement
    base_pos -= 1
    draw_base()
    if base_pos <= -1000:
        base_pos = 0
    pygame.display.update()
    clock.tick(200)
