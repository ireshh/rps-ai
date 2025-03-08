# Implementation Document

## General Structure of the Program

I have structured the program into several main components:

1. **Main Game Logic**:  
   This is Implemented in `base_game.py`, it controls the basic game loop. This module handles:
   - User input validation (accepts nothing but `r`, `p`, `s`, or `end`).
   - Calling the AI module to derive a move.
   - Determining the round outcome based on pre-set win conditions.
   - and lastly managing the game state (for example - updating scores, move history trimming, and final score reporting)

2. **AI Logic**:  
   I have implemented this in `multi_ai.py` and `trie.py`, in which the AI uses a trie-based approach to predict the user’s next move using markov chains. This includes:
   - The `MultiAI` class maintaining multiple trie models (orders 1 to 5) to 'remember' different lengths of the user’s move history.
   - The `predict_user_move` method being able to traverse the trie for a given order and return a weighted outcome based on past counts.
   - The `update_after_round` method updates model performance each round by scoring each model’s counter move with either +1 or -1 or 0 and then inserts the new sequence into the respective trie.
   - The `Trie` class is able to store valid move sequences (only those that result in a total length between 2 and 6) along with their frequency for each possible next move.

3. **Command Line Interface (GUI) –  GUI Future Work**:  
   The game currently runs in the command line (CLI).

4. **Testing**:  
   The project includes comprehensive unit tests to check key functions:
   - `test_base_game.py` verifies user input handling, game flow, outcome determination, and history management.
   - `test_multi_ai.py` exercises AI prediction logic, counter move generation, score tracking, and trie updates.
   - `test_trie.py` tests the integrity and proper functioning of the trie data structure (including valid and invalid sequence insertions into tries).

## Time and Space Complexities

- **Main Game Logic**:
  Each game round operates in O(1) time as it involves fixed-time input processing, simple condition checks, and constant-time updates to game state.

- **AI Logic**:  
  - The `predict_user_move` method in the `MultiAI` class has O(n) time complexity (with n corresponding to the order of the model, from 1 to 5).
  - The `insert` method in `Trie` operates in O(k) time, where k is the length of the move sequence (restricted to lengths between 2 and 6).

- **Space Complexity**:  
  The trie models require O(m * k) space, with m being the total number of stored sequences and k the average length per sequence.

## Performance and Big O Analysis Comparison

This markov chain approach for predicting the user’s next move offers a fast mechanism for:

- Firstly, storing and querying user move sequences.
- Improving prediction accuracy over a simple random choice strategy over time.

## Potential Shortcomings and Suggested Improvements

- **Shortcomings**:
  - The AI’s performance depends fully on the existence of non random user move patterns. Against a completely random user, prediction accuracy is useless.

- **Suggested Improvements**:
  - Maybe combine into the game multiple prediction strategies to further improve accuracy.
  - When implementing the GUI, include visual representations of the AI’s learning progress and move statistics.
  - Optimize the trie data structure further to reduce memory usage and enhance update speeds.

## References

- Multi‑AI competing and winning against humans in iterated Rock‑Paper‑Scissors game: <https://arxiv.org/pdf/2003.06769>
