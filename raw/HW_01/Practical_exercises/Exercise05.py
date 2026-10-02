"""
Artificial Intelligence
NRC: 1651

Raymond Portilla
Banner ID: 00335050

Exercise 05: Missionaries and Cannibals Problem
"""

from collections import deque

BOAT_LOADS = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]


def is_legal(state):
    m_left = state[0]
    c_left = state[1]
    m_right = 3 - m_left
    c_right = 3 - c_left

    if m_left < c_left and m_left > 0:
        return False
    if m_right < c_right and m_right > 0:
        return False
    return True


def describe_action(dm, dc, going_right):
    text = str(dm) + " missionary(ies) and " + str(dc) + " cannibal(s)"
    if going_right == True:
        return text + " cross the river"
    else:
        return text + " return"


def get_next_states(state):
    m_left = state[0]
    c_left = state[1]
    boat_left = state[2]
    results = []

    i = 0
    while i < len(BOAT_LOADS):
        load = BOAT_LOADS[i]
        dm = load[0]
        dc = load[1]
        new_state = list(state)

        if boat_left == True:
            if dm > m_left or dc > c_left:
                i = i + 1
                continue
            new_state[0] = new_state[0] - dm
            new_state[1] = new_state[1] - dc
            new_state[2] = False
            action = describe_action(dm, dc, True)
        else:
            m_right = 3 - m_left
            c_right = 3 - c_left
            if dm > m_right or dc > c_right:
                i = i + 1
                continue
            new_state[0] = new_state[0] + dm
            new_state[1] = new_state[1] + dc
            new_state[2] = True
            action = describe_action(dm, dc, False)

        new_state = tuple(new_state)
        if is_legal(new_state) == True:
            results.append((new_state, action))

        i = i + 1

    return results


def bfs(start_state, goal_state):
    queue = deque()
    queue.append(start_state)
    visited = set()
    visited.add(start_state)
    parent = {}
    parent[start_state] = (None, None)

    while len(queue) > 0:
        current_state = queue.popleft()
        if current_state == goal_state:
            return reconstruct_path(parent, current_state)

        next_options = get_next_states(current_state)
        j = 0
        while j < len(next_options):
            option = next_options[j]
            next_state = option[0]
            action = option[1]
            already_seen = next_state in visited
            if already_seen == False:
                visited.add(next_state)
                parent[next_state] = (current_state, action)
                queue.append(next_state)
            j = j + 1

    return None


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


def print_solution(path):
    if path is None:
        print("No solution found.")
        return

    print("Start: All on the left side")
    first_item = path[0]
    print_state(first_item[0])

    i = 1
    while i < len(path):
        item = path[i]
        state = item[0]
        action = item[1]
        print("")
        print("Action: " + action)
        print_state(state)
        i = i + 1

    steps = len(path) - 1
    print("")
    print("Successfully completed in " + str(steps) + " steps.")


def print_state(state):
    m_left = state[0]
    c_left = state[1]
    boat_left = state[2]
    m_right = 3 - m_left
    c_right = 3 - c_left

    print("  - Missionaries: " + str(m_left) + " on the left, " + str(m_right) + " on the right")
    print("  - Cannibals: " + str(c_left) + " on the left, " + str(c_right) + " on the right")
    if boat_left == True:
        boat_side = "left"
    else:
        boat_side = "right"
    print("  - Boat: " + boat_side)


if __name__ == "__main__":
    print("\n.: Missionaries and Cannibals Problem :. \n")
    start_state = (3, 3, True)
    goal_state = (0, 0, False)
    solution = bfs(start_state, goal_state)
    print_solution(solution)