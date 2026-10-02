"""
Artificial Intelligence
NRC: 1651

Raymond Portilla
Banner ID: 00335050

Exercise 06: Sudoku
"""

import os
import time


def copy_board  (board):
    new_board = []
    r = 0
    while r < 9:
        row = []
        c = 0
        while c < 9:
            row.append(board[r][c])
            c = c + 1
        new_board.append(row)
        r = r + 1
    return new_board


def read_board(path):
    board = []
    file = open(path, "r")
    for line in file:
        line = line.strip()
        if line == "":
            continue
        parts = line.replace(".", "0").split()
        row = []
        i = 0
        while i < len(parts):
            row.append(int(parts[i]))
            i = i + 1
        if len(row) != 9:
            file.close()
            print("Each row must have 9 numbers: " + path)
            return None
        board.append(row)
    file.close()
    if len(board) != 9:
        print("The board must have 9 rows: " + path)
        return None
    return board


def print_board(board):
    print("+-------+-------+-------+")
    r = 0
    while r < 9:
        line = "|"
        c = 0
        while c < 9:
            value = board[r][c]
            if value == 0:
                line = line + " ."
            else:
                line = line + " " + str(value)
            if c == 2 or c == 5 or c == 8:
                line = line + " |"
            c = c + 1
        print(line)
        if r == 2 or r == 5 or r == 8:
            print("+-------+-------+-------+")
        r = r + 1


def is_consistent(board, row, col, value):
    c = 0
    while c < 9:
        if board[row][c] == value:
            return False
        c = c + 1

    r = 0
    while r < 9:
        if board[r][col] == value:
            return False
        r = r + 1

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    r = box_row
    while r < box_row + 3:
        c = box_col
        while c < box_col + 3:
            if board[r][c] == value:
                return False
            c = c + 1
        r = r + 1

    return True


def legal_values(board, row, col):
    values = []
    value = 1
    while value <= 9:
        if is_consistent(board, row, col, value) == True:
            values.append(value)
        value = value + 1
    return values


def find_empty_naive(board):
    r = 0
    while r < 9:
        c = 0
        while c < 9:
            if board[r][c] == 0:
                return r, c
            c = c + 1
        r = r + 1
    return -1, -1


def find_empty_mrv(board):
    # Choose the empty cell with the fewest legal values
    best_row = -1
    best_col = -1
    best_count = 10

    r = 0
    while r < 9:
        c = 0
        while c < 9:
            if board[r][c] == 0:
                count = len(legal_values(board, r, c))
                if count < best_count:
                    best_count = count
                    best_row = r
                    best_col = c
            c = c + 1
        r = r + 1

    return best_row, best_col


def lcv_score(board, row, col, value):
    # How many empty neighbors would lose this value (Least Constraining Value)
    removed = 0

    c = 0
    while c < 9:
        if c != col and board[row][c] == 0:
            if is_consistent(board, row, c, value) == True:
                removed = removed + 1
        c = c + 1

    r = 0
    while r < 9:
        if r != row and board[r][col] == 0:
            if is_consistent(board, r, col, value) == True:
                removed = removed + 1
        r = r + 1

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    r = box_row
    while r < box_row + 3:
        c = box_col
        while c < box_col + 3:
            same_cell = (r == row and c == col)
            same_row = (r == row)
            same_col = (c == col)
            if same_cell == False and same_row == False and same_col == False:
                if board[r][c] == 0:
                    if is_consistent(board, r, c, value) == True:
                        removed = removed + 1
            c = c + 1
        r = r + 1

    return removed


def order_values_lcv(board, row, col, values):
    n = len(values)
    scores = []
    i = 0
    while i < n:
        scores.append(lcv_score(board, row, col, values[i]))
        i = i + 1

    # Smallest score first: the value that rules out the fewest neighbor options
    swapped = True
    while swapped == True:
        swapped = False
        i = 0
        while i < n - 1:
            if scores[i] > scores[i + 1]:
                temp_score = scores[i]
                scores[i] = scores[i + 1]
                scores[i + 1] = temp_score
                temp_value = values[i]
                values[i] = values[i + 1]
                values[i + 1] = temp_value
                swapped = True
            i = i + 1

    return values


