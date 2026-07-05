#ai-assisted with OCA/OpenAI Model with human supervision

from __future__ import annotations

import json
import os
import random
import sys
from dataclasses import dataclass, field

import pygame

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

Color = tuple[int, int, int]
HighScore = dict[str, str | int]


@dataclass
class GameState:
    """Mutable state for one round of Snake."""

    x: float
    y: float
    food_x: float
    food_y: float
    x_change: int = 0
    y_change: int = 0
    segments: list[list[float]] = field(default_factory=list)
    length: int = 1
    game_over: bool = False
    game_close: bool = False
    score_saved: bool = False
    easter_egg_message: str = ""
    easter_egg_timer: int = 0
    easter_egg_pos: tuple[int, int] = (0, 0)


def your_score(score: int) -> None:
    value = score_font.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])


def our_snake(block_size: int, snake_list: list[list[float]]) -> None:
    for segment in snake_list:
        pygame.draw.rect(screen, green, [segment[0], segment[1], block_size, block_size])


def toggle_fullscreen() -> None:
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

def message(
    msg: str,
    color: Color,
    y_offset: int = 0,
    x_pos: float | None = None,
) -> None:
    mesg = font_style.render(msg, True, color)
    if x_pos is None:
        x_pos = screen_width / 6
    screen.blit(mesg, [x_pos, screen_height / 3 + y_offset])


def load_high_scores() -> list[HighScore]:
    if os.path.exists(HIGH_SCORES_FILE):
        try:
            with open(HIGH_SCORES_FILE, "r", encoding="utf-8") as score_file:
                scores = json.load(score_file)
                return scores if isinstance(scores, list) else []
        except (OSError, json.JSONDecodeError):
            return []
    return []


def save_high_scores(scores: list[HighScore]) -> None:
    with open(HIGH_SCORES_FILE, "w", encoding="utf-8") as score_file:
        json.dump(scores, score_file)


def add_high_score(name: str, score: int) -> list[HighScore]:
    scores = load_high_scores()
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # Keep only top 10
    save_high_scores(scores)
    return scores


def get_player_name() -> str:
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
                    if event.unicode.isalnum() or event.unicode in [" ", "_", "-"]:
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


def display_high_scores(current_score: int | None = None, player_name: str | None = None) -> None:
    scores = load_high_scores()

    screen.fill(black)
    title = font_style.render("HIGH SCORES", True, green)
    screen.blit(title, [screen_width / 3, 50])

    y_pos = 120
    for i, score_data in enumerate(scores[:10]):
        is_current_player = (
            score_data.get("name") == player_name
            and score_data.get("score") == current_score
        )
        color = green if is_current_player else white
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


def _random_food_coordinate(limit: int) -> float:
    return round(random.randrange(0, limit - snake_block) / 20.0) * 20.0


def _random_food_position() -> tuple[float, float]:
    return _random_food_coordinate(screen_width), _random_food_coordinate(screen_height)


def _new_game_state() -> GameState:
    food_x, food_y = _random_food_position()
    return GameState(screen_width / 2, screen_height / 2, food_x, food_y)


def _handle_game_over_screen(state: GameState, player_name: str) -> None:
    while state.game_close and not state.game_over:
        final_score = state.length - 1
        if not state.score_saved:
            add_high_score(player_name, final_score)
            state.score_saved = True
        display_high_scores(final_score, player_name)

        for event in pygame.event.get():
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_f:
                toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE and is_fullscreen:
                toggle_fullscreen()
            elif event.key == pygame.K_q:
                state.game_over = True
                state.game_close = False
            elif event.key == pygame.K_c:
                main_game()


def _reposition_food_if_needed(state: GameState) -> None:
    if state.food_x >= screen_width - snake_block:
        state.food_x = _random_food_coordinate(screen_width)
    if state.food_y >= screen_height - snake_block:
        state.food_y = _random_food_coordinate(screen_height)


def _handle_game_key(state: GameState, key: int) -> None:
    if key == pygame.K_f:
        toggle_fullscreen()
        _reposition_food_if_needed(state)
    elif key == pygame.K_ESCAPE and is_fullscreen:
        toggle_fullscreen()
        _reposition_food_if_needed(state)
    elif key == pygame.K_LEFT:
        state.x_change, state.y_change = -snake_block, 0
    elif key == pygame.K_RIGHT:
        state.x_change, state.y_change = snake_block, 0
    elif key == pygame.K_UP:
        state.x_change, state.y_change = 0, -snake_block
    elif key == pygame.K_DOWN:
        state.x_change, state.y_change = 0, snake_block


def _handle_gameplay_events(state: GameState) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.game_over = True
        elif event.type == pygame.KEYDOWN:
            _handle_game_key(state, event.key)


def _advance_snake(state: GameState) -> None:
    if (
        state.x >= screen_width
        or state.x < 0
        or state.y >= screen_height
        or state.y < 0
    ):
        state.game_close = True
    state.x += state.x_change
    state.y += state.y_change
    snake_head = [state.x, state.y]
    state.segments.append(snake_head)
    if len(state.segments) > state.length:
        del state.segments[0]
    if snake_head in state.segments[:-1]:
        state.game_close = True


def _render_game(state: GameState) -> None:
    screen.fill(black)
    if state.easter_egg_timer > 0:
        easter_egg = font_style.render(state.easter_egg_message, True, white)
        screen.blit(easter_egg, state.easter_egg_pos)
        state.easter_egg_timer -= 1
    pygame.draw.rect(
        screen,
        red,
        [state.food_x, state.food_y, snake_block, snake_block],
    )
    our_snake(snake_block, state.segments)
    your_score(state.length - 1)
    pygame.display.update()


def _handle_food_collision(state: GameState) -> None:
    if state.x != state.food_x or state.y != state.food_y:
        return
    state.food_x, state.food_y = _random_food_position()
    state.length += 1
    if random.randint(1, 5) == 1:
        state.easter_egg_message = "@rekharoy"
        state.easter_egg_timer = 30
        state.easter_egg_pos = (
            random.randint(50, max(51, screen_width - 250)),
            random.randint(50, max(51, screen_height - 100)),
        )


def gameLoop(player_name: str = "Player") -> None:
    state = _new_game_state()
    while not state.game_over:
        _handle_game_over_screen(state, player_name)
        _handle_gameplay_events(state)
        _advance_snake(state)
        _render_game(state)
        _handle_food_collision(state)
        clock.tick(snake_speed)
    pygame.quit()
    sys.exit()


def start_screen() -> None:
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
        hint_text = (
            "Press F for Fullscreen"
            if not is_fullscreen
            else "Press ESC to exit Fullscreen"
        )
        hint = small_font.render(hint_text, True, white)
        screen.blit(hint, [screen_width / 3, screen_height - 40])
        pygame.display.update()
        clock.tick(15)


def show_high_scores_menu() -> None:
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


def main_game() -> None:
    player_name = get_player_name()
    gameLoop(player_name)


if __name__ == "__main__":
    start_screen()
    main_game()
