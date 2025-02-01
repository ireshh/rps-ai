"""
Unit tests for main game
"""

import unittest
from unittest.mock import patch
from base_game import input_user_choice, input_computer_choice, who_wins, play_rps, trie, past_choices

class TestBaseGame(unittest.TestCase):
    """Tests for the main game"""

    def setUp(self):
        """Setting up the environment"""
        past_choices.clear()
        self.user_wins = self.computer_wins = self.ties = 0

    @patch('builtins.input', side_effect=['r', 'p', 's'])
    def test_input_user_choice_valid(self, mock_input):
        """Test valid user choices"""
        for choice in ['r', 'p', 's']:
            self.assertEqual(input_user_choice(), choice)

    @patch('builtins.input', side_effect=['x', 'y', 'z', 'r'])
    def test_input_user_choice_invalid_then_valid(self, mock_input):
        """Test invalid user choices followed by a valid"""
        self.assertEqual(input_user_choice(), 'r')
        self.assertEqual(mock_input.call_count, 4)

    def test_input_computer_choice(self):
        """Test computer choice"""
        self.assertIn(input_computer_choice(), ['r', 'p', 's'])
        past_choices.append('r')
        self.assertIn(input_computer_choice(), ['r', 'p', 's'])

    @patch('base_game.trie.predict', return_value=None)
    def test_input_computer_choice_with_no_prediction(self, mock_predict):
        """Test computer choice with no prediction"""
        self.assertIn(input_computer_choice(), ['r', 'p', 's'])

    @patch('random.choice', return_value='p')
    def test_input_computer_choice_short_past_moves(self, mock_random_choice):
        """Test computer choice with short past moves"""
        self.assertEqual(input_computer_choice(), 'p')
        past_choices.append('r')
        self.assertEqual(input_computer_choice(), 'p')

    @patch('base_game.trie.predict', return_value='r')
    @patch('random.choice')
    def test_input_computer_choice_with_prediction(self, mock_random_choice, mock_predict):
        """Test computer choice with prediction"""
        past_choices.extend(['r', 'p', 's', 'r', 'p'])
        self.assertEqual(input_computer_choice(), 'p')
        mock_predict.assert_called_with(['r', 'p', 's', 'r', 'p'])

    @patch('base_game.trie.predict', return_value=None)
    @patch('random.choice', return_value='s')
    def test_input_computer_choice_no_prediction(self, mock_random_choice, mock_predict):
        """Test computer choice with no prediction"""
        past_choices.extend(['r', 'p', 's', 'r', 'p'])
        self.assertEqual(input_computer_choice(), 's')
        mock_predict.return_value = 'x'
        self.assertEqual(input_computer_choice(), 's')

    def test_who_wins(self):
        """Test the outcome of the game"""
        outcomes = {
            ('r', 'r'): "It's a tie!", ('p', 'p'): "It's a tie!", ('s', 's'): "It's a tie!",
            ('r', 's'): "You win!", ('s', 'p'): "You win!", ('p', 'r'): "You win!",
            ('s', 'r'): "Computer wins!", ('p', 's'): "Computer wins!", ('r', 'p'): "Computer wins!"
        }
        for (user, comp), result in outcomes.items():
            self.assertEqual(who_wins(user, comp), result)

    @patch('builtins.input', side_effect=['r', 'end'])
    @patch('base_game.input_computer_choice', return_value='s')
    def test_play_rps_win_and_quit(self, mock_computer_choice, mock_input):
        """Test playing the game, win and end"""
        with patch('builtins.print') as mock_print:
            play_rps()
            mock_print.assert_any_call("You win!")
            mock_print.assert_any_call("Thanks for playing!")

    @patch('builtins.input', side_effect=['p', 's', 'end'])
    @patch('base_game.input_computer_choice', side_effect=['p', 'r'])
    def test_play_rps_multiple_rounds(self, mock_computer_choice, mock_input):
        """Test playing multiple rounds of the game"""
        with patch('builtins.print') as mock_print:
            play_rps()
            mock_print.assert_any_call("It's a tie!")
            mock_print.assert_any_call("Computer wins!")

    @patch('builtins.input', side_effect=['end'])
    def test_play_rps_exit_immediately(self, mock_input):
        """Test exiting the game immediately"""
        with patch('builtins.print') as mock_print:
            play_rps()
            mock_print.assert_any_call("Thanks for playing!")

    def test_trie_insert_and_predict(self):
        """Test trie insertion and prediction"""
        trie.insert(['r', 'p'], 's')
        trie.insert(['r', 'p'], 's')
        trie.insert(['r', 'p'], 'r')
        self.assertEqual(trie.predict(['r', 'p']), 's')

    def test_trie_predict_no_history(self):
        """Test trie prediction with no history"""
        self.assertIsNone(trie.predict(['x', 'y', 'z']))

    def test_past_moves_tracking(self):
        """Test tracking of past moves"""
        past_choices.extend(['r', 'p'])
        self.assertEqual(past_choices, ['r', 'p'])

    @patch('builtins.input', side_effect=['r', 'p', 's', 'r', 'p', 's', 'r', 'end'])
    @patch('base_game.input_computer_choice', return_value='s')
    def test_past_moves_management(self, mock_computer_choice, mock_input):
        """Test management of past moves"""
        with patch('builtins.print'):
            play_rps()
        self.assertEqual(past_choices, ['p', 's', 'r', 'p', 's', 'r'])

    @patch('builtins.input', side_effect=['r', 'p', 's', 'end'])
    @patch('base_game.input_computer_choice', return_value='s')
    def test_trie_insertion_during_play(self, mock_computer_choice, mock_input):
        """Test trie insertion during gameplay"""
        with patch('builtins.print'):
            play_rps()
        self.assertEqual(trie.predict(['r']), 'r')
        self.assertEqual(trie.predict(['r', 'p']), 's')
        self.assertEqual(trie.predict(['r', 'p', 's']), 's')

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
