"""
Artificial Intelligence
NRC: 1651

Raymond Portilla
Banner ID: 00335050

Exercise 01: 8-Tile
"""

from collections import deque
import heapq
import math


START_STATE = (7, 2, 4, 5, 0, 6, 8, 3, 1)

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Blank moves: name, index change, row change, column change
MOVES = [
    ("Up", -3, -1, 0),
    ("Down", 3, 1, 0),
    ("Left", -1, 0, -1),
    ("Right", 1, 0, 1),
]


def print_board(state):
    print("+---+---+---+")
    for row in range(3):
        line = "|"
        for col in range(3):
            tile = state[row * 3 + col]
            if tile == 0:
                line += "   |"
            else:
                line += " " + str(tile) + " |"
        print(line)
        print("+---+---+---+")


def find_blank(state):
    for i in range(9):
        if state[i] == 0:
            return i
    return -1


def get_next_states(state):
    blank = find_blank(state)
    row = blank // 3
    col = blank % 3
    results = []

    for name, index_change, row_change, col_change in MOVES:
        new_row = row + row_change
        new_col = col + col_change
        if new_row < 0 or new_row > 2 or new_col < 0 or new_col > 2:
            continue

        new_blank = blank + index_change
        new_state = list(state)
        new_state[blank] = new_state[new_blank]
        new_state[new_blank] = 0
        results.append((tuple(new_state), name))

    return results


def inversion_count(state):
    # Parity test: ignore the blank, count pairs that are out of order
    count = 0
    tiles = []
    for tile in state:
        if tile != 0:
            tiles.append(tile)

    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                count += 1
    return count


def is_solvable(start_state, goal_state):
    return inversion_count(start_state) % 2 == inversion_count(goal_state) % 2


def reconstruct_path(parent, goal_state):
    path = []
    state = goal_state
    while state is not None:
        prev_state, action = parent[state]
        path.append((state, action))
        state = prev_state
    path.reverse()
    return path


# My choice of free heuristic: how many tiles are not in their goal square (blank does not count)
def misplaced_tiles(state, goal_state):
    count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal_state[i]:
            count += 1
    return count


def manhattan_distance(state, goal_state):
    # For each tile, abs(row difference) + abs(column difference)
    total = 0
    for i in range(9):
        tile = state[i]
        if tile == 0:
            continue
        goal_index = goal_state.index(tile)
        row = i // 3
        col = i % 3
        goal_row = goal_index // 3
        goal_col = goal_index % 3
        total += abs(row - goal_row) + abs(col - goal_col)
    return total


def euclidean_distance(state, goal_state):
    # Straight-line distance of each tile to its goal square
    total = 0.0
    for i in range(9):
        tile = state[i]
        if tile == 0:
            continue
        goal_index = goal_state.index(tile)
        row = i // 3
        col = i % 3
        goal_row = goal_index // 3
        goal_col = goal_index % 3
        total += math.sqrt((row - goal_row) ** 2 + (col - goal_col) ** 2)
    return total


def bfs(start_state, goal_state):
    queue = deque([start_state])
    visited = set([start_state])
    parent = {start_state: (None, None)}
    generated = 0
    expanded = 0

    while queue:
        current_state = queue.popleft()
        expanded += 1
        if current_state == goal_state:
            path = reconstruct_path(parent, current_state)
            return path, generated, expanded

        for next_state, action in get_next_states(current_state):
            generated += 1
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (current_state, action)
                queue.append(next_state)

    return None, generated, expanded


def dfs(start_state, goal_state):
    stack = [start_state]
    visited = set([start_state])
    parent = {start_state: (None, None)}
    generated = 0
    expanded = 0

    while stack:
        current_state = stack.pop()
        expanded += 1
        if current_state == goal_state:
            path = reconstruct_path(parent, current_state)
            return path, generated, expanded

        for next_state, action in get_next_states(current_state):
            generated += 1
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (current_state, action)
                stack.append(next_state)

    return None, generated, expanded


def best_first_search(start_state, goal_state, heuristic):
    # Greedy best-first search: expand the node with the smallest h(n).
    # This is best-first search with f(n) = h(n). A* would use g(n) + h(n).
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state, goal_state), start_state))
    visited = set([start_state])
    parent = {start_state: (None, None)}
    generated = 0
    expanded = 0

    while frontier:
        h_value, current_state = heapq.heappop(frontier)
        expanded += 1
        if current_state == goal_state:
            path = reconstruct_path(parent, current_state)
            return path, generated, expanded

        for next_state, action in get_next_states(current_state):
            generated += 1
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (current_state, action)
                next_h = heuristic(next_state, goal_state)
                heapq.heappush(frontier, (next_h, next_state))

    return None, generated, expanded


def print_path(path, max_boards=30):
    if path is None:
        print("No solution found.")
        return

    steps = len(path) - 1
    print("Start board:")
    print_board(path[0][0])

    if steps > max_boards:
        print("\nPath is long (" + str(steps) + " moves). Showing only the last board.")
        print("\nGoal board:")
        print_board(path[-1][0])
        print("\nSuccessfully completed in " + str(steps) + " steps.")
        return

    for state, action in path[1:]:
        print("\nAction: blank " + action)
        print_board(state)

    print("\nSuccessfully completed in " + str(steps) + " steps.")


def print_stats(name, path, generated, expanded):
    if path is None:
        length = "-"
    else:
        length = str(len(path) - 1)
    print(
        name.ljust(28)
        + " path="
        + length.ljust(6)
        + " generated="
        + str(generated).ljust(10)
        + " expanded="
        + str(expanded)
    )


if __name__ == "__main__":
    start_state = START_STATE
    goal_state = GOAL_STATE

    print("\n.: 8-tile puzzle :. \n")
    print("Start:")
    print_board(start_state)
    print("")
    print("Goal:")
    print_board(goal_state)
    print("")

    if not is_solvable(start_state, goal_state):
        print("This start cannot reach the goal (different inversion parity).")
    else:
        print("The start is solvable (same inversion parity as the goal).\n")

        print("\n----o---- Breadth-first search ----o----\n")
        bfs_path, bfs_gen, bfs_exp = bfs(start_state, goal_state)
        print_path(bfs_path)

        print("\n\n----o---- Depth-first search ----o----\n")
        dfs_path, dfs_gen, dfs_exp = dfs(start_state, goal_state)
        print_path(dfs_path)

        print("\n\n----o---- Best-first search (Euclidean distance) ----o----\n")
        euc_path, euc_gen, euc_exp = best_first_search(start_state, goal_state, euclidean_distance)
        print_path(euc_path)

        print("\n\n----o---- Best-first search (Manhattan distance) ----o----\n")
        man_path, man_gen, man_exp = best_first_search(start_state, goal_state, manhattan_distance)
        print_path(man_path)

        print("\n\n----o---- Best-first search (misplaced tiles) ----o----\n")
        mis_path, mis_gen, mis_exp = best_first_search(start_state, goal_state, misplaced_tiles)
        print_path(mis_path)

        print("\n\n----o---- Comparison ----o----\n")
        print_stats("BFS", bfs_path, bfs_gen, bfs_exp)
        print_stats("DFS", dfs_path, dfs_gen, dfs_exp)
        print_stats("Best-first Euclidean", euc_path, euc_gen, euc_exp)
        print_stats("Best-first Manhattan", man_path, man_gen, man_exp)
        print_stats("Best-first misplaced", mis_path, mis_gen, mis_exp)