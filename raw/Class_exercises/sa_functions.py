import numpy as np
import matplotlib.pyplot as plt

def simulated_annealing(func, bounds, max_iter, initial_temp, cooling_rate):
    # Generar una solución inicial aleatoria dentro de los límites
    current_solution = np.array([np.random.uniform(low, high) for low, high in bounds])
    current_value = func(current_solution)
    best_solution = current_solution.copy()
    best_value = current_value
    temperature = initial_temp
    values = []

    for i in range(max_iter):
        # Generar una nueva solución cercana
        new_solution = current_solution + np.random.uniform(-1, 1, size=len(bounds))
        # Asegurarse de que la nueva solución esté dentro de los límites
        new_solution = np.clip(new_solution, [low for low, high in bounds], [high for low, high in bounds])
        new_value = func(new_solution)

        # Calcular la diferencia de energía
        delta = new_value - current_value

        # Decidir si se acepta la nueva solución
        if delta < 0 or np.random.rand() < np.exp(-delta / temperature):
            current_solution = new_solution
            current_value = new_value

            # Actualizar la mejor solución encontrada
            if new_value < best_value:
                best_solution = new_solution
                best_value = new_value

        # Enfriar la temperatura
        temperature *= cooling_rate
        values.append(current_value)

    return best_solution, best_value, values

# Definir la función objetivo a minimizar
def objective_function(x):
    # Ejemplo: Función de Rastrigin en 2D
    return 10 * len(x) + sum([xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x])

def objective_f2(x):
    # Ackley Function
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))) - np.exp(
        0.5 * (np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[1]))) + np.e + 20

# Parámetros
bounds = [(-5.12, 5.12), (-5.12, 5.12)]  # Límites para cada dimensión
max_iter = 100000
initial_temp = 100
cooling_rate = 0.8

# Ejecutar el algoritmo
best_sol, best_val, history = simulated_annealing(objective_function, bounds, max_iter, initial_temp, cooling_rate)

print(f"Mejor solución encontrada: {best_sol}")
print(f"Valor de la función objetivo: {best_val}")

# Graficar el progreso de la optimización
plt.plot(history)
plt.xlabel('Iteraciones')
plt.ylabel('Valor de la función objetivo')
plt.title('Progreso del Simulated Annealing')
plt.show()