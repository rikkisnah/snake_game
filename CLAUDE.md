# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
A Python implementation of the classic Snake game using Pygame with high score persistence, fullscreen support, and an easter egg feature. The game is implemented in a single file (snake_game.py) using a functional programming approach.

## Commands

### Setup & Installation
```bash
make install      # Creates venv and installs pygame==2.6.1
```

### Running the Game
```bash
make run         # Activates venv and runs snake_game.py
python3 snake_game.py  # Alternative direct run (ensure venv is active)
```

### Testing
```bash
make test        # Runs unittest discover with venv
python3 -m unittest discover  # Alternative test command
python3 -m unittest test_snake_game.TestSnakeGame.test_specific  # Run single test
```

### Cleanup
```bash
make clean       # Removes __pycache__, .pytest_cache, .coverage
```

## Architecture

### Core Game Loop Flow (snake_game.py)
1. **main_game()**: Entry point - gets player name then starts game loop
2. **get_player_name()**: Interactive name entry (max 15 chars, alphanumeric + space/underscore/hyphen)
3. **gameLoop(player_name)**: Main game logic
   - Event handling (movement, quit, fullscreen toggle)
   - Snake position updates and collision detection
   - Food consumption and respawning
   - Easter egg trigger (20% chance on food consumption)
   - Score persistence via high_scores.json

### Key Functions and State Management
- **Display Functions**: `your_score()`, `our_snake()`, `message()`
- **High Score System**: `load_high_scores()`, `save_high_scores()`, `add_high_score()`, `display_high_scores()`
- **Game State Variables in gameLoop()**:
  - `snake_List`: List of [x,y] coordinates for all segments
  - `Length_of_snake`: Current snake length (increases on food consumption)
  - `x1_change/y1_change`: Movement direction (±20 pixels)
  - `easter_egg_timer`: Controls "@rekharoy" display duration (30 frames)

### Collision Detection Algorithms
- **Wall collision**: Checks if head position exceeds screen boundaries
- **Self collision**: Iterates through body segments checking for head overlap
- **Food collision**: Exact coordinate match between head and food position

### Data Persistence
- **high_scores.json**: Stores top 10 scores as `[{"name": "player", "score": 29}, ...]`
- Automatically created if missing, sorted by score descending
- Graceful error handling for file corruption

### Game Constants
- Screen: 800x600 default (fullscreen supported via F key)
- Block size: 20x20 pixels (snake segments and food)
- Game speed: 15 FPS via `clock.tick(15)`
- Colors: Black (0,0,0), Green (0,255,0), Red (255,0,0), White (255,255,255)

### Controls
- **Menu**: SPACE (start), H (high scores), F (fullscreen toggle)
- **Gameplay**: Arrow keys (movement), F (fullscreen)
- **Game Over**: C (continue/restart), Q (quit)
- **Name Entry**: Alphanumeric keys, BACKSPACE, RETURN to submit

### Testing Approach
- Uses unittest framework with mocking for pygame components
- Test file: test_snake_game.py
- Currently minimal coverage - focus on expanding collision and state management tests