"""
this contains Trie class for RPS game
"""

class RPSTrieNode:
    """trie node with move children and counts"""
    def __init__(self):
        self.kids = {}
        self.counts = {'r': 0, 'p': 0, 's': 0}
    def get_kids(self):
        """return the children of this node"""
        return self.kids

class Trie:
    """stores move sequences; only accepts history+move lengths of 2-6"""
    def __init__(self):
        self.root = RPSTrieNode()
        self.invalid_insertion_called = False

    def insert(self, sequence, next_move):
        """if valid this inserts a sequence with the next move into trie"""
        if not 2 <= len(sequence) + 1 <= 6:
            self.invalid_insertion_called = True
            return
        node = self.root
        for move in sequence:
            node = node.kids.setdefault(move, RPSTrieNode())
        node.counts[next_move] += 1
