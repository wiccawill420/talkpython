import random
import json
import os
import datetime

rolls = {}


def main():
    log("App starting up")
    load_rolls()
    show_header()
    show_leaderboard()
    player1, player2 = get_players()
    log(f"{player1} has logged in.")
    play_game(player1, player2)
    log("Game Over")


def show_header():
    print("-----------------")
    print(" Rock Paper Scissors v3 ")
    print(" External file mode ")
    print("-----------------")


def show_leaderboard():
    leaders = load_leaders()

    sorted_names = list(leaders.items())
    sorted_names.sort(key=lambda l: l[1], reverse=True)

    print()
    print("Leaders: ")
    for name,wins in sorted_names[0:5]:
        print(f"{wins:,} -- {name}")
    print()
    print("-----------------")
    print()


def get_players():
    p1 = input("Player 1, what is your name? ")
    p2 = "Computer"

    return p1, p2


def play_game(player1, player2):
    log(f"New game starting between {player1} and {player2}")
    wins = {player1: 0, player2: 0}
    rolls_names = list(rolls.keys())

    while not find_winner(wins, wins.keys()):
        roll1 = get_roll(player1, rolls_names)
        roll2 = random.choice(rolls_names)

        if not roll1:
            print("Try again")
            continue

        log(f"Round: {player1} rolls {roll1} and {player2} rolls {roll2}")
        print(f"{player1} roll {roll1}")
        print(f"{player2} rolls {roll2}")

        winner = check_for_winner(player1, player2, roll1, roll2)

        if winner is None:
            msg = "This round was a tie!"
            print(msg)
            log(msg)
        else:
            msg = f"{winner} has won this round"
            print(msg)
            log(msg)
            wins[winner] += 1

        msg = f"Score is {player1}: {wins[player1]} and {player2}: {wins[player2]}"
        print(msg)
        log(msg)
        print()
    overall_winner = find_winner(wins, wins.keys())
    msg = f"{overall_winner} wins the game!"
    print(msg)
    log(msg)
    record_win(overall_winner)


def find_winner(wins, names):
    best_of = 3
    for name in names:
        if wins.get(name, 0) >= best_of:
            return name
    return None


def check_for_winner(player1, player2, roll1, roll2):
    winner = None
    if roll1 == roll2:
        print("The play was tied!")

    outcome = rolls.get(roll1, {})
    if roll2 in outcome.get('defeats'):
        return player1
    elif roll2 in outcome.get('defeated_by'):
        return player2


def get_roll(player_name, roll_names):
    print("Available rolls:")
    for index, r in enumerate(roll_names, start=1):
        print(f"{index}. {r}")

    text = input(f"{player_name}, what is your roll? [1-{len(rolls)}]: ")
    selected_index = int(text) - 1

    if selected_index < 0 or selected_index >= len(rolls):
        print(f"Sorry {player_name}, {text} is out of bounds")
        return None

    return roll_names[selected_index]


def load_rolls():
    global rolls

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'rolls.json')

    with open(filename, 'r', encoding='utf-8') as fin:
        rolls = json.load(fin)

    log(f"Loaded rolls: {list(rolls.keys())} from {os.path.basename(filename)}")


def load_leaders():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json')

    if not os.path.exists(filename):
        return {}

    with open(filename, 'r', encoding='utf-8') as fin:
        return json.load(fin)


def record_win(winner_name):
    leaders = load_leaders()

    if winner_name in leaders:
        leaders[winner_name] += 1
    else:
        leaders[winner_name] = 1

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json')

    with open(filename, 'w', encoding='utf-8') as fout:
        json.dump(leaders, fout)


def log(msg):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'rps.log')

    with open(filename, 'a', encoding='utf-8') as fout:
        fout.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ")
        fout.write(msg)
        fout.write('\n')


if __name__ == '__main__':
    main()
