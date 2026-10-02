import numpy as np

NUMBER_OF_PARTICLES = 100
EPOCHS = 100
DIMENSIONS = 2

ALPHA1 = 2.0  # Cognitive component weight
ALPHA2 = 2.0  # Social component weight

LOWER_BOUND = -10.0
UPPER_BOUND = 10.0


def objective(position):
    # f(x, y) = (x+2)^2 + (y-2)^2 + 10
    target = np.zeros(len(position))
    target[0] = -2.0
    if len(position) > 1:
        target[1] = 2.0
    return float(np.sum((position - target) ** 2) + 10)


def initialize_particles():
    particles = []
    global_best_position = None
    global_best_fitness = np.inf

    for _ in range(NUMBER_OF_PARTICLES):
        position = np.random.uniform(LOWER_BOUND, UPPER_BOUND, DIMENSIONS)
        velocity = np.zeros(DIMENSIONS)
        fitness_value = objective(position)

        if fitness_value < global_best_fitness:
            global_best_position = position.copy()
            global_best_fitness = fitness_value

        particles.append({
            'position': position,
            'velocity': velocity,
            'personal_best_position': position.copy(),
            'personal_best_fitness': fitness_value,
        })

    return particles, global_best_position, global_best_fitness


def update_particles(particles, global_best_position):
    for particle in particles:
        phi1 = np.random.random()
        phi2 = np.random.random()

        cognitive_component = ALPHA1 * phi1 * (particle['personal_best_position'] - particle['position'])
        social_component = ALPHA2 * phi2 * (global_best_position - particle['position'])
        particle['velocity'] = particle['velocity'] + cognitive_component + social_component
        particle['position'] = particle['position'] + particle['velocity']


def evaluate_particles(particles, global_best_position, global_best_fitness):
    for particle in particles:
        fitness_value = objective(particle['position'])

        if fitness_value < particle['personal_best_fitness']:
            particle['personal_best_position'] = particle['position'].copy()
            particle['personal_best_fitness'] = fitness_value

        if fitness_value < global_best_fitness:
            global_best_position = particle['position'].copy()
            global_best_fitness = fitness_value

    return global_best_position, global_best_fitness


if __name__ == "__main__":
    particles, global_best_position, global_best_fitness = initialize_particles()

    print(f"\n.: Particle Swarm Optimization :.")
    print(f"\nStarting point: {global_best_position}")
    print(f"Initial value of f: {global_best_fitness}\n")

    for epoch in range(EPOCHS):
        update_particles(particles, global_best_position)
        global_best_position, global_best_fitness = evaluate_particles(
            particles, global_best_position, global_best_fitness
        )

        if (epoch + 1) <= 10 or (epoch + 1) % 10 == 0:            
            print(
                f"Epoch {epoch + 1}: Best position: {global_best_position}, "
                f"Best value of f: {global_best_fitness}"
            )