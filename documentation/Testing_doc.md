# Testing Document

## Coverage Report

Name                     Stmts   Miss  Cover

--------------------------------------------

main_game\__init__.py        0      0   100%

main_game\base_game.py      43      0   100%

main_game\multi_ai.py       55      0   100%

main_game\trie.py           16      0   100%

--------------------------------------------

TOTAL                      114      0   100%

## Tested Components

### Main Game Logic (`base_game.py`)

- **Input Validation:**  
  - The tests ensure user inputs are limited to `r`, `p`, `s`, or `end`.  
  - They ensure the program recovers from invalid inputs.

- **Outcome Determination:**  
  - The tests compares user and computer moves using predefined win conditions.  
  - They test updating global scores (user wins, computer wins, ties).

- **Game State Management:**  
  - They test maintaining and triming past user choices.
  - They also test displaying round results and final score statistics when the game ends.

### AI Logic (`multi_ai.py` and `trie.py`)

- **AI Predictions and Counter Moves:**  
  - We test for `MultiAI.predict_user_move` being able to navigate trie structures to return weighted predictions based on past data.
  - We also test for `MultiAI.counter_move` being able to correctly return a counter move for any given user choice.
  - Also tested that `MultiAI.update_after_round` updates model performance scores and is able to store new move sequences.

- **Trie Functionality:**  
  - We test `Trie` class accepting valid sequences (total length between 2 and 6) and updating frequency counts.
  - Handling of invalid insertions is also verified via the `invalid_insertion_called` flag.
  - Tested trie nodes are being correctly initialized and managed.

### Testing Infrastructure

- **Methodology:**  
  - Tests are executed via Python’s `unittest` framework.
  - `unittest.mock` is used to simulate user input.
  - Coverage is monitored using `coverage.py` and some analysis with pylint.

## Repeating Tests

### Steps to Repeat Tests

1. Open a terminal in the project root (`~\rps-ai\`).
2. Run the tests with:

   ```bash
   poetry run pytest --cov
   ```

3. To generate a detailed coverage report, run:

   ```bash
   poetry run coverage report -m
   ```

## Conclusion

The testing makes sure that thorough unit tests happen and keep the project working well throughout its development. This combined with integration tests ensure that the game logic, AI predictions, and trie operations function as expected.
