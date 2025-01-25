"""
This is an implementation for a simple Rock-Paper-Scissors game.
"""

import random

def input_user_choice():
    """
    Ask the user to enter their choice and validate input.

    """
    choice = ['r', 'p', 's']
    while True:
        user_choice = input("Enter your choice (r, p, s): ").lower()
        if user_choice in choice:
            return user_choice
        print("Invalid choice. Please choose r, p, or s.")

def input_computer_choice():
    """
    Randomly select the computer's choice for now until we develop AI.

    """
    return random.choice(['r', 'p', 's'])

def who_wins(user_choice, computer_choice):
    """
    Determine winner of the Rock-Paper-Scissors game.

    """
    if user_choice == computer_choice:
        return "It's a tie!"
    if (
        (user_choice == 'r' and computer_choice == 's') or
        (user_choice == 's' and computer_choice == 'p') or
        (user_choice == 'p' and computer_choice == 'r')
    ):
        return "You win!"
    return "Computer wins!"

def play_rps():
    """
    Run the Rock-Paper-Scissors loop.
    """
    print("Welcome to Rock-Paper-Scissors!")
    while True:
        user_choice = input_user_choice()
        computer_choice = input_computer_choice()
        print(f"You chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")
        print(who_wins(user_choice, computer_choice))

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again not in ['y', 'yes']:
            print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    play_rps()
