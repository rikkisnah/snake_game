import unittest
import pygame
from unittest.mock import MagicMock, patch
from snake_game import our_snake, gameLoop

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.snake_block = 20

    def tearDown(self):
        pygame.quit()

    @patch('snake_game.pygame.draw.rect')
    def test_our_snake(self, mock_draw_rect):
        # Define a snake list
        snake_list = [[100, 100], [120, 100], [140, 100]]

        # Call the our_snake function
        our_snake(self.snake_block, snake_list)

        # Assert that pygame.draw.rect was called for each segment of the snake
        self.assertEqual(mock_draw_rect.call_count, len(snake_list))

    @patch('snake_game.pygame.event.get')
    def test_gameLoop_exit(self, mock_event_get):
        # Mock the quit event
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]

        # Run the game loop and assert it raises SystemExit
        with self.assertRaises(SystemExit):
            gameLoop()

if __name__ == '__main__':
    unittest.main()
