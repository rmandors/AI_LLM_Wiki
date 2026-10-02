import numpy as np
import matplotlib.pyplot as plt

N_CITIES = 25
PLANE_SIZE = 100.0

N_ANTS = 100
EPOCHS = 100
Q = 100      # Pheromone deposit factor
ALPHA = 1.0  # Pheromone importance
BETA = 1.0   # Heuristic importance
EVAPORATION_RATE = 0.5  


def create_cities(n):
    return np.random.uniform(0.0, PLANE_SIZE, size=(n, 2))


def distance_matrix(cities):
    # Symmetric Euclidean distances. Diagonal stays 0 to avoid self-loops
    n = len(cities)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dx = cities[i][0] - cities[j][0]
            dy = cities[i][1] - cities[j][1]
            d = (dx * dx + dy * dy) ** 0.5
            dist[i][j] = d
            dist[j][i] = d
    return dist


def nearest_neighbor_tour(dist):
    n = len(dist)
    start = int(np.random.randint(n))
    tour = [start]
    visited = []
    for i in range(n):
        visited.append(False)
    visited[start] = True

    for step in range(n - 1):
        i = tour[len(tour) - 1]
        best_j = -1
        best_d = 0.0
        for j in range(n):
            if visited[j]:
                continue
            if best_j == -1 or dist[i][j] < best_d:
                best_j = j
                best_d = dist[i][j]
        tour.append(best_j)
        visited[best_j] = True

    return tour


def tour_length(tour, dist):
    length = 0.0
    n = len(tour)
    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]
        length += dist[a][b]
    return length


def construct_tour(pheromone, heuristic):
    n = len(pheromone)
    start = int(np.random.randint(n))
    tour = [start]
    visited = []
    for i in range(n):
        visited.append(False)
    visited[start] = True

    for step in range(n - 1):
        i = tour[len(tour) - 1]
        allowed = []
        weights = []
        for j in range(n):
            if visited[j]:
                continue
            weight = (pheromone[i][j] ** ALPHA) * (heuristic[i][j] ** BETA)
            allowed.append(j)
            weights.append(weight)

        total = 0.0
        for w in weights:
            total += w

        if total <= 0.0:
            pick = int(np.random.randint(len(allowed)))
            j = allowed[pick]
        else:
            r = np.random.random() * total
            cumulative = 0.0
            j = allowed[len(allowed) - 1]
            for index in range(len(allowed)):
                cumulative += weights[index]
                if cumulative >= r:
                    j = allowed[index]
                    break

        tour.append(j)
        visited[j] = True

    return tour


def update_pheromone(pheromone, tours, lengths):
    n = len(pheromone)
    factor = 1.0 - EVAPORATION_RATE
    for i in range(n):
        for j in range(n):
            pheromone[i][j] *= factor

    for k in range(len(tours)):
        tour = tours[k]
        deposit = Q / lengths[k]
        n_tour = len(tour)
        for i in range(n_tour):
            a = tour[i]
            b = tour[(i + 1) % n_tour]
            pheromone[a][b] += deposit
            pheromone[b][a] += deposit
    return pheromone


def heuristic_matrix(dist):
    n = len(dist)
    heuristic = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                heuristic[i][j] = 1.0 / dist[i][j]
    return heuristic


def initialize_pheromone(dist):
    # Pheromone starts at the same value on every edge
    n = len(dist)
    initial_tour = nearest_neighbor_tour(dist)
    tau0 = 1.0 / (n * tour_length(initial_tour, dist))
    pheromone = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                pheromone[i][j] = tau0
    return pheromone, initial_tour


def run_ants(pheromone, heuristic, dist):
    tours = []
    lengths = []
    for k in range(N_ANTS):
        tour = construct_tour(pheromone, heuristic)
        tours.append(tour)
        lengths.append(tour_length(tour, dist))

    pheromone = update_pheromone(pheromone, tours, lengths)

    best_index = 0
    for k in range(len(lengths)):
        if lengths[k] < lengths[best_index]:
            best_index = k
    return pheromone, tours[best_index], lengths[best_index]


def plot_results(cities, history, best_tour, best_length):
    xs = []
    ys = []
    for i in range(len(best_tour)):
        city = best_tour[i]
        xs.append(cities[city][0])
        ys.append(cities[city][1])
    xs.append(cities[best_tour[0]][0])
    ys.append(cities[best_tour[0]][1])

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    axes[0].plot(range(len(history)), history)
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Best tour length")
    axes[0].set_title("ACO: best tour length vs epoch")
    axes[0].grid(True)

    axes[1].plot(xs, ys, "-o", markersize=4)
    axes[1].scatter(cities[best_tour[0]][0], cities[best_tour[0]][1], c="red", s=40, zorder=3)
    axes[1].set_xlim(0, PLANE_SIZE)
    axes[1].set_ylim(0, PLANE_SIZE)
    axes[1].set_aspect("equal")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("y")
    axes[1].set_title(f"Best tour (length {best_length:.2f})")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    cities = create_cities(N_CITIES)
    dist = distance_matrix(cities)
    heuristic = heuristic_matrix(dist)
    pheromone, best_tour = initialize_pheromone(dist)
    best_length = tour_length(best_tour, dist)
    history = [best_length]

    print("\n.: Ant Colony Optimization (ACO):.")
    print(f"\n{N_CITIES} cities in a {PLANE_SIZE:.0f}x{PLANE_SIZE:.0f} plane, fully connected.")
    print(f"Nearest-neighbor tour length: {best_length:.4f}\n")

    for epoch in range(EPOCHS):
        pheromone, epoch_tour, epoch_length = run_ants(pheromone, heuristic, dist)
        if epoch_length < best_length:
            best_tour = epoch_tour
            best_length = epoch_length
        history.append(best_length)
        print(f"Epoch {epoch + 1}: Best tour length: {best_length:.4f}")

    closed = []
    for city in best_tour:
        closed.append(city)
    closed.append(best_tour[0])
    print(f"\nBest tour: {closed}")
    print(f"Best tour length: {best_length:.4f}")
    plot_results(cities, history, best_tour, best_length)