"""
Artificial Intelligence
NRC: 1651

Raymond Portilla
Banner ID: 00335050

Exercise 04: Farmer, Wolf, Goat, and Cabbage Problem
"""

from collections import deque

Actions = [
    "Farmer goes alone",
    "Farmer takes wolf",
    "Farmer takes goat",
    "Farmer takes cabbage",
]

State = [
    "Farmer",
    "Wolf",
    "Goat",
    "Cabbage",
]


def is_legal(state):
    farmer = state[0]
    wolf = state[1]
    goat = state[2]
    cabbage = state[3]

    if wolf == goat and farmer != wolf:
        return False
    if goat == cabbage and farmer != goat:
        return False
    return True


def flip_side(value):
    if value == True:
        return False
    else:
        return True


def get_next_state(state, action):
    new_state = list(state)

    if action == "Farmer goes alone":
        new_state[0] = flip_side(new_state[0])
        return new_state

    if action == "Farmer takes wolf":
        index = 1
    elif action == "Farmer takes goat":
        index = 2
    elif action == "Farmer takes cabbage":
        index = 3
    else:
        return None

    # The farmer can only take a passenger that's on the same side
    if state[index] != state[0]:
        return None

    new_state[0] = flip_side(new_state[0])
    new_state[index] = flip_side(new_state[index])
    return new_state


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

        for action in Actions:
            next_state = get_next_state(current_state, action)
            if next_state is None:
                continue
            next_state = tuple(next_state)
            already_seen = next_state in visited
            if already_seen == False:
                if is_legal(next_state) == True:
                    visited.add(next_state)
                    parent[next_state] = (current_state, action)
                    queue.append(next_state)

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
    print("Start: All on the right side")
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


def side_name(is_right):
    if is_right == True:
        return "Right"
    else:
        return "Left"


def print_state(state):
    farmer_side = side_name(state[0])
    wolf_side = side_name(state[1])
    goat_side = side_name(state[2])
    cabbage_side = side_name(state[3])

    print("  - Farmer: " + farmer_side)
    print("  - Wolf: " + wolf_side)
    print("  - Goat: " + goat_side)
    print("  - Cabbage: " + cabbage_side)


if __name__ == "__main__":
    print("\n.: Farmer, Wolf, Goat, and Cabbage Problem :. \n")
    start_state = (True, True, True, True)
    goal_state = (False, False, False, False)
    solution = bfs(start_state, goal_state)
    if solution is not None:
        print_solution(solution)
    else:
        print("No solution found.")