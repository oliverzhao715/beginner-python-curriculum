import pygame
import sys
import random

# Initialize Pygame
def header():
    print("====================================")
    print("    WELCOME TO THE CASTING GAME!    ")
    print("====================================")

pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 255, 127)
YELLOW = (255, 215, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)

# Create the window
screen = screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

real_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Most Fair and Balanced Python Game Ever")
clock = pygame.time.Clock()

# Game Variables
player_x = 50
player_y = 100
player_size = 20

# Rage Mechanics: Slippery physics (velocity and friction)
player_vx = 0
player_vy = 0
ACCELERATION = 0.4
FRICTION = 0.98  # High value = slippery like ice

# Statistics
death_count = 0
shake_duration = 0

# Goal position
goal_rect = pygame.Rect(700, 480, 40, 40)

# Invisible walls (The player doesn't see these until they crash!)
walls = [
    pygame.Rect(0, 0, 800, 40),          # Top border
    pygame.Rect(0, 560, 800, 40),        # Bottom border
    pygame.Rect(0, 0, 40, 600),          # Left border
    pygame.Rect(760, 0, 40, 600),        # Right border
    pygame.Rect(200, 40, 50, 400),       # Hidden maze wall 1
    pygame.Rect(400, 160, 50, 400),      # Hidden maze wall 2
    pygame.Rect(600, 40, 50, 400)        # Hidden maze wall 3
]

# Fake Skip Button Variables
button_rect = pygame.Rect(320, 10, 160, 30)

def reset_player():
    """Resets player position and stops momentum."""
    global player_x, player_y, player_vx, player_vy
    player_x = 60
    player_y = 80
    player_vx = 0
    player_vy = 0

# Initialize player position
reset_player()

# Main Game Loop
running = True
while running:
    # 1. Handle Events
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rage Mechanic: Runaway "Skip Level" button
    if button_rect.collidepoint(mouse_pos):
        button_rect.x = random.randint(50, SCREEN_WIDTH - 210)
        button_rect.y = random.randint(50, SCREEN_HEIGHT - 80)

    # 2. Handle Keyboard Input (Movement)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_vx -= ACCELERATION
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_vx += ACCELERATION
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_vy -= ACCELERATION
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_vy += ACCELERATION

    # Apply friction (creates the slippery sliding effect)
    player_vx *= FRICTION
    player_vy *= FRICTION

    # Update positions
    player_x += player_vx
    player_y += player_vy

    # Create a temporary rect for player collision checking
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # 3. Collision Detection
    collision_detected = False
    for wall in walls:
        if player_rect.colliderect(wall):
            collision_detected = True
            break

    if collision_detected:
        death_count += 1
        shake_duration = 15  # Trigger screen shake frames
        reset_player()
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # Check Win Condition
    if player_rect.colliderect(goal_rect):
        # Troll ending: Instead of winning, it adds 1000 deaths and resets
        death_count += 1000
        shake_duration = 40
        reset_player()

    # 4. Drawing Everything
    screen.fill(BLACK)

    # Draw Safe Zones (Start and Goal)
    pygame.draw.rect(screen, GRAY, (40, 40, 100, 100)) # Spawn area indicator
    pygame.draw.rect(screen, YELLOW, goal_rect)

    # Rage Mechanic: Walls are INVISIBLE. They only render for a split second 
    # when the screen shakes from a death. Otherwise, you have to guess.
    if shake_duration > 0:
        for wall in walls:
            pygame.draw.rect(screen, RED, wall)
    else:
        # Draw only outer borders so player doesn't escape map entirely
        pygame.draw.rect(screen, GRAY, walls[0])
        pygame.draw.rect(screen, GRAY, walls[1])
        pygame.draw.rect(screen, GRAY, walls[2])
        pygame.draw.rect(screen, GRAY, walls[3])

    # Draw Player
    pygame.draw.rect(screen, GREEN, player_rect)

    # Draw Fake Skip Button
    pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
    font = pygame.font.SysFont("Arial", 18, bold=True)
    btn_text = font.render("SKIP LEVEL", True, BLACK)
    screen.blit(btn_text, (button_rect.x + 35, button_rect.y + 3))

    # Draw Death Counter UI
    ui_font = pygame.font.SysFont("Impact", 32)
    death_text = ui_font.render(f"DEATHS: {death_count}", True, RED)
    screen.blit(death_text, (40, 500))

    # 5. Screen Shake Logic & Final Render
    shift_x = 0
    shift_y = 0
    if shake_duration > 0:
        shift_x = random.randint(-8, 8)
        shift_y = random.randint(-8, 8)
        shake_duration -= 1

    real_screen.fill(BLACK)
    real_screen.blit(screen, (shift_x, shift_y))
    pygame.display.flip()

    # Maintain frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
