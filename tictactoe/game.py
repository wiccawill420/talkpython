from colorama import Fore


def main():
    print(Fore.WHITE + "Welcome to Tic Tac Toe!")
    # board is a list of rows
    # rows are a list of cells
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    active_player_index = 0
    players = ["Bridget", "Computer"]
    symbols = ["X", "O"]
    player = players[active_player_index]

    # until someone wins
    while not find_winner(board):
        # show the board
        player = players[active_player_index]
        symbol = symbols[active_player_index]

        announce_turn(player, active_player_index)
        show_board(board)
        if not choose_location(board, symbol):
            print(Fore.RED + "that isn't an option, try again.")
            print(Fore.WHITE)
            continue

        # toggle active player
        active_player_index = (active_player_index + 1) % len(players)

    print()
    fore = Fore.GREEN if active_player_index == 1 else Fore.YELLOW
    print("GAME OVER! " + fore + player + Fore.WHITE + " has won with the board: ")
    show_board(board)
    print()


def choose_location(board, symbol):
    row = int(input("Choose which row: "))
    column = int(input("Choose which column: "))

    row -= 1
    column -= 1
    if row < 0 or row >= len(board):
        return False
    if column < 0 or row >= len(board[0]):
        return False

    cell = board[row][column]
    if cell is not None:
        return False

    board[row][column] = symbol
    return True


def show_board(board):
    for row in board:
        print(Fore.WHITE + "| ", end='')
        for cell in row:
            symbol = cell if cell is not None else "_"
            if cell == 'X':
                fore = Fore.GREEN
            elif cell == 'O':
                fore = Fore.YELLOW
            else:
                fore = Fore.WHITE
            print(fore + symbol, end='')
            print(Fore.WHITE + " | ", end='')
        print()


def announce_turn(player, index):
    print()
    fore = Fore.GREEN if index == 0 else Fore.YELLOW
    print(fore + f"It's {player}'s turn" + Fore.WHITE)
    print()


def find_winner(board):
    sequences = get_winning_sequences(board)
    for cells in sequences:
        symbol1 = cells[0]
        if symbol1 and all(symbol1 == cell for cell in cells):
            return True

    return False


def get_winning_sequences(board):
    sequences = []

    # Win by row
    rows = board
    sequences.extend(rows)

    # Win by columns
    for col_idx in range(0, 3):
        col = [
            board[0][col_idx],
            board[1][col_idx],
            board[2][col_idx],
        ]
        sequences.append(col)

    # Win by diagonals
    diagonals = [
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    sequences.extend(diagonals)

    return sequences


if __name__ == '__main__':
    main()
