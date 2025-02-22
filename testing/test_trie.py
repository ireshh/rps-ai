"""unit tests for Trie"""
import unittest
from main_game.trie import Trie, RPSTrieNode

class TestTrie(unittest.TestCase):
    """test cases for RPS Trie"""
    def setUp(self):
        """initialize fresh Trie"""
        self.trie = Trie()

    def test_valid_insert_operations(self):
        """test valid sequence insertions"""
        self.trie.insert(['r', 'p'], 's')
        node = self.trie.root.kids['r'].kids['p']
        self.assertEqual(node.counts['s'], 1)

    def test_invalid_insert_handling(self):
        """test invalid sequence insertions"""
        self.trie.insert(['r']*6, 'p')
        self.assertTrue(self.trie.invalid_insertion_called)

    def test_node_initial_state(self):
        """test trie node initializing values"""
        node = RPSTrieNode()
        self.assertEqual(node.counts['r'], 0)
        self.assertEqual(node.counts['p'], 0)

    def test_depth_management(self):
        """test sequence length"""
        self.trie.insert(['r', 'p', 's', 'r', 'p'], 's')
        self.assertFalse(self.trie.invalid_insertion_called)
        self.trie.insert(['r', 'p', 's', 'r', 'p', 's'], 'r')
        self.assertTrue(self.trie.invalid_insertion_called)

if __name__ == "__main__":
    unittest.main()
