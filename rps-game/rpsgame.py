import random


def main():
    show_header()

    play_game("You", "Computer")


def show_header():
    print("-----------------")
    print(" Rock Paper Scissors v1 ")
    print("-----------------")


def play_game(player1, player2):
    rounds = 3
    wins_p1 = 0
    wins_p2 = 0

    rolls = ['rock', 'paper', 'scissors']

    while wins_p1 < rounds and wins_p2 < rounds:
        roll1 = get_roll(player1, rolls)
        roll2 = random.choice(rolls)

        if not roll1:
            print("Try again")
            continue

        print(f"{player1} roll {roll1}")
        print(f"{player2} rolls {roll2}")

        winner = check_for_winner(player1, player2, roll1, roll2)

        if winner is None:
            print("This round was a tie!")
        else:
            print(f"{winner} has won this round")
            if winner == player1:
                wins_p1 += 1
            if winner == player2:
                wins_p2 += 1

        print(f"Score is {player1}: {wins_p1} and {player2}: {wins_p2}")
        print()
    overall_winner = None
    if wins_p1 >= rounds:
        overall_winner = player1
    else:
        overall_winner = player2

    print(f"{overall_winner} wins the game!")


def check_for_winner(player1, player2, roll1, roll2):
    winner = None
    if roll1 == roll2:
        print("The play was tied!")
    elif roll1 == 'rock':
        if roll2 == 'paper':
            winner = player2
        elif roll2 == 'scissors':
            winner = player1
    elif roll1 == 'paper':
        if roll2 == 'scissors':
            winner = player2
        elif roll2 == 'rock':
            winner = player1
    elif roll1 == 'scissors':
        if roll2 == 'rock':
            winner = player2
        elif roll2 == 'paper':
            winner = player1
    return winner


def get_roll(player_name, rolls):
    print("Available rolls:")
    for index, r in enumerate(rolls, start=1):
        print(f"{index}. {r}")

    text = input(f"{player_name}, what is your roll? [rock, paper, scissors]: ")
    selected_index = int(text) - 1

    if selected_index < 0 or selected_index >= len(rolls):
        print(f"Sorry {player_name}, {text} is out of bounds")
        return None

    return rolls[selected_index]


if __name__ == '__main__':
    main()