def forward_check_ok(board, row, col):
    # After an assignment, no empty neighbor may have an empty domain
    c = 0
    while c < 9:
        if c != col and board[row][c] == 0:
            if len(legal_values(board, row, c)) == 0:
                return False
        c = c + 1

    r = 0
    while r < 9:
        if r != row and board[r][col] == 0:
            if len(legal_values(board, r, col)) == 0:
                return False
        r = r + 1

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    r = box_row
    while r < box_row + 3:
        c = box_col
        while c < box_col + 3:
            same_cell = (r == row and c == col)
            if same_cell == False and board[r][c] == 0:
                if len(legal_values(board, r, c)) == 0:
                    return False
            c = c + 1
        r = r + 1

    return True


def make_stats():
    stats = {}
    stats["assignments"] = 0
    stats["backtracks"] = 0
    stats["max_depth"] = 0
    stats["solutions"] = 0
    stats["solution"] = None
    stats["time"] = 0.0
    return stats


def backtrack(board, stats, depth, use_mrv, use_lcv, use_fc, stop_at_first):
    if depth > stats["max_depth"]:
        stats["max_depth"] = depth

    if use_mrv == True:
        row, col = find_empty_mrv(board)
    else:
        row, col = find_empty_naive(board)

    if row == -1:
        stats["solutions"] = stats["solutions"] + 1
        if stats["solution"] is None:
            stats["solution"] = copy_board(board)
        if stop_at_first == True:
            return True
        return False

    values = legal_values(board, row, col)
    if use_lcv == True:
        values = order_values_lcv(board, row, col, values)

    i = 0
    while i < len(values):
        value = values[i]
        board[row][col] = value
        stats["assignments"] = stats["assignments"] + 1

        fc_ok = True
        if use_fc == True:
            fc_ok = forward_check_ok(board, row, col)

        if fc_ok == True:
            found = backtrack(board, stats, depth + 1, use_mrv, use_lcv, use_fc, stop_at_first)
            if found == True:
                return True

        board[row][col] = 0
        stats["backtracks"] = stats["backtracks"] + 1
        i = i + 1

    return False


def run_solver(name, board, use_mrv, use_lcv, use_fc, stop_at_first):
    work = copy_board(board)
    stats = make_stats()
    stats["name"] = name
    start = time.time()
    backtrack(work, stats, 0, use_mrv, use_lcv, use_fc, stop_at_first)
    stats["time"] = time.time() - start
    return stats


def print_stats_row(stats):
    time_text = str(round(stats["time"], 4))
    print(
        stats["name"].ljust(28)
        + " assignments="
        + str(stats["assignments"]).ljust(10)
        + " backtracks="
        + str(stats["backtracks"]).ljust(10)
        + " max_depth="
        + str(stats["max_depth"]).ljust(4)
        + " time="
        + time_text
        + "s"
    )


def solve_board(title, path):
    print("-----o----- " + title + " -----o-----")
    board = read_board(path)
    if board is None:
        return

    print("\nStart board:")
    print_board(board)
    print("")

    versions = []
    versions.append(run_solver("Naive backtracking", board, False, False, False, True))
    versions.append(run_solver("MRV", board, True, False, False, True))
    versions.append(run_solver("LCV", board, False, True, False, True))
    versions.append(run_solver("Forward checking", board, False, False, True, True))

    print("First solution (from naive backtracking):")
    if versions[0]["solution"] is None:
        print("No solution found.")
    else:
        print_board(versions[0]["solution"])
    print("")

    print("Comparison table (stop at the first solution):")
    i = 0
    while i < len(versions):
        print_stats_row(versions[i])
        i = i + 1
    print("")

    print("Counting every solution with MRV...")
    count_stats = run_solver("Count all solutions", board, True, False, False, False)
    print("Number of solutions: " + str(count_stats["solutions"]))
    if count_stats["solutions"] == 1:
        print("This board has exactly one solution, as a well-posed Sudoku should.")
    print("\n")


if __name__ == "__main__":
    print("\n.: Sudoku :. \n")
    script_folder = os.path.dirname(__file__)
    if script_folder == "":
        script_folder = "."

    board1 = script_folder + "/sudoku_board1.txt"
    board2 = script_folder + "/sudoku_board2.txt"

    solve_board("Board 1 (30 givens)", board1)
    solve_board("Board 2 (22 givens)", board2)