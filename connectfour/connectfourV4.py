import datetime
import json
import os
from colorama import Fore


def main():
    log("Game started")
    print()
    print("Welcome to Connect 4 V4!")
    print("Color and error handling edition")
    print("-----------------")
    print()

    # create empty board
    board = [
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
    ]

    show_leader_board()

    # get players
    active_player_index = 0
    try:
        players = [input("Player 1, what is your name? "), input("Player 2, what is your name? ")]
        symbols = ["@", "■"]
        log(f"Players are {players[0]} as {symbols[0]} and {players[1]} as {symbols[1]}")
        # repeat until breakpoint (winner)
        while True:
            # set the player and symbol based on index of 0 or 1
            player = players[active_player_index]
            symbol = symbols[active_player_index]
            announce_turn(player, symbol, active_player_index)
            show_board(board, symbols)
            log(f"{player}'s turn")
            # allow player to set piece, save location of piece
            this_turn = choose_location(board, symbol, active_player_index)
            # check if placement failed and retry turn
            if not this_turn:
                print("You can't place that piece, try again.")
                log(f"Bad placement by {player}")
                continue
            log(f"{player} placed {symbol} in column {this_turn[1] + 1}")
            # see if this turn has made a winner and end the game
            if find_winner(board, symbol):
                if active_player_index == 0:
                    fg = Fore.LIGHTGREEN_EX
                else:
                    fg = Fore.BLUE
                print()
                print(f"Congratulations, " + fg + player + Fore.WHITE + " has won the game! ")
                log(f"Player {player} has won the game")
                show_board(board, symbols)
                record_win(player)
                break
            # check for a stalemate condition
            if check_stalemate(board):
                print()
                print("Game over, " + Fore.RED + "Stalemate" + Fore.WHITE + " detected!")
                show_board(board, symbols)
                record_win("Stalemate")
                log(f"Stalemate between {players[0]} and {players[1]}")
                break
            # set for next player
            active_player_index = (active_player_index + 1) % len(players)
    except KeyboardInterrupt:
        print()
        print(Fore.CYAN + "Okay, I guess you don't want to play right now.")
        print("Not like I have " + Fore.RED + "FEELINGS" + Fore.CYAN + " to consider or anything" + Fore.WHITE)


def show_leader_board():
    leaders = load_leaders()

    sorted_names = list(leaders.items())
    sorted_names.sort(key=lambda l: l[1], reverse=True)

    print()
    print("Leaders: ")
    for name, wins in sorted_names[0:5]:
        print(Fore.LIGHTGREEN_EX + f"{wins:,} " + Fore.WHITE + "-- " + Fore.BLUE + name + Fore.WHITE)
    print()
    print("-----------------")
    print()


def announce_turn(player, symbol, active_index):
    if active_index == 0:
        fg = Fore.LIGHTGREEN_EX
    else:
        fg = Fore.BLUE
    print("It is " + fg + player + Fore.WHITE + "'s turn, place your " + fg + symbol + Fore.WHITE)
    print()


def show_board(board, symbols):
    # board column numbers and header spacer
    print("_ 1 _ 2 _ 3 _ 4 _ 5 _ 6 _ 7 _")
    print("- - - - - - - - - - - - - - -")
    for row in board:
        print("| ", end="")
        for cell in row:
            symbol = cell if cell is not None else "_"
            if symbol == symbols[0]:
                fg = Fore.LIGHTGREEN_EX
            elif symbol == symbols[1]:
                fg = Fore.BLUE
            else:
                fg = Fore.WHITE
            print(fg + symbol + Fore.WHITE, end=" | ")
        print()
    # footer
    print("- - - - - - - - - - - - - - -")


def choose_location(board, symbol, active_index):
    if active_index == 0:
        fg = Fore.LIGHTGREEN_EX
    else:
        fg = Fore.BLUE
    try:
        # get the column number to drop piece
        column = int(input(f"Choose a column to drop your " + fg + symbol + Fore.WHITE + " piece(1-7): "))
    except ValueError:
        return False
    # offset for array index 0
    column -= 1
    # check for out of bound entry
    if column < 0 or column >= len(board[0]):
        return False

    # check if whole column is full
    top_cell = board[0][column]
    if top_cell is not None:
        return False

    # get the lowest empty row in this column
    bottom = find_bottom(board, column)
    # change that cell to this player symbol
    board[bottom][column] = symbol

    # give the position of the new piece
    return [bottom, column]


def find_bottom(board, column):
    # in the column given, go through each row from the top down
    for row_idx in range(0, 6):
        # if the cell has a piece, return the row above
        if board[row_idx][column] is not None:
            return row_idx - 1
    # if none of the cells have a piece, return bottom
    return 5


def find_winner(board, symbol):
    # get lists of cells to test
    test_cells = get_test_cells(board)
    # test each list if they all match this player's symbol
    for this_list in test_cells:
        for idx_start in range(0, len(this_list) - 3):
            cells = this_list[idx_start:idx_start + 4]
            if all(symbol == cell for cell in cells):
                return True
    return False


def get_test_cells(board):
    all_testable_cells = []

    # rows are just the board as-is
    all_testable_cells.extend(board)

    # columns are every row for each column in turn
    for col in range(0, len(board[0])):
        this_col = []
        for row in range(0, len(board)):
            this_col.append(board[row][col])
        all_testable_cells.append(this_col)

    # diagonals are manually grabbing all possibles as lists, not all cells can be possible
    # UL/DR first, then UR/DL
    diagonals = [
        [board[3][0], board[2][1], board[1][2], board[0][3]],
        [board[4][0], board[3][1], board[2][2], board[1][3], board[0][4]],
        [board[5][0], board[4][1], board[3][2], board[2][3], board[1][4], board[0][5]],
        [board[5][1], board[4][2], board[3][3], board[2][4], board[1][5], board[0][6]],
        [board[5][2], board[4][3], board[3][4], board[2][5], board[1][6]],
        [board[5][3], board[4][4], board[3][5], board[2][6]],
        [board[3][6], board[2][5], board[1][4], board[0][3]],
        [board[4][6], board[3][5], board[2][4], board[1][3], board[0][2]],
        [board[5][6], board[4][5], board[3][4], board[2][3], board[1][2], board[0][1]],
        [board[5][5], board[4][4], board[3][3], board[2][2], board[1][1], board[0][0]],
        [board[5][4], board[4][3], board[3][2], board[2][1], board[1][0]],
        [board[5][3], board[4][2], board[3][1], board[2][0]],
    ]
    all_testable_cells.extend(diagonals)

    return all_testable_cells


def check_stalemate(board):
    if None in board[0]:
        return False
    return True


def load_leaders():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'c4leaderboard.json')

    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r', encoding='utf-8') as fin:
            return json.load(fin)
    except json.decoder.JSONDecodeError:
        print(Fore.RED + "Could not load leader-board file!" + Fore.WHITE)
        return {}


def record_win(winner_name):
    leaders = load_leaders()

    if winner_name in leaders:
        leaders[winner_name] += 1
    else:
        leaders[winner_name] = 1

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'c4leaderboard.json')

    try:
        with open(filename, 'w', encoding='utf-8') as fout:
            json.dump(leaders, fout)
    except Exception as ex:
        print("Could not write to leader-board file!")
        print(ex)


def log(msg):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'c4.log')

    try:
        with open(filename, 'a', encoding='utf-8') as fout:
            fout.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ")
            fout.write(msg)
            fout.write('\n')
    except Exception as ex:
        print("Could not write to log file!")
        print(ex)


if __name__ == "__main__":
    main()
