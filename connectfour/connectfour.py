
def main():
    print()
    print("Welcome to Connect 4!")
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

    # get players
    active_player_index = 0
    players = ["Player 1", "Player 2"]
    symbols = ["X", "O"]

    # repeat until breakpoint (winner)
    while True:
        # set the player and symbol based on index of 0 or 1
        player = players[active_player_index]
        symbol = symbols[active_player_index]
        announce_turn(player, symbol)
        show_board(board)
        # allow player to set piece, save location of piece
        this_turn = choose_location(board, symbol)
        # check if placement failed and retry turn
        if not this_turn:
            print("You can't place that piece, try again.")
            continue
        # see if this turn has made a winner and end the game
        if find_winner(board, symbol, this_turn):
            print()
            print(f"Congratulations, {player} has won the game! ")
            show_board(board)
            break
        # set for next player
        active_player_index = (active_player_index + 1) % len(players)


def announce_turn(player, symbol):
    print(f"It is {player}'s turn, place your {symbol}")
    print()


def show_board(board):
    # board column numbers and header spacer
    print("_ 1 _ 2 _ 3 _ 4 _ 5 _ 6 _ 7 _")
    print("- - - - - - - - - - - - - - -")
    for row in board:
        print("| ", end="")
        for cell in row:
            symbol = cell if cell is not None else "_"
            print(symbol, end=" | ")
        print()
    # footer
    print("- - - - - - - - - - - - - - -")


def choose_location(board, symbol):
    try:
        # get the column number to drop piece
        column = int(input(f"Choose a column to drop your {symbol} piece(1-7): "))
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


if __name__ == "__main__":
    main()
