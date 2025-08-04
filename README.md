# Snake Game

This is a simple implementation of the classic Snake game using Python and the Pygame library.

## Features

- The snake can move in four directions (up, down, left, right).
- The snake grows longer each time it eats food.
- The game ends if the snake collides with itself or the walls.
- The current score is displayed.
- A simple start and end screen.
- Keyboard controls for snake movement.
- **High Score System**: Tracks top 10 scores with player names.
- **Player Name Entry**: Enter your name before playing.
- **Persistent Scores**: High scores are saved between game sessions.
- **Fullscreen Mode**: Toggle fullscreen with F key for immersive gameplay.
- Easter egg feature that randomly displays "@rekharoy".

## Getting Started

### Prerequisites

- Python 3
- pip
- Make

### Installation

Simply run the following command to install the dependencies:

```bash
make install
```

This will create a virtual environment and install the required packages.

## How to Play

Run the following command to start the game:

```bash
make run
```

- Press `SPACE` to start the game or `H` to view high scores from the main menu.
- Press `F` to toggle fullscreen mode on/off.
- Press `ESC` to exit fullscreen mode.
- Enter your name when prompted (press ENTER when done).
- Use the arrow keys (Up, Down, Left, Right) to control the snake.
- After game over, your score is automatically saved to the high scores.
- Press `C` to play again or `Q` to quit after losing.

## Running the Tests

To run the unit tests, execute the following command:

```bash
make test
```

## Makefile Commands

The `Makefile` includes the following commands:

- `make install`: Creates a virtual environment and installs the dependencies.
- `make run`: Starts the game.
- `make test`: Runs the unit tests.
- `make clean`: Removes temporary files and directories.
