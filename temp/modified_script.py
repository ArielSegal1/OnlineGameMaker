import pygame
import random

import sys
import os

# if getattr(sys, 'frozen', False): # PyInstaller adds this attribute
#     # Running in a bundle
#     CurrentPath = sys._MEIPASS
# else:
#     # Running in normal Python environment
#     CurrentPath = os.path.dirname(__file__)
# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pygame Game")

# Load and resize player image
original_player_image = pygame.image.load("cloud.png")
DESIRED_PLAYER_SIZE = (50, 50)
player_image = pygame.transform.scale(original_player_image, DESIRED_PLAYER_SIZE)
PLAYER_SIZE = player_image.get_rect().size
player_color = (0, 128, 255)
collect_color = (255, 100, 0)
background_color = (0, 0, 0)

# Set up player
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 23

# Set up collectible
COLLECT_SIZE = 30
collect_pos = [random.randint(0, WIDTH - COLLECT_SIZE), random.randint(0, HEIGHT - COLLECT_SIZE)]

# Set up score
score = 0
font = pygame.font.SysFont("comicsansms", 35)

# Game loop
running = True
while running:
    pygame.time.delay(30)  # Delay to control frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE[0]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - PLAYER_SIZE[1]:
        player_pos[1] += player_speed

    # Check for collision
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE[0], PLAYER_SIZE[1])
    collect_rect = pygame.Rect(collect_pos[0], collect_pos[1], COLLECT_SIZE, COLLECT_SIZE)
    if player_rect.colliderect(collect_rect):
        score += 1
        collect_pos = [random.randint(0, WIDTH - COLLECT_SIZE), random.randint(0, HEIGHT - COLLECT_SIZE)]

    # Draw everything
    win.fill(background_color)
    win.blit(player_image, player_pos)
    pygame.draw.rect(win, collect_color, (collect_pos[0], collect_pos[1], COLLECT_SIZE, COLLECT_SIZE))

    # Render score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
