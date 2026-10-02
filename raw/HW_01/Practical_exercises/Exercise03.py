"""
Artificial Intelligence
NRC: 1651

Raymond Portilla
Banner ID: 00335050

Exercise 03: 8-Queens
"""


def create_board(N_QUEENS):
    board = []
    for i in range(N_QUEENS):
        row = []
        for j in range(N_QUEENS):
            row.append(0)
        board.append(row)
    return board


def print_board(board):
    size = len(board)
    border = "+"
    i = 0
    while i < size:
        border = border + "---+"
        i = i + 1

    print(border)
    r = 0
    while r < size:
        line = "|"
        c = 0
        while c < size:
            if board[r][c] == 1:
                line = line + " Q |"
            else:
                line = line + "   |"
            c = c + 1
        print(line)
        print(border)
        r = r + 1


def place_queen(board, row, col):
    board[row][col] = 1


def remove_queen(board, row, col):
    board[row][col] = 0


def is_safe(board, row, col):
    # same row, to the left
    for c in range(col):
        if board[row][c] == 1:
            return False

    # upper-left diagonal
    r = row - 1
    c = col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            return False
        r = r - 1
        c = c - 1

    # lower-left diagonal
    r = row + 1
    c = col - 1
    while r < len(board) and c >= 0:
        if board[r][c] == 1:
            return False
        r = r + 1
        c = c - 1

    return True


def backtrack(board, col):
    if col == len(board):
        return True

    for row in range(len(board)):
        if is_safe(board, row, col):
            place_queen(board, row, col)
            result = backtrack(board, col + 1)

            if result == True:
                return True
            remove_queen(board, row, col)

    return False


if __name__ == "__main__":
    print("\n.: N-Queens :. \n")
    N_QUEENS = int(input("Enter the number of queens: "))
    board = create_board(N_QUEENS)

    if backtrack(board, 0) == True:
        print("")
        print("Solution found for " + str(N_QUEENS) + " queens:")
        print_board(board)
    else:
        print("")
        print("No solution found for " + str(N_QUEENS) + " queens.")