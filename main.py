import pygame
import sys
import random

# Pygame & Mixer Initialize ചെയ്യുക (ക്രാഷ് ആവാതിരിക്കാൻ try-except)
pygame.init()
try:
    pygame.mixer.init()
    sound_enabled = True
except:
    sound_enabled = False

# സ്ക്രീൻ വലിപ്പം
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HEBERT Bird")

clock = pygame.time.Clock()
FPS = 30

# നിറങ്ങൾ
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (135, 206, 235)

# കസ്റ്റം ഫേസ് ലോഡ് ചെയ്യുന്നു (face.png)
try:
    bird_img = pygame.image.load("face.png")
    bird_img = pygame.transform.scale(bird_img, (40, 40))
except:
    bird_img = pygame.Surface((40, 40))
    bird_img.fill((255, 200, 0))

# സൗണ്ട് ഫയലുകൾ ലോഡ് ചെയ്യുന്നു (.m4a മാത്രം)
try:
    if sound_enabled:
        score_sound = pygame.mixer.Sound("score.m4a")
        gameover_sound = pygame.mixer.Sound("gameover.m4a")
    else:
        score_sound = None
        gameover_sound = None
except:
    score_sound = None
    gameover_sound = None

# വേരിയബിളുകൾ
bird_x = 50
bird_y = 300
gravity = 0.8
bird_movement = 0

pipe_gap = 150
pipe_width = 70
pipe_speed = 3
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

score = 0
font = pygame.font.Font(None, 40)
game_active = True

def create_pipe():
    random_pipe_pos = random.randint(150, 400)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, random_pipe_pos, pipe_width, SCREEN_HEIGHT - random_pipe_pos)
    top_pipe = pygame.Rect(SCREEN_WIDTH, random_pipe_pos - pipe_gap - SCREEN_HEIGHT, pipe_width, SCREEN_HEIGHT)
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(pipes):
    global game_active
    bird_rect = pygame.Rect(bird_x, bird_y, 40, 40)
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            if sound_enabled and gameover_sound:
                gameover_sound.play()
            return False
            
    if bird_y <= 0 or bird_y >= SCREEN_HEIGHT:
        if sound_enabled and gameover_sound:
            gameover_sound.play()
        return False
        
    return True

# ഗെയിം ലൂപ്പ്
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                bird_movement = 0
                bird_movement -= 10
            else:
                game_active = True
                pipe_list.clear()
                bird_y = 300
                bird_movement = 0
                score = 0
                
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.fill(BLUE)

    if game_active:
        bird_movement += gravity
        bird_y += bird_movement
        screen.blit(bird_img, (bird_x, bird_y))
        
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        game_active = check_collision(pipe_list)
        
        for pipe in pipe_list:
            if pipe.centerx == bird_x:
                score += 0.5
                if score.is_integer() and sound_enabled and score_sound:
                    score_sound.play()
                    
        score_text = font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
    else:
        over_text = font.render("HEBERT Bird Over!", True, WHITE)
        restart_text = font.render("Tap to Restart", True, WHITE)
        screen.blit(over_text, (80, 250))
        screen.blit(restart_text, (100, 300))

    pygame.display.update()
    clock.tick(FPS)
