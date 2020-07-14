# x create board
# x get players
# x while no winner
#   x show board
#   x alternate players
#   x drop chips from top to arrive at lowest place in column
# active player won


def main():
    print()
    print("Welcome to Connect 4!")
    print()

    # create board
    board = [
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
    ]

    # get players
    active_player_index = 0
    players = ["Bridget", "Computer"]
    symbols = ["X", "O"]

    # until someone wins
    while not find_winner(board):
        player = players[active_player_index]
        symbol = symbols[active_player_index]
        announce_turn(player)
        show_board(board)
        if not choose_location(board, symbol):
            print("You can't place a piece there, try again.")
            continue
        active_player_index = (active_player_index + 1) % len(players)


def announce_turn(player):
    print(f"It is {player}'s turn")
    print()


def show_board(board):
    print("_ 1 _ 2 _ 3 _ 4 _ 5 _ 6 _ 7 _")
    print("- - - - - - - - - - - - - - -")
    for row in board:
        print("| ", end="")
        for cell in row:
            symbol = cell if cell is not None else "_"
            print(symbol, end=" | ")
        print()
    print("- - - - - - - - - - - - - - -")


def choose_location(board, symbol):
    column = int(input("Choose a column to drop your piece(1-7): "))
    column -= 1
    if column < 0 or column >= len(board[0]):
        return False

    top_cell = board[0][column]
    if top_cell is not None:
        return False

    bottom = find_bottom(board, column)
    board[bottom][column] = symbol

    return True


def find_bottom(board, column):
    for row_idx in range(0, 6):
        if board[row_idx][column] is not None:
            return row_idx - 1
    return 5


def find_winner(board):
    for row in range(0, 5):
        for column in range(0, 6):
            if board[row][column] is None:
                continue
            else:
                this_symbol = board[row][column]

    # by row

    # by column

    # by diagonal

    return False


if __name__ == "__main__":
    main()
