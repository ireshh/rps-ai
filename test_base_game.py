import unittest
from unittest.mock import patch
from base_game import input_user_choice, input_computer_choice, who_wins, play_rps

class TestBaseGame(unittest.TestCase):

    @patch('builtins.input', side_effect=['r', 'p', 's'])
    def test_input_user_choice_valid(self, mock_input):
        self.assertEqual(input_user_choice(), 'r')
        self.assertEqual(input_user_choice(), 'p')
        self.assertEqual(input_user_choice(), 's')

    @patch('builtins.input', side_effect=['x', 'y', 'z', 'r'])
    def test_input_user_choice_invalid_then_valid(self, mock_input):
        self.assertEqual(input_user_choice(), 'r')
        self.assertEqual(mock_input.call_count, 4)

    def test_input_computer_choice(self):
        choices = ['r', 'p', 's']
        for _ in range(10):
            self.assertIn(input_computer_choice(), choices)

    def test_who_wins(self):
        self.assertEqual(who_wins('r', 'r'), "It's a tie!")
        self.assertEqual(who_wins('p', 'p'), "It's a tie!")
        self.assertEqual(who_wins('s', 's'), "It's a tie!")
        self.assertEqual(who_wins('r', 's'), "You win!")
        self.assertEqual(who_wins('s', 'p'), "You win!")
        self.assertEqual(who_wins('p', 'r'), "You win!")
        self.assertEqual(who_wins('s', 'r'), "Computer wins!")
        self.assertEqual(who_wins('p', 's'), "Computer wins!")
        self.assertEqual(who_wins('r', 'p'), "Computer wins!")

    @patch('builtins.input', side_effect=['r', 'n'])
    @patch('base_game.input_computer_choice', return_value='s')
    def test_play_rps_win_and_quit(self, mock_computer_choice, mock_input):
        with patch('builtins.print') as mock_print:
            play_rps()
            mock_print.assert_any_call("You chose: r")
            mock_print.assert_any_call("Computer chose: s")
            mock_print.assert_any_call("You win!")
            mock_print.assert_any_call("Thanks for playing! Goodbye!")

    @patch('builtins.input', side_effect=['p', 'y', 's', 'n'])
    @patch('base_game.input_computer_choice', side_effect=['p', 'r'])
    def test_play_rps_multiple_rounds(self, mock_computer_choice, mock_input):
        with patch('builtins.print') as mock_print:
            play_rps()
            mock_print.assert_any_call("You chose: p")
            mock_print.assert_any_call("Computer chose: p")
            mock_print.assert_any_call("It's a tie!")
            mock_print.assert_any_call("You chose: s")
            mock_print.assert_any_call("Computer chose: r")
            mock_print.assert_any_call("Computer wins!")
            mock_print.assert_any_call("Thanks for playing! Goodbye!")

if __name__ == "__main__":
    unittest.main()