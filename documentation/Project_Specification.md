# Rock-Paper-Scissors AI Bot

**Degree Program**: Bachelor's Programme in Science (BSc)

**Project Language**: Python

**Project Documentation Language**: English

## Overview

The goal of my project is to develop a Rock-Paper-Scissors-playing bot fully capable of playing Rock-Paper-Scissor against an opponent.
By using predictive algorithms, the bot will be able to analyze how the opponents play against it and build on that, creating strategies guided by AI algorithms to reduce the chances of losing.

## What problem are you solving?

This project will hopefully lead to the creation of an AI bot that learns its opponent's moves and adapts in a competitive game of RPS. The AI will:

1. **Recognize Patterns**: Using Markov Chains to predict the opponent's next move based on their previous moves.
2. **Adapt Strategy**: Dynamically counter the predicted moves with the aim of maximizing the win rate.

I will also implement a simple randomized choice AI that will act as a control which will help measure the efficiency of my AI.

## What algorithms and data structures are you implementing in your work?

This project will implement the following algorithms and data structures:

1. **Markov Chains**: Model state transitions based off previous moves to predict the opponents next move.
    - **Data Structure**: A transition matrix will be stored as a dictionary, allowing me to map each move to a probability distribution over the possible next moves.

2. **Randomized Choice**: Provide a simple AI that randomly chooses moves with equal probability to measure the effectiveness of the AI.

3. **Game Logic**: To implement the simple rules of RPS and decide on the outcomes of every round.

## What inputs does your program take, and how are these used?

I will implement the following input systems:

- **User's Moves**: The moves the player can make: Rock, Paper, or Scissors.
- **Game Parameters**: The number of rounds to be played can be specified or it can continue infinitely until the program is manually terminated.
This will be implemented as a CLI(maybe upgrade to GUI if possible).

Those inputs are going to be used to:

1. **Update Game History**: Store and analyze previous moves for pattern recognition.
2. **Predict Moves**: Use a Markov Chain model to predict the next move based on those observed patterns.
3. **Make Decisions**: Allow the AI to create moves to counter the predicted move or choose randomly when needed.

All feedback is welcome :D
