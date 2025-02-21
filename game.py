import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (169, 169, 169)
FONT = pygame.font.Font(None, 36)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")
clock = pygame.time.Clock()

# Game states
STATE_MAIN_MENU = "main_menu"
STATE_INSTRUCTIONS = "instructions"
STATE_GAME = "game"
STATE_RESULT = "result"
game_state = STATE_MAIN_MENU

# Buttons
play_button = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 - 20, 100, 40)
proceed_button = pygame.Rect(WIDTH//2 - 50, HEIGHT - 100, 100, 40)

# AI prediction memory
history = []

# Spacebar tracking
spacebar_count = 0
player_choice = None
player_wins = 0
ai_wins = 0

def get_ai_choice(history):
    if len(history) < 3:
        return random.choice([1, 2, 3])
    return history[-1]  # Predicts last move

def display_text(text, x, y, color=BLACK):
    render = FONT.render(text, True, color)
    screen.blit(render, (x, y))

# Main loop
running = True
result_time = None
result_text = ""

while running:
    screen.fill(GREY)
    
    if game_state == STATE_MAIN_MENU:
        display_text("Rock Paper Scissors", WIDTH//2 - 100, 100)
        pygame.draw.rect(screen, BLUE, play_button)
        display_text("Play", WIDTH//2 - 20, HEIGHT//2 - 10, WHITE)
    
    elif game_state == STATE_INSTRUCTIONS:
        instructions = [
            "The game follows the rhythm: Rock. Paper. Scissors. Shoot!",
            "Press SPACEBAR 3 times, then press 1, 2, or 3 for Rock, Paper, or Scissors.",
            "The AI will predict your next move.",
            "Click Proceed to start!"
        ]
        for i, line in enumerate(instructions):
            display_text(line, 50, 50 + i * 40)
        pygame.draw.rect(screen, GREEN, proceed_button)
        display_text("Proceed", WIDTH//2 - 30, HEIGHT - 90, WHITE)
    
    elif game_state == STATE_GAME:
        display_text(f"Player Wins: {player_wins}  AI Wins: {ai_wins}", WIDTH//2 - 100, 50, BLACK)
        display_text("press space bar 3 times, play again.", WIDTH//2 - 100, 100, BLACK)
        if spacebar_count == 1:
            pygame.draw.rect(screen, RED, (WIDTH//4, HEIGHT//2, 50, 50))
        elif spacebar_count == 2:
            pygame.draw.rect(screen, YELLOW, (WIDTH//4 + 60, HEIGHT//2, 50, 50))
        elif spacebar_count == 3:
            pygame.draw.rect(screen, GREEN, (WIDTH//4 + 120, HEIGHT//2, 50, 50))
            display_text("Press 1, 2, or 3 to choose!", WIDTH//4, HEIGHT//2 + 100)
        
    elif game_state == STATE_RESULT:
        display_text(result_text, WIDTH//2 - 200, HEIGHT//2, RED)
        if time.time() - result_time > 5:
            spacebar_count = 0
            game_state = STATE_GAME
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == STATE_MAIN_MENU and play_button.collidepoint(event.pos):
                game_state = STATE_INSTRUCTIONS
            elif game_state == STATE_INSTRUCTIONS and proceed_button.collidepoint(event.pos):
                game_state = STATE_GAME
        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_GAME:
                if event.key == pygame.K_SPACE and spacebar_count < 3:
                    spacebar_count += 1
                elif spacebar_count == 3 and event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    player_choice = event.key - pygame.K_0
                    ai_choice = get_ai_choice(history)
                    history.append(player_choice)
                    
                    if player_choice == ai_choice:
                        result_text = f"It's a tie! Player chose {player_choice}, AI chose {ai_choice}" 
                    elif (player_choice == 1 and ai_choice == 3) or (player_choice == 2 and ai_choice == 1) or (player_choice == 3 and ai_choice == 2):
                        result_text = f"You win! Player chose {player_choice}, AI chose {ai_choice}"
                        player_wins += 1
                    else:
                        result_text = f"AI wins! Player chose {player_choice}, AI chose {ai_choice}" 
                        ai_wins += 1
                    
                    result_time = time.time()
                    game_state = STATE_RESULT
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
