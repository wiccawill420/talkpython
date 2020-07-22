import datetime
import json
import os
from colorama import Fore


def main():
    log("Game started")
    print()
    print("Welcome to Connect 4 V3!")
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
        if find_winner(board, symbol, this_turn):
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


def find_winner(board, symbol, this_turn):
    # get list of lists to test around last placed piece
    test_cells = get_adjacent_cells(board, this_turn[0], this_turn[1])
    # test each list if they all match this player's symbol
    for cells in test_cells:
        if all(symbol == cell for cell in cells):
            return True
    return False


def check_stalemate(board):
    if None in board[0]:
        return False
    return True


def get_adjacent_cells(board, row, column):
    test_cells = []

    # row right (+)
    # diagonal UR (- +)
    # diagonal DR (+ +)
    this_row = []
    up_diagonal = []
    down_diagonal = []
    ud_offset = 0
    # from the piece placed, grab it and the 3 pieces to the right
    for col_idx in range(column, column + 4):
        # if it falls off the board, return None
        if col_idx > len(board[0]) - 1:
            this_row.append(None)
            up_diagonal.append(None)
            down_diagonal.append(None)
        else:
            this_row.append(board[row][col_idx])
            # move up with column to get diagonal
            # if it falls off the top of the board, None
            if row - ud_offset < 0:
                up_diagonal.append(None)
            else:
                ud_idx = row - ud_offset
                up_diagonal.append(board[ud_idx][col_idx])
            # moved down with column to get diagonal
            # if it falls off the bottom of the board, None
            if row + ud_offset > len(board) - 1:
                down_diagonal.append(None)
            else:
                dd_idx = row + ud_offset
                down_diagonal.append(board[dd_idx][col_idx])
        ud_offset += 1
    # output results to list of lists
    test_cells.append(this_row)
    test_cells.append(up_diagonal)
    test_cells.append(down_diagonal)

    # row left (-)
    # diagonal UL (- -)
    # diagonal DL (+ -)
    this_row = []
    up_diagonal = []
    down_diagonal = []
    # due to moving left, start at left-most offset-most position
    ud_offset = 3
    # from the piece placed, grab it and the 3 pieces to the right
    for col_idx in range(column - 3, column + 1):
        # if it falls off the board, return None
        if col_idx < 0:
            this_row.append(None)
            up_diagonal.append(None)
            down_diagonal.append(None)
        else:
            this_row.append(board[row][col_idx])
            # move up with column to get diagonal
            # if it falls off the top of the board, None
            if row - ud_offset < 0:
                up_diagonal.append(None)
            else:
                ud_idx = row - ud_offset
                up_diagonal.append(board[ud_idx][col_idx])
            # moved down with column to get diagonal
            # if it falls off the bottom of the board, None
            if row + ud_offset > len(board) - 1:
                down_diagonal.append(None)
            else:
                dd_idx = row + ud_offset
                down_diagonal.append(board[dd_idx][col_idx])
        ud_offset -= 1
    # output results to list of lists
    test_cells.append(this_row)
    test_cells.append(up_diagonal)
    test_cells.append(down_diagonal)

    # column down (+)
    this_col = []
    for row_idx in range(row, row + 4):
        if row_idx > len(board) - 1:
            this_col.append(None)
        else:
            this_col.append(board[row_idx][column])
    test_cells.append(this_col)

    # column up (-)
    this_col = []
    for row_idx in range(row - 3, row + 1):
        if row_idx < 0:
            this_col.append(None)
        else:
            this_col.append(board[row_idx][column])
    test_cells.append(this_col)
    return test_cells


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
