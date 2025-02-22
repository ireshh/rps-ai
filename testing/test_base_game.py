"""unit tests for base_game module"""
import unittest
from unittest.mock import patch
import importlib
import main_game.base_game as base_game

class TestBaseGame(unittest.TestCase):
    """test cases for core logic"""
    
    def setUp(self):
        """initialize fresh game state"""
        self.base_game = importlib.reload(base_game)
        self.base_game.past_choices.clear()
        self.base_game.USER_WINS = 0
        self.base_game.COMPUTER_WINS = 0
        self.base_game.TIES = 0

    @patch('builtins.input', side_effect=['r', 'p', 's'])
    def test_valid_inputs(self, mock_input):
        """test valid user inputs"""
        self.assertEqual(self.base_game.input_user_choice(), 'r')
        self.assertEqual(self.base_game.input_user_choice(), 'p')
        self.assertEqual(self.base_game.input_user_choice(), 's')

    @patch('builtins.input', side_effect=['x', 'y', 'z', 'r'])
    def test_invalid_input_recovery(self, mock_input):
        """test invalid inputs"""
        self.assertEqual(self.base_game.input_user_choice(), 'r')
        self.assertEqual(mock_input.call_count, 4)

    @patch('main_game.multi_ai.MultiAI.get_computer_choice')
    def test_computer_choice_proxy(self, mock_get_choice):
        """test computer choice"""
        mock_get_choice.return_value = 'p'
        self.assertEqual(self.base_game.input_computer_choice(), 'p')

    @patch('random.choice', return_value='s')
    def test_short_history_choice(self, mock_random):
        """test computer choice with little history"""
        self.base_game.past_choices.append('r')
        self.assertEqual(self.base_game.input_computer_choice(), 'r')

    def test_outcome_determination(self):
        """test all outcomes"""
        outcomes = {
            ('r', 'r'): "You Tied!",
            ('r', 's'): "You Win :)",
            ('s', 'r'): "Computer Wins :(",
        }
        for (user, comp), expected in outcomes.items():
            with self.subTest(user=user, comp=comp):
                self.assertEqual(self.base_game.who_wins(user, comp), expected)

    @patch('builtins.input', side_effect=['end'])
    def test_immediate_exit_flow(self, mock_input):
        """test game exit without playing any rounds"""
        with patch('builtins.print') as mock_print:
            self.base_game.play_rps()
            outputs = [call[0][0] for call in mock_print.call_args_list]
            self.assertNotIn("Final Score", " ".join(outputs))

    @patch('builtins.input', side_effect=['r', 'p', 'end'])
    @patch('main_game.base_game.input_computer_choice', return_value='p')
    def test_full_game_flow(self, mock_comp, mock_input):
        """test full game session with scores"""
        with patch('builtins.print') as mock_print:
            self.base_game.play_rps()
            outputs = [call[0][0] for call in mock_print.call_args_list]
            self.assertTrue(any("Final Score ->" in s for s in outputs))

    @patch('builtins.input', side_effect=['r', 'r', 'r', 'r', 'r', 'r', 'r', 'end'])
    @patch('main_game.base_game.input_computer_choice', return_value='p')
    def test_history_management(self, mock_comp, mock_input):
        """test past choices list length"""
        self.base_game.play_rps()
        self.assertEqual(len(self.base_game.past_choices), 6)

if __name__ == "__main__":
    unittest.main()
