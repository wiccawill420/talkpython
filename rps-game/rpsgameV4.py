import random
import json
import os
import datetime
from colorama import Fore
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completer, Completion

rolls = {}


def main():
    print(Fore.WHITE)
    log("App starting up")
    load_rolls()
    show_header()
    show_leaderboard()
    player1, player2 = get_players()
    log(f"{player1} has logged in.")
    play_game(player1, player2)
    log("Game Over")


def show_header():
    print(Fore.MAGENTA)
    print("-----------------")
    print(" Rock Paper Scissors v4 ")
    print(" External packages addition ")
    print("-----------------")
    print(Fore.WHITE)


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
            print(Fore.LIGHTRED_EX + "Try again")
            print(Fore.WHITE)
            continue

        log(f"Round: {player1} rolls {roll1} and {player2} rolls {roll2}")
        print(Fore.YELLOW + f"{player1} rolls {roll1}")
        print(Fore.LIGHTBLUE_EX + f"{player2} rolls {roll2}")
        print(Fore.WHITE)

        winner = check_for_winner(player1, player2, roll1, roll2)

        if winner is None:
            msg = "This round was a tie!"
            print(msg)
            log(msg)
        else:
            msg = f"{winner} has won this round"
            fore = Fore.GREEN if winner == player1 else Fore.LIGHTRED_EX
            print(fore + msg + Fore.WHITE)
            log(msg)
            wins[winner] += 1

        msg = f"Score is {player1}: {wins[player1]} and {player2}: {wins[player2]}"
        print(msg)
        log(msg)
        print()
    overall_winner = find_winner(wins, wins.keys())
    msg = f"{overall_winner} wins the game!"
    fore = Fore.GREEN if overall_winner == player1 else Fore.LIGHTRED_EX
    print(fore + msg + Fore.WHITE)
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
    if os.environ.get('PYCHARM_HOSTED') == "1":
        print(Fore.LIGHTRED_EX + "Warning: Cannot use fancy prompt from pycharm")
        print("Run this app outside pycharm to see its full glory")
        print(Fore.LIGHTYELLOW_EX + f"Available rolls: {', '.join(roll_names)}.")
        val = input(Fore.LIGHTYELLOW_EX + "What is your roll: ")
        print(Fore.WHITE)
        return val

    print(f"Available rolls: {', '.join(roll_names)}.")

    # word_comp = WordCompleter(roll_names)
    # word_comp = WordCompleter(roll_names)
    word_comp = PlayComplete()

    roll = prompt(f"{player_name}, what is your roll: ", completer=word_comp)

    if not roll or roll not in roll_names:
        print(f"Sorry {player_name}, {roll} is not valid!")
        return None

    return roll


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


class PlayComplete(Completer):

    def get_completions(self, document, complete_event):
        roll_names = list(rolls.keys())
        word = document.get_word_before_cursor()
        complete_all = not word if not word.strip() else word == '.'
        completions = []

        for roll in roll_names:
            is_substring = word in roll
            if complete_all or is_substring:
                completions.append(
                    Completion(roll,
                               start_position=-len(word),
                               style="fg:white bg:darkgreen",
                               selected_style="fg:yellow bg:lightgreen"
                               ))

        return completions


if __name__ == '__main__':
    main()
