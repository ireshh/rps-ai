# Rock-Paper-Scissors AI Bot – User Guide

## Overview

I created a Rock-Paper-Scissors game that uses AI to learn and counter your moves and is implemented in Python. The bot uses a trie-based algorithm with Markov chain principles to predict your move and responds.

## Installation and Setup

The project uses [Poetry](https://python-poetry.org/) for dependency management. Set up the project:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ireshh/rps-ai.git
   cd rps-ai
   ```

2. **Install Poetry (if not already installed)**

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install Project Dependencies**

   ```bash
   poetry install
   ```

## Running the Game

To start playing, execute the following command from the project root:

```bash
poetry run rps
```

When you launch, the game will display a simple interface and instructions for input.

### Testing

- **Testing Framework:**  
  The project uses Python's `unittest` framework along with `pytest` and `coverage.py` to ensure thorough testing.
- **Running Tests:**
  - To run all tests:

    ```bash
    poetry run pytest --cov
    ```
  
  - For a detailed terminal report:

    ```bash
    poetry run coverage report -m
    ```
  
  - To generate an HTML version of the report:
  
    ```bash
    poetry run coverage html
    ```

## Accepted Input Formats

- **Valid Inputs:**
  - `r` for Rock  
  - `p` for Paper  
  - `s` for Scissors  
  - `end` to quit the game

Have fun enjoying my project!
