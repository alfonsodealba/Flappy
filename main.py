import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Game')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load assets
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    player_image = pygame.image.load(os.path.join(current_dir, 'cui.jpg'))
    player_image = pygame.transform.scale(player_image, (40, 40))
    background = pygame.image.load('space-background.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    jump_sound = pygame.mixer.Sound('jump.wav')
    hit_sound = pygame.mixer.Sound('hit.wav')
except Exception as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    sys.exit()

# Game variables
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
player_x = 50
player_y = SCREEN_HEIGHT // 2
player_velocity = 0
gravity = 0.25
jump_strength = -7
passed_pipe = False

# Pipe variables
PIPE_WIDTH = 70
PIPE_GAP = 200
pipe_x = SCREEN_WIDTH
pipe_height = random.randint(150, 400)

# Score
score = 0
font = pygame.font.Font(None, 74)

# Game states
game_over = False
show_cuinino = False
cuinino_timer = 0
CUININO_DURATION = 60  # How many frames to show the text (60 frames = 1 second)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player_velocity = jump_strength
                jump_sound.play()
            if event.key == pygame.K_r and game_over:
                # Reset game
                player_y = SCREEN_HEIGHT // 2
                player_velocity = 0
                pipe_x = SCREEN_WIDTH
                score = 0
                game_over = False
                passed_pipe = False

    if not game_over:
        # Update player
        player_velocity += gravity
        player_y += player_velocity

        # Update pipe
        pipe_x -= 3

        # Check if pipe is off screen
        if pipe_x < -PIPE_WIDTH:
            pipe_x = SCREEN_WIDTH
            pipe_height = random.randint(150, 400)
            passed_pipe = False

        # Score update
        if pipe_x < player_x and not passed_pipe:
            score += 1
            passed_pipe = True
            show_cuinino = True
            cuinino_timer = CUININO_DURATION

        # Update cuinino timer
        if show_cuinino:
            cuinino_timer -= 1
            if cuinino_timer <= 0:
                show_cuinino = False

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        top_pipe_rect = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
        bottom_pipe_rect = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)

        # Check collisions
        if (player_rect.colliderect(top_pipe_rect) or 
            player_rect.colliderect(bottom_pipe_rect) or 
            player_y >= SCREEN_HEIGHT - PLAYER_HEIGHT or 
            player_y <= 0):
            game_over = True
            hit_sound.play()

    # Draw everything
    screen.blit(background, (0, 0))

    # Draw pipes
    pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, pipe_height))
    pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

    # Draw Cuiniño text
    if show_cuinino:
        cuinino_text = font.render('Cuiniño!', True, WHITE)
        text_rect = cuinino_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(cuinino_text, text_rect)

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw game over
    if game_over:
        game_over_text = font.render('Game Over!', True, RED)
        restart_text = font.render('Press R to restart', True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()