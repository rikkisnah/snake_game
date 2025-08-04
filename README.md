# Snake Game

This is a simple implementation of the classic Snake game using Python and the Pygame library.

## Features

- The snake can move in four directions (up, down, left, right).
- The snake grows longer each time it eats food.
- The game ends if the snake collides with itself or the walls.
- The current score is displayed.
- A simple start and end screen.
- Keyboard controls for snake movement.

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

- Use the arrow keys (Up, Down, Left, Right) to control the snake.
- Press the `SPACE` bar to start the game.
- If you lose, press `C` to play again or `Q` to quit.

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
