# AI Rock Paper Scissors

A Rock Paper Scissors game that uses AI to learn from your play patterns using markov chain algorithms.

## Features

- You can play Rock Paper Scissors against an AI opponent :D
- Features multiple AI models that learn from your previous moves
- Adaptive gameplay that becomes more challenging over time
- Detailed statistics tracking your performance

## Installation

This project uses Poetry for dependency management. To install:

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install the project
git clone https://github.com/ireshh/rps-ai.git
cd rps-ai
poetry install
```

## Playing the Game

```bash
# Run the game
poetry run rps
```

Enter 'r' for rock, 'p' for paper, 's' for scissors, or 'end' to quit.

## Development

```bash
# Run tests
poetry run pytest --cov
```

The longer you play, the smarter the AI becomes!
