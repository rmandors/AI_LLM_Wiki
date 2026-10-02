import numpy as np
import matplotlib.pyplot as plt

# Objective: minimize f(x, y) = (x+2)^2 + (y-2)^2 + 10
def objective(x, y):
    return (x + 2)**2 + (y - 2)**2 + 10

# Individual: 16 bits = | sign + 7 bits for x | sign + 7 bits for y |
# Magnitude range: 0..127 / 10  -->  [0.0, 12.7]
BITS_PER_VAR = 8
CHROMOSOME_LENGTH = BITS_PER_VAR * 2
SCALE = 10.0


def random_individual():
    return "".join(np.random.choice(["0", "1"], CHROMOSOME_LENGTH))


def decode_variable(bits):
    sign = -1 if bits[0] == "1" else 1
    magnitude = int(bits[1:], 2) / SCALE
    return sign * magnitude


def decode_individual(chromosome):
    x = decode_variable(chromosome[:BITS_PER_VAR])
    y = decode_variable(chromosome[BITS_PER_VAR:])
    return x, y


def fitness(chromosome):
    x, y = decode_individual(chromosome)
    return objective(x, y)


def crossover(parent1, parent2):
    # Single-point crossover
    point = np.random.randint(1, len(parent1))
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(chromosome, mutation_rate=None):
    # Uniform bit-flip: each bit is flipped independently with the same probability
    if mutation_rate is None:
        mutation_rate = 1.0 / len(chromosome)
    bits = list(chromosome)
    for i in range(len(bits)):
        if np.random.rand() < mutation_rate:
            bits[i] = "1" if bits[i] == "0" else "0"
    return "".join(bits)


if __name__ == "__main__":
    # Genetic algorithm parameters
    population_size = 100
    num_epochs = 100
    k_elites = 10

    # Initialize population
    population = [random_individual() for _ in range(population_size)]

    best_chromosome = min(population, key=fitness)
    best_xy = decode_individual(best_chromosome)
    best_f = fitness(best_chromosome)
    history = [best_f]
    print(f"\nStarting point: {best_xy}")
    print(f"Initial value of f: {best_f}\n")

    for epoch in range(num_epochs):
        # Rank individuals by fitness (minimize)
        ranked = sorted(population, key=fitness)

        # Keep the k=10 best individuals
        elites = ranked[:k_elites]
        next_population = elites[:]

        # Fill the rest with single-point crossover of elite parents, then mutate
        while len(next_population) < population_size:
            i, j = np.random.randint(0, k_elites, size=2)
            child1, child2 = crossover(elites[i], elites[j])
            next_population.append(mutate(child1))
            if len(next_population) < population_size:
                next_population.append(mutate(child2))

        population = next_population

        epoch_best = min(population, key=fitness)
        epoch_xy = decode_individual(epoch_best)
        epoch_f = fitness(epoch_best)
        history.append(epoch_f)
        if epoch_f < best_f:
            best_chromosome = epoch_best
            best_xy = epoch_xy
            best_f = epoch_f

        print(f"Epoch {epoch + 1}, (x, y) = {epoch_xy}, f = {epoch_f:.2f}")

    x_star, y_star = best_xy
    print(f"\nBest solution found (x*, y*) = {x_star, y_star}")
    print(f"Minimum value of f: {best_f}")

    plt.plot(range(len(history)), history)
    plt.xlabel("Epoch")
    plt.ylabel("f(best solution)")
    plt.title("Genetic Algorithm: best fitness vs epoch")
    plt.grid(True)
    plt.tight_layout()
    plt.show()