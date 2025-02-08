"""
this is the implementation for a AI Rock-Paper-Scissors game
"""

from multi_ai import MultiAI

multi_ai = MultiAI()
past_choices = []
WIN_CONDITIONS = {('r', 's'), ('s', 'p'), ('p', 'r')}

USER_WINS = 0
COMPUTER_WINS = 0
TIES = 0

def input_computer_choice():
    """return AI move based on past choices"""
    return multi_ai.get_computer_choice(past_choices)

def input_user_choice():
    """prompt user until valid choice is made"""
    valid = {'r', 'p', 's', 'end'}
    while (choice := input("Enter (r, p, s, or end): ").lower()) not in valid:
        print("Invalid choice. Please choose r, p, s, or end.")
    return choice

def who_wins(user, comp):
    global USER_WINS, COMPUTER_WINS, TIES
    """return outcome text & update scores"""
    if user == comp:
        TIES += 1
        return "You Tied!"
    if (user, comp) in WIN_CONDITIONS:
        USER_WINS += 1
        return "You Win :)"
    COMPUTER_WINS += 1
    return "Computer Wins :("

def play_rps():
    """run main game loop until the user quits"""
    print("Rock-Paper-Scissors with AI!")
    while True:
        user = input_user_choice()
        if user == 'end':
            total = USER_WINS + COMPUTER_WINS + TIES
            if total:
                print(f"Final Score -> You: {USER_WINS} AI: {COMPUTER_WINS} Ties: {TIES}")
                print(
                    "Percentages -> "
                    f"You: {USER_WINS/total*100:.2f}% "
                    f"AI: {COMPUTER_WINS/total*100:.2f}% "
                    f"Ties: {TIES/total*100:.2f}%"
                )
            print("Thank you for playing!")
            break
        comp = input_computer_choice()
        print(f"You: {user}")
        print(f"Computer: {comp}")
        print(who_wins(user, comp))
        print(
            f"Score -> You: {USER_WINS} "
            f"AI: {COMPUTER_WINS} "
            f"Ties: {TIES}"
        )
        multi_ai.update_after_round(past_choices, user)
        if len(past_choices) >= 6:
            past_choices.pop(0)
        past_choices.append(user)

if __name__ == "__main__":  # pragma: no cover
    play_rps()
