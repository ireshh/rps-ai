"""
This is an implementation for a simple Rock-Paper-Scissors game
"""

import random

class RPSTrieNode:
    """Node for Trie data structure"""
    def __init__(self):
        self.kids = {}
        self.counts = {'r': 0, 'p': 0, 's': 0}

class Trie:
    """Trie data structure for storing sequences"""
    def __init__(self):
        self.root = RPSTrieNode()

    def insert(self, sequence, next_move):
        """Insert a sequence and track the next move frequency"""
        node = self.root
        for move in sequence:
            node = node.kids.setdefault(move, RPSTrieNode())
        node.counts[next_move] += 1

    def predict(self, sequence):
        """Predict the most likely next move based on history"""
        node = self.root
        for move in sequence:
            if move not in node.kids:
                return None
            node = node.kids[move]
        return max(node.counts, key=node.counts.get) if sum(node.counts.values()) > 0 else None

trie = Trie()
past_choices = []
USER_WINS = 0
COMPUTER_WINS = 0
TIES = 0

WIN_CONDITIONS = {('r', 's'), ('s', 'p'), ('p', 'r')}


def input_user_choice():
    """Get user input and validate choice"""
    choices = {'r', 'p', 's', 'end'}
    while (user_choice := input("Enter your choice (r, p, s, or end to quit): ").lower()) not in choices:
        print("Invalid choice. Please choose r, p, s, or end.")
    return user_choice


def input_computer_choice():
    """Determine basic AI choice based on past moves"""
    if len(past_choices) < 2:
        return random.choice(['r', 'p', 's'])

    predicted_move = trie.predict(past_choices[-5:])
    return {'r': 'p', 'p': 's', 's': 'r'}.get(predicted_move, random.choice(['r', 'p', 's']))


def who_wins(user_choice, computer_choice):
    """Determine round winner and keep score"""
    global USER_WINS, COMPUTER_WINS, TIES
    if user_choice == computer_choice:
        TIES += 1
        return "It's a tie!"
    if (user_choice, computer_choice) in WIN_CONDITIONS:
        USER_WINS += 1
        return "You win!"
    COMPUTER_WINS += 1
    return "Computer wins!"


def play_rps():
    """Main game loop for Rock-Paper-Scissors"""
    print("Welcome to Rock-Paper-Scissors with AI!")
    while True:
        user_choice = input_user_choice()
        if user_choice == 'end':
            total_games = USER_WINS + COMPUTER_WINS + TIES
            if total_games > 0:
                print(f"Final Score -> You: {USER_WINS} AI: {COMPUTER_WINS} Ties: {TIES}")
                print(f"Percentage -> You: {USER_WINS/total_games*100:.2f}% AI: {COMPUTER_WINS/total_games*100:.2f}% Ties: {TIES/total_games*100:.2f}%")
            print("Thanks for playing!")
            break

        computer_choice = input_computer_choice()
        print(f"You chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")
        print(who_wins(user_choice, computer_choice))
        print(f"Score -> You: {USER_WINS} AI: {COMPUTER_WINS} Ties: {TIES}")

        if len(past_choices) >= 6:
            past_choices.pop(0)
        past_choices.append(user_choice)

        for i in range(len(past_choices)):
            trie.insert(past_choices[:i+1], user_choice)

if __name__ == "__main__": # pragma: no cover
    play_rps()
