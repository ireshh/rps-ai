"""unit tests for the AI decision logic"""
import unittest
from unittest.mock import patch, call
from main_game.multi_ai import MultiAI, POSSIBLE_MOVES
from main_game.trie import RPSTrieNode

class TestMultiAI(unittest.TestCase):
    """test cases for MultiAI prediction and learning logic"""
    def setUp(self):
        """initialize AI for each test"""
        self.ai = MultiAI()

    def test_counter_move_logic(self):
        """test move counter strategy"""
        counters = {'r': 'p', 'p': 's', 's': 'r'}
        for move, expected in counters.items():
            with self.subTest(move=move):
                self.assertEqual(self.ai.counter_move(move), expected)

    @patch('random.choice')
    def test_prediction_edge_cases(self, mock_choice):
        """test prediction in edge cases"""
        mock_choice.side_effect = ['r', 'p']
        self.assertEqual(self.ai.predict_user_move(3, ['r', 'p']), 'r')
        self.assertEqual(self.ai.predict_user_move(2, ['r', 's']), 'p')
        mock_choice.assert_has_calls([
            call(['r', 'p', 's']),
            call(['r', 'p', 's'])
        ])

    def test_model_selection(self):
        """test model selection logic"""
        self.ai.model_history = {1: [1], 2: [-1], 3: [0], 4: [], 5: []}
        choice, _ = self.ai.multi_ai_choice(['r', 'p', 's'])
        self.assertIn(choice, POSSIBLE_MOVES)

    @patch.object(MultiAI, 'predict_user_move', return_value='r')
    def test_score_tracking(self, _):
        """test model scoring"""
        self.ai.update_after_round(['r', 'p', 's'], 's')
        self.assertEqual(self.ai.model_history[1][-1], -1)

    def test_trie_updates(self):
        """test sequence storing in trie"""
        sequence = ['r', 'p', 's', 'r', 'p']
        self.ai.update_after_round(sequence, 's')
        for order in range(1, 6):
            if order <= len(sequence):
                node = self.ai.multi_models[order].root
                for move in sequence[-order:]:
                    node = node.kids[move]
                self.assertEqual(node.counts['s'], 1)

class TestAIIntegration(unittest.TestCase):
    """integration tests for AI"""
    
    def test_zero_count_prediction(self):
        """test prediction with empty count node"""
        ai = MultiAI()
        ai.multi_models[2].root.kids['r'] = RPSTrieNode()
        with patch('random.choice', return_value='s'):
            self.assertEqual(ai.predict_user_move(2, ['r', 'r']), 's')

    def test_full_path_zero_counts(self):
        """test prediction with existing path but no count"""
        ai = MultiAI()
        node = ai.multi_models[3].root
        for move in ['r', 'r', 'r']:
            node = node.kids.setdefault(move, RPSTrieNode())
        with patch('random.choice', return_value='p'):
            self.assertEqual(ai.predict_user_move(3, ['r', 'r', 'r']), 'p')

if __name__ == "__main__":
    unittest.main()