import unittest
from unittest.mock import patch, call
import random
from main_game.base_game import (
    input_user_choice, input_computer_choice, who_wins, play_rps, past_choices,
    USER_WINS, COMPUTER_WINS, TIES
)
from main_game.multi_ai import MultiAI, WIN_CONDITIONS
from main_game.trie import Trie, RPSTrieNode

def custom_choice(seq):
    return seq[0] if seq and isinstance(seq[0], int) else 'p'

class TestBaseGame(unittest.TestCase):
    def setUp(self):
        past_choices.clear()
        global USER_WINS, COMPUTER_WINS, TIES
        USER_WINS = 0
        COMPUTER_WINS = 0
        TIES = 0

    @patch('builtins.input', side_effect=['r', 'p', 's'])
    def test_input_user_choice_valid(self, mock_input):
        for expected in ['r', 'p', 's']:
            self.assertEqual(input_user_choice(), expected)

    @patch('builtins.input', side_effect=['x', 'y', 'z', 'r'])
    def test_input_user_choice_invalid_then_valid(self, mock_input):
        self.assertEqual(input_user_choice(), 'r')
        self.assertEqual(mock_input.call_count, 4)

    @patch('main_game.multi_ai.MultiAI.get_computer_choice')
    def test_input_computer_choice(self, mock_get_choice):
        mock_get_choice.return_value = 'p'
        self.assertEqual(input_computer_choice(), 'p')

    @patch('random.choice', return_value='s')
    def test_input_computer_choice_short_history(self, mock_random):
        past_choices.append('r')
        self.assertEqual(input_computer_choice(), 's')

    def test_who_wins_logic(self):
        self.assertEqual(who_wins('r', 'r'), "It's a tie!")
        self.assertEqual(who_wins('r', 's'), "You win!")
        self.assertEqual(who_wins('s', 'r'), "Computer wins!")

    @patch('builtins.input', side_effect=['end'])
    def test_play_rps_immediate_quit(self, mock_input):
        with patch('builtins.print') as mock_print:
            play_rps()
            mock_print.assert_any_call("Thanks for playing!")
            self.assertNotIn('Final Score', [call[0][0] for call in mock_print.call_args_list])

    @patch('builtins.input', side_effect=['r', 'r', 'r', 'r', 'r', 'r', 'r', 'end'])
    @patch('main_game.base_game.input_computer_choice', return_value='p')
    def test_past_choices_length_management(self, mock_comp, mock_input):
        play_rps()
        self.assertEqual(len(past_choices), 6)

class TestMultiAI(unittest.TestCase):
    def setUp(self):
        self.ai = MultiAI()
        self.history = ['r', 'p', 's']

    def test_counter_move(self):
        self.assertEqual(self.ai.counter_move('r'), 'p')
        self.assertEqual(self.ai.counter_move('p'), 's')
        self.assertEqual(self.ai.counter_move('s'), 'r')

    def test_predict_user_move_insufficient_history(self):
        with patch('random.choice', return_value='r'):
            self.assertEqual(self.ai.predict_user_move(3, ['r', 'p']), 'r')

    def test_predict_user_move_unseen_sequence(self):
        with patch('random.choice', return_value='p'):
            self.assertEqual(self.ai.predict_user_move(2, ['r', 's']), 'p')

    def test_multi_ai_choice_default_order(self):
        self.ai.model_history = {1: [], 2: [], 3: [], 4: [], 5: []}
        choice, _ = self.ai.multi_ai_choice([])
        self.assertEqual(choice, self.ai.counter_move(random.choice(['r', 'p', 's'])))

    def test_update_after_round_score_calculation(self):
        with patch('random.choice', return_value='p'), \
             patch.object(self.ai, 'predict_user_move', return_value='r'):
            self.ai.update_after_round(['r', 'p', 's'], 's')
            for order in 1, 2, 3:
                self.assertEqual(self.ai.model_history[order][-1], 1)
            for order in 4, 5:
                self.assertEqual(self.ai.model_history[order][-1], -1)

    def test_multi_model_insertions(self):
        past_choices = ['r', 'p', 's', 'r', 'p']
        self.ai.update_after_round(past_choices, 's')
        for order in range(1, 6):
            if order <= 5:
                model = self.ai.multi_models[order]
                sequence = past_choices[-order:]
                node = model.root
                for move in sequence:
                    node = node.kids[move]
                self.assertEqual(node.counts['s'], 1)

class TestMultiAIExtended(unittest.TestCase):
    def test_predict_user_move_zero_counts(self):
        ai = MultiAI()
        ai.multi_models[3].root.kids['r'] = RPSTrieNode()  # Node with zero counts
        result = ai.predict_user_move(3, ['r', 'r', 'r'])
        self.assertIn(result, ['r', 'p', 's'])

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()

    def test_insert_valid_sequence(self):
        self.trie.insert(['r', 'p'], 's')
        self.assertFalse(self.trie.invalid_insertion_called)

    def test_insert_invalid_sequence(self):
        self.trie.insert(['r']*6, 'p')
        self.assertTrue(self.trie.invalid_insertion_called)

    def test_default_predict(self):
        self.assertIsNone(self.trie.predict(['r', 'p']))

    def test_node_counts(self):
        node = RPSTrieNode()
        node.counts['r'] = 5
        self.assertEqual(node.counts['r'], 5)

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['r', 'p', 'end'])
    @patch('main_game.base_game.input_computer_choice', return_value='p')
    def test_full_game_flow(self, mock_comp, mock_input):
        with patch('builtins.print') as mock_print:
            play_rps()
            mock_print.assert_any_call("You: r | Computer: p")
            mock_print.assert_any_call("Final Score")

if __name__ == "__main__":
    unittest.main()