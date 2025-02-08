"""
multi AI module for Rock, Paper, Scissors game
"""

import random
from trie import Trie

WIN_CONDITIONS = {('r', 's'), ('s', 'p'), ('p', 'r')}

class MultiAI:
    """AI that predicts user moves for RPS"""

    def __init__(self):
        """initialize AI with multiple trie models"""
        self.focus_length = 5
        self.multi_models = {order: Trie() for order in range(1, 6)}
        self.model_history = {order: [] for order in range(1, 6)}

    def counter_move(self, move):
        """return the counter to the user's move"""
        return {'r': 'p', 'p': 's', 's': 'r'}.get(move, random.choice(['r', 'p', 's']))

    def predict_user_move(self, order, past_choices):
        """predict user move based on past choicess"""
        if len(past_choices) < order:
            return random.choice(['r', 'p', 's'])
        sequence = past_choices[-order:]
        node = self.multi_models[order].root
        for move in sequence:
            if move not in node.kids:
                return random.choice(['r', 'p', 's'])
            node = node.kids[move]
        total = sum(node.counts.values())
        if total == 0:
            ret = random.choice(['r', 'p', 's'])
            return ret
        moves = ['r', 'p', 's']
        weights = [node.counts[m] for m in moves]
        return random.choices(moves, weights=weights, k=1)[0]

    def multi_ai_choice(self, past_choices):
        """return move from the best-performing model"""
        rec_moves = {}
        for order in range(1, 6):
            if len(past_choices) >= order:
                predicted = self.predict_user_move(order, past_choices)
                rec_moves[order] = self.counter_move(predicted)
            else:
                rec_moves[order] = random.choice(['r', 'p', 's'])
        cumulative = {order: sum(self.model_history[order]) for order in range(1, 6)}
        chosen_order = (
            1 if all(score == 0 for score in cumulative.values())
            else random.choice([o for o, s in cumulative.items()
                                if s == max(cumulative.values())])
        )
        return rec_moves[chosen_order], rec_moves

    def get_computer_choice(self, past_choices):
        """get the AI move"""
        return self.multi_ai_choice(past_choices)[0]

    def update_after_round(self, past_choices, user_choice):
        """update each model performance after every round"""
        rec_moves = {}
        for order in range(1, 6):
            if len(past_choices) >= order:
                predicted = self.predict_user_move(order, past_choices)
                rec_moves[order] = self.counter_move(predicted)
            else:
                rec_moves[order] = random.choice(['r', 'p', 's'])
            score = 0 if rec_moves[order] == user_choice else \
                    1 if (rec_moves[order], user_choice) in WIN_CONDITIONS else -1
            self.model_history[order].append(score)
            if len(self.model_history[order]) > self.focus_length:
                self.model_history[order].pop(0)
        prev_seq = past_choices.copy()
        for order in range(1, 6):
            if len(prev_seq) >= order:
                self.multi_models[order].insert(prev_seq[-order:], user_choice)
