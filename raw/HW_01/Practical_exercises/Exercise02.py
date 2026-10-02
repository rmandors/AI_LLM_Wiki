"""
Artificial Intelligence
NRC: 1651

Raymond Portilla
Banner ID: 00335050

Exercise 02: 80-Tile
"""

import heapq
import os
import time


SIZE = 9
N_CELLS = 81

QUADRANT_LETTERS = "ABCDEFGHI"

START_QUADRANTS = [0, 1, 2, 3, 4, 5, 6, 7, 8]
GOAL_QUADRANTS = [0, 1, 2, 7, 8, 3, 6, 5, 4]

START_INSIDE = [1, 2, 3, 4, 5, 6, 7, 8, 9]
GOAL_INSIDE = [1, 2, 3, 8, 9, 4, 7, 6, 5]

# Missing tile 9I (the hole starts at the bottom right)
BLANK_TILE = 8 * 9 + 9

MOVES = [
    ("Up", -SIZE, -1, 0),
    ("Down", SIZE, 1, 0),
    ("Left", -1, 0, -1),
    ("Right", 1, 0, 1),
]


def make_tile(quadrant, number):
    return quadrant * 9 + number


def tile_name(tile):
    if tile == 0:
        return "  "
    number = (tile - 1) % 9 + 1
    letter = QUADRANT_LETTERS[(tile - 1) // 9]
    return str(number) + letter


def build_board(quadrants, inside):
    cells = []
    i = 0
    while i < N_CELLS:
        cells.append(0)
        i = i + 1

    qi = 0
    while qi < 9:
        qr = qi // 3
        qc = qi % 3
        q = quadrants[qi]
        li = 0
        while li < 9:
            lr = li // 3
            lc = li % 3
            number = inside[li]
            tile = make_tile(q, number)
            row = qr * 3 + lr
            col = qc * 3 + lc
            cells[row * SIZE + col] = tile
            li = li + 1
        qi = qi + 1

    i = 0
    while i < N_CELLS:
        if cells[i] == BLANK_TILE:
            cells[i] = 0
        i = i + 1

    return tuple(cells)


def board_lines(state):
    lines = []
    r = 0
    while r < SIZE:
        line = ""
        c = 0
        while c < SIZE:
            name = tile_name(state[r * SIZE + c])
            line = line + name
            if c == 2 or c == 5:
                line = line + " | "
            else:
                if c < SIZE - 1:
                    line = line + " "
            c = c + 1
        lines.append(line)
        if r == 2 or r == 5:
            lines.append("---------+----------+---------")
        r = r + 1
    return lines


def print_board(state):
    lines = board_lines(state)
    i = 0
    while i < len(lines):
        print(lines[i])
        i = i + 1


def find_blank(state):
    i = 0
    while i < N_CELLS:
        if state[i] == 0:
            return i
        i = i + 1
    return -1


def get_next_states(state):
    blank = find_blank(state)
    row = blank // SIZE
    col = blank % SIZE
    results = []

    m = 0
    while m < len(MOVES):
        name = MOVES[m][0]
        index_change = MOVES[m][1]
        row_change = MOVES[m][2]
        col_change = MOVES[m][3]
        new_row = row + row_change
        new_col = col + col_change
        m = m + 1
        if new_row < 0 or new_row > SIZE - 1 or new_col < 0 or new_col > SIZE - 1:
            continue
        new_blank = blank + index_change
        new_state = list(state)
        new_state[blank] = new_state[new_blank]
        new_state[new_blank] = 0
        results.append((tuple(new_state), name))

    return results


def inversion_parity(state, goal_state):
    # Map each tile to the index it should have in the goal
    goal_index = []
    i = 0
    while i < N_CELLS:
        goal_index.append(-1)
        i = i + 1

    i = 0
    while i < N_CELLS:
        goal_index[goal_state[i]] = i
        i = i + 1

    perm = []
    i = 0
    while i < N_CELLS:
        perm.append(goal_index[state[i]])
        i = i + 1

    seen = []
    i = 0
    while i < N_CELLS:
        seen.append(False)
        i = i + 1

    swaps = 0
    i = 0
    while i < N_CELLS:
        if seen[i] == False:
            j = i
            length = 0
            while seen[j] == False:
                seen[j] = True
                j = perm[j]
                length = length + 1
            swaps = swaps + (length - 1)
        i = i + 1

    return swaps % 2


def blank_taxicab(start_state, goal_state):
    start_blank = find_blank(start_state)
    goal_blank = find_blank(goal_state)
    sr = start_blank // SIZE
    sc = start_blank % SIZE
    gr = goal_blank // SIZE
    gc = goal_blank % SIZE
    return abs(sr - gr) + abs(sc - gc)


def is_solvable(start_state, goal_state):
    return inversion_parity(start_state, goal_state) == (blank_taxicab(start_state, goal_state) % 2)


def reconstruct_path(parent, goal_state):
    path = []
    state = goal_state
    while state is not None:
        info = parent[state]
        prev_state = info[0]
        action = info[1]
        path.append((state, action))
        state = prev_state
    path.reverse()
    return path


def build_goal_tables(goal_state):
    # cost[tile][index] = Manhattan distance of that tile if it sits at index
    cost = []
    t = 0
    while t < BLANK_TILE + 1:
        row = []
        i = 0
        while i < N_CELLS:
            row.append(0)
            i = i + 1
        cost.append(row)
        t = t + 1

    i = 0
    while i < N_CELLS:
        tile = goal_state[i]
        if tile != 0:
            goal_row = i // SIZE
            goal_col = i % SIZE
            p = 0
            while p < N_CELLS:
                row = p // SIZE
                col = p % SIZE
                cost[tile][p] = abs(row - goal_row) + abs(col - goal_col)
                p = p + 1
        i = i + 1
    return cost


def manhattan_distance(state, cost):
    total = 0
    i = 0
    while i < N_CELLS:
        tile = state[i]
        if tile != 0:
            total = total + cost[tile][i]
        i = i + 1
    return total


def neighbors_of_blank():
    table = []
    i = 0
    while i < N_CELLS:
        table.append([])
        i = i + 1

    i = 0
    while i < N_CELLS:
        row = i // SIZE
        col = i % SIZE
        m = 0
        while m < len(MOVES):
            name = MOVES[m][0]
            index_change = MOVES[m][1]
            row_change = MOVES[m][2]
            col_change = MOVES[m][3]
            new_row = row + row_change
            new_col = col + col_change
            m = m + 1
            if new_row < 0 or new_row > SIZE - 1 or new_col < 0 or new_col > SIZE - 1:
                continue
            table[i].append((name, i + index_change))
        i = i + 1
    return table


def apply_move(state, blank, new_blank):
    new_state = list(state)
    new_state[blank] = new_state[new_blank]
    new_state[new_blank] = 0
    return tuple(new_state)


def weighted_a_star(start_state, cost, neigh, weight, max_expansions, time_limit):
    start_h = manhattan_distance(start_state, cost)
    start_blank = find_blank(start_state)
    frontier = []
    counter = 0
    heapq.heappush(frontier, (weight * start_h, 0, start_h, counter, start_state, start_blank))
    visited = {}
    visited[start_state] = 0
    parent = {}
    parent[start_state] = (None, None)
    generated = 0
    expanded = 0
    best_h = start_h
    t0 = time.time()

    while len(frontier) > 0:
        node = heapq.heappop(frontier)
        g_value = node[1]
        h_value = node[2]
        current = node[4]
        blank = node[5]
        expanded = expanded + 1

        if h_value < best_h:
            best_h = h_value

        if h_value == 0:
            elapsed = time.time() - t0
            path = reconstruct_path(parent, current)
            return path, generated, expanded, elapsed, best_h, True

        if expanded >= max_expansions or (time.time() - t0) > time_limit:
            elapsed = time.time() - t0
            return None, generated, expanded, elapsed, best_h, False

        k = 0
        while k < len(neigh[blank]):
            action = neigh[blank][k][0]
            new_blank = neigh[blank][k][1]
            k = k + 1
            tile = current[new_blank]
            next_state = apply_move(current, blank, new_blank)
            generated = generated + 1
            next_g = g_value + 1
            already = next_state in visited
            if already == False or visited[next_state] > next_g:
                visited[next_state] = next_g
                parent[next_state] = (current, action)
                next_h = h_value - cost[tile][new_blank] + cost[tile][blank]
                counter = counter + 1
                next_f = next_g + weight * next_h
                heapq.heappush(frontier, (next_f, next_g, next_h, counter, next_state, new_blank))

    elapsed = time.time() - t0
    return None, generated, expanded, elapsed, best_h, True


def a_star(start_state, cost, neigh, max_expansions, time_limit):
    return weighted_a_star(start_state, cost, neigh, 1, max_expansions, time_limit)


def beam_search(start_state, cost, neigh, width, max_depth, time_limit):
    start_h = manhattan_distance(start_state, cost)
    start_blank = find_blank(start_state)
    level = []
    level.append((start_h, start_state, start_blank))
    visited = set()
    visited.add(start_state)
    parent = {}
    parent[start_state] = (None, None)
    generated = 0
    expanded = 0
    best_h = start_h
    depth = 0
    t0 = time.time()
    counter = 0

    while len(level) > 0:
        if depth >= max_depth or (time.time() - t0) > time_limit:
            elapsed = time.time() - t0
            return None, generated, expanded, elapsed, best_h, False

        children = []
        i = 0
        while i < len(level):
            h_value = level[i][0]
            current = level[i][1]
            blank = level[i][2]
            i = i + 1
            expanded = expanded + 1

            k = 0
            while k < len(neigh[blank]):
                action = neigh[blank][k][0]
                new_blank = neigh[blank][k][1]
                k = k + 1
                tile = current[new_blank]
                next_state = apply_move(current, blank, new_blank)
                generated = generated + 1
                if next_state in visited:
                    continue
                visited.add(next_state)
                parent[next_state] = (current, action)
                next_h = h_value - cost[tile][new_blank] + cost[tile][blank]
                if next_h < best_h:
                    best_h = next_h
                if next_h == 0:
                    elapsed = time.time() - t0
                    path = reconstruct_path(parent, next_state)
                    return path, generated, expanded, elapsed, best_h, True
                counter = counter + 1
                children.append((next_h, counter, next_state, new_blank))

        if len(children) == 0:
            elapsed = time.time() - t0
            return None, generated, expanded, elapsed, best_h, True

        children.sort()
        level = []
        j = 0
        while j < len(children) and j < width:
            level.append((children[j][0], children[j][2], children[j][3]))
            j = j + 1
        depth = depth + 1

    elapsed = time.time() - t0
    return None, generated, expanded, elapsed, best_h, True


def board_dot_label(action, state, cost):
    h_value = manhattan_distance(state, cost)
    html = "<"
    html = html + "<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" CELLPADDING=\"3\">"
    html = html + "<TR><TD COLSPAN=\"9\" BORDER=\"0\" ALIGN=\"CENTER\"><B>"
    html = html + action + "</B>  h=" + str(h_value) + "</TD></TR>"
    r = 0
    while r < SIZE:
        html = html + "<TR>"
        c = 0
        while c < SIZE:
            name = tile_name(state[r * SIZE + c]).strip()
            qr = r // 3
            qc = c // 3
            if name == "":
                name = " "
                bg = "#FFE066"
            else:
                if (qr + qc) % 2 == 0:
                    bg = "white"
                else:
                    bg = "#E8E8E8"
            html = html + "<TD BGCOLOR=\"" + bg + "\" ALIGN=\"CENTER\">" + name + "</TD>"
            c = c + 1
        html = html + "</TR>"
        r = r + 1
    html = html + "</TABLE>>"
    return html


def write_dot_walk(file, state, cost, depth, max_depth, node_id, action, counter):
    file.write("    " + node_id + " [label=" + board_dot_label(action, state, cost) + "];\n")
    if depth == max_depth:
        return

    kids = get_next_states(state)
    i = 0
    while i < len(kids):
        counter[0] = counter[0] + 1
        child_id = "n" + str(counter[0])
        file.write("    " + node_id + " -> " + child_id + " [label=\"" + kids[i][1] + "\"];\n")
        write_dot_walk(file, kids[i][0], cost, depth + 1, max_depth, child_id, kids[i][1], counter)
        i = i + 1


def write_dot_file(start_state, cost, max_depth, path):
    file = open(path, "w")
    file.write("digraph SearchTree {\n")
    file.write("    rankdir=TB;\n")
    file.write("    node [shape=plaintext, fontname=\"Courier\"];\n")
    file.write("    nodesep=0.5;\n")
    file.write("    ranksep=0.7;\n")
    counter = [0]
    write_dot_walk(file, start_state, cost, 0, max_depth, "n0", "start", counter)
    file.write("}\n")
    file.close()


def print_tree_portion(start_state, cost, max_depth, dot_path):
    write_dot_file(start_state, cost, max_depth, dot_path)
    print("Graphviz tree written to: " + dot_path)
    print("Render it at https://edotor.net")


def print_compact_path(path):
    if path is None:
        print("No solution found.")
        return

    steps = len(path) - 1
    print("Start board:")
    print_board(path[0][0])
    print("")
    print("Goal board:")
    print_board(path[len(path) - 1][0])
    print("")

    line = ""
    i = 1
    while i < len(path):
        if i > 1:
            line = line + " "
        line = line + path[i][1]
        i = i + 1
    print("Moves (" + str(steps) + "):")
    print(line)


def print_stats(name, path, generated, expanded, elapsed, best_h, finished):
    if path is None:
        length = "-"
        if finished == True:
            note = "no path"
        else:
            note = "stopped (best h=" + str(best_h) + ")"
    else:
        length = str(len(path) - 1)
        note = "ok"
    time_text = str(round(elapsed, 2))
    print(
        name.ljust(28)
        + " path="
        + length.ljust(8)
        + " generated="
        + str(generated).ljust(10)
        + " expanded="
        + str(expanded).ljust(10)
        + " time="
        + time_text.ljust(8)
        + "s  "
        + note
    )


if __name__ == "__main__":
    start_state = build_board(START_QUADRANTS, START_INSIDE)
    goal_state = build_board(GOAL_QUADRANTS, GOAL_INSIDE)
    cost = build_goal_tables(goal_state)
    neigh = neighbors_of_blank()

    print("\n.: 80-tile puzzle :.\n")
    print("Start: ")
    print_board(start_state)
    print("")
    print("Goal: ")
    print_board(goal_state)
    print("")
    print("Manhattan distance of the start: " + str(manhattan_distance(start_state, cost)))
    print("")

    if is_solvable(start_state, goal_state) == False:
        print("This start cannot reach the goal (parity test failed).")
    else:
        print("The start is solvable (permutation parity matches the blank taxicab parity).")
        print("")
        script_folder = os.path.dirname(__file__)
        if script_folder == "":
            script_folder = "."
        dot_path = script_folder + "/Exercise02_tree.dot"
        print_tree_portion(start_state, cost, 2, dot_path)
        print("")

        print("\n----o---- A* (f = g + h) ----o----")
        a_path, a_gen, a_exp, a_time, a_best, a_done = a_star(
            start_state, cost, neigh, 250000, 30
        )
        if a_path is None:
            print("No solution within the limit. Expanded " + str(a_exp) + " states. Best h = " + str(a_best) + ".")
        else:
            print_compact_path(a_path)
        print("")

        print("\n----o---- Weighted A* (f = g + 10*h) ----o----")
        w_path, w_gen, w_exp, w_time, w_best, w_done = weighted_a_star(
            start_state, cost, neigh, 10, 1000000, 60
        )
        if w_path is None:
            print("No solution within the limit. Expanded " + str(w_exp) + " states. Best h = " + str(w_best) + ".")
        else:
            print("Found a path of " + str(len(w_path) - 1) + " moves.")
        print("")

        print("\n----o---- Beam search (width = 500) ----o----")
        b500_path, b500_gen, b500_exp, b500_time, b500_best, b500_done = beam_search(
            start_state, cost, neigh, 500, 4000, 90
        )
        if b500_path is None:
            print("No solution within the limit. Expanded " + str(b500_exp) + " states. Best h = " + str(b500_best) + ".")
        else:
            print("Found a path of " + str(len(b500_path) - 1) + " moves.")
        print("")

        print("\n----o---- Beam search (width = 5000) ----o----")
        b5000_path, b5000_gen, b5000_exp, b5000_time, b5000_best, b5000_done = beam_search(
            start_state, cost, neigh, 5000, 4000, 90
        )
        if b5000_path is None:
            print("No solution within the limit. Expanded " + str(b5000_exp) + " states. Best h = " + str(b5000_best) + ".")
        else:
            print("Found a path of " + str(len(b5000_path) - 1) + " moves.")
        print("")

        best_path = None
        best_len = -1
        if w_path is not None:
            best_path = w_path
            best_len = len(w_path) - 1
        if b500_path is not None:
            n = len(b500_path) - 1
            if best_path is None or n < best_len:
                best_path = b500_path
                best_len = n
        if b5000_path is not None:
            n = len(b5000_path) - 1
            if best_path is None or n < best_len:
                best_path = b5000_path
                best_len = n

        print("----o---- Shortest path found among the solvers above ----o----\n")
        print_compact_path(best_path)
        print("")

        print("\n----o---- Comparison ----o----")
        print_stats("A*", a_path, a_gen, a_exp, a_time, a_best, a_done)
        print_stats("Weighted A* (W=10)", w_path, w_gen, w_exp, w_time, w_best, w_done)
        print_stats("Beam (k=500)", b500_path, b500_gen, b500_exp, b500_time, b500_best, b500_done)
        print_stats("Beam (k=5000)", b5000_path, b5000_gen, b5000_exp, b5000_time, b5000_best, b5000_done)