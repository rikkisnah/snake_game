# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
A Python implementation of the classic Snake game using Pygame. The game features snake movement, food collection, score tracking, and includes an easter egg that randomly displays "@rekharoy" when eating food.

## Commands

### Setup & Installation
```bash
make install      # Creates venv and installs pygame dependency
```

### Running the Game
```bash
make run         # Runs the snake game
python3 snake_game.py  # Alternative direct run
```

### Testing
```bash
make test        # Runs unit tests with unittest discover
python3 -m unittest discover  # Alternative test command
```

### Cleanup
```bash
make clean       # Removes __pycache__, .pytest_cache, .coverage
```

## Architecture

### Core Components
- **snake_game.py**: Single-file game implementation using Pygame
  - `Snake` class: Manages snake position, movement, and collision detection
  - `Food` class: Handles food positioning and respawning
  - `Game` class: Main game loop, event handling, and screen rendering
  - Easter egg: 20% chance to display "@rekharoy" when eating food

### Game Constants
- Screen: 800x600 pixels
- Block size: 20x20 pixels  
- Game speed: 15 FPS
- Colors: Black background, green snake, red food, white text

### Controls
- Arrow keys: Snake movement
- SPACE: Start game from menu
- C: Continue after game over
- Q: Quit after game over