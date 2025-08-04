import pygame
import sys
import random
import json
import os

# Initialize Pygame
pygame.init()

# Get display info for fullscreen
display_info = pygame.display.Info()
fullscreen_width = display_info.current_w
fullscreen_height = display_info.current_h

# Screen dimensions
default_width = 800
default_height = 600
screen_width = default_width
screen_height = default_height
is_fullscreen = False

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Snake properties
snake_block = 20
snake_speed = 15

# Font
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)
small_font = pygame.font.SysFont(None, 25)

# High scores file
HIGH_SCORES_FILE = "high_scores.json"


def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])


def toggle_fullscreen():
    global screen, screen_width, screen_height, is_fullscreen
    is_fullscreen = not is_fullscreen
    
    if is_fullscreen:
        screen_width = fullscreen_width
        screen_height = fullscreen_height
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen_width = default_width
        screen_height = default_height
        screen = pygame.display.set_mode((screen_width, screen_height))

def message(msg, color, y_offset=0, x_pos=None):
    mesg = font_style.render(msg, True, color)
    if x_pos is None:
        x_pos = screen_width / 6
    screen.blit(mesg, [x_pos, screen_height / 3 + y_offset])


def load_high_scores():
    if os.path.exists(HIGH_SCORES_FILE):
        try:
            with open(HIGH_SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def save_high_scores(scores):
    with open(HIGH_SCORES_FILE, 'w') as f:
        json.dump(scores, f)


def add_high_score(name, score):
    scores = load_high_scores()
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # Keep only top 10
    save_high_scores(scores)
    return scores


def get_player_name():
    name = ""
    input_active = True
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE and is_fullscreen:
                    toggle_fullscreen()
                elif event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15:  # Limit name length
                    if event.unicode.isalnum() or event.unicode in [' ', '_', '-']:
                        name += event.unicode
        
        screen.fill(black)
        message("Enter Your Name:", white, -50)
        name_surface = font_style.render(name + "_", True, green)
        screen.blit(name_surface, [screen_width / 3, screen_height / 2])
        hint = small_font.render("Press ENTER when done", True, white)
        screen.blit(hint, [screen_width / 3, screen_height / 2 + 60])
        pygame.display.update()
        clock.tick(15)
    
    return name if name else "Anonymous"


def display_high_scores(current_score=None, player_name=None):
    scores = load_high_scores()
    
    screen.fill(black)
    title = font_style.render("HIGH SCORES", True, green)
    screen.blit(title, [screen_width / 3, 50])
    
    y_pos = 120
    for i, score_data in enumerate(scores[:10]):
        color = green if score_data.get("name") == player_name and score_data.get("score") == current_score else white
        score_text = f"{i+1}. {score_data['name'][:15]:15} {score_data['score']:5}"
        score_surface = small_font.render(score_text, True, color)
        screen.blit(score_surface, [screen_width / 3, y_pos])
        y_pos += 30
    
    if current_score is not None:
        current_text = score_font.render(f"Your Score: {current_score}", True, white)
        screen.blit(current_text, [screen_width / 3, y_pos + 30])
    
    hint = small_font.render("Press C-Play Again or Q-Quit", True, white)
    screen.blit(hint, [screen_width / 3, screen_height - 80])
    
    pygame.display.update()


def gameLoop(player_name="Player"):
    global screen_width, screen_height
    game_over = False
    game_close = False

    # Initial position of the snake
    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    easter_egg_message = ""
    easter_egg_timer = 0
    easter_egg_pos = (0, 0)
    
    score_saved = False  # Flag to track if score has been saved

    # Position of the food
    foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0

    while not game_over:

        while game_close == True:
            final_score = Length_of_snake - 1
            if not score_saved:
                scores = add_high_score(player_name, final_score)
                score_saved = True
            display_high_scores(final_score, player_name)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE and is_fullscreen:
                        toggle_fullscreen()
                    elif event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        main_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    toggle_fullscreen()
                    # Reposition food if it's out of bounds after fullscreen toggle
                    if foodx >= screen_width - snake_block:
                        foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
                    if foody >= screen_height - snake_block:
                        foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
                elif event.key == pygame.K_ESCAPE and is_fullscreen:
                    toggle_fullscreen()
                    # Reposition food if needed
                    if foodx >= screen_width - snake_block:
                        foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
                    if foody >= screen_height - snake_block:
                        foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
                elif event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(black)

        if easter_egg_timer > 0:
            mesg = font_style.render(easter_egg_message, True, white)
            screen.blit(mesg, easter_egg_pos)
            easter_egg_timer -= 1

        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

            if random.randint(1, 5) == 1:  # 20% chance to trigger easter egg
                easter_egg_message = "@rekharoy"
                easter_egg_timer = 30  # Show for 30 frames
                easter_egg_pos = (random.randint(50, max(51, screen_width - 250)), random.randint(50, max(51, screen_height - 100)))


        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()


def start_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                elif event.key == pygame.K_h:
                    show_high_scores_menu()
                elif event.key == pygame.K_f:
                    toggle_fullscreen()

        screen.fill(black)
        message("Welcome to Snake!", green)
        message("Press SPACE to start", white, 50)
        message("Press H for High Scores", white, 100)
        hint_text = "Press F for Fullscreen" if not is_fullscreen else "Press ESC to exit Fullscreen"
        hint = small_font.render(hint_text, True, white)
        screen.blit(hint, [screen_width / 3, screen_height - 40])
        pygame.display.update()
        clock.tick(15)


def show_high_scores_menu():
    viewing = True
    while viewing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    viewing = False
        
        display_high_scores()
        hint = small_font.render("Press ESC or SPACE to return", True, white)
        screen.blit(hint, [screen_width / 3, screen_height - 40])
        pygame.display.update()
        clock.tick(15)


def main_game():
    player_name = get_player_name()
    gameLoop(player_name)


if __name__ == '__main__':
    start_screen()
    main_game()
