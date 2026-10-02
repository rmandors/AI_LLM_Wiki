import numpy as np

# Función objetivo: f(x, y) = (x-2)^2 + (y+2)^2
def objective(w):
    """
    Calcula el valor de la función cuadrática en el punto w = [x, y].
    """
    x, y = w[0], w[1]
    return (x - 2)**2 + (y + 2)**2

# Gradiente de la función objetivo
def grad_f(w):
    """
    Calcula el gradiente de la función en el punto w = [x, y].
    Devuelve un vector [df/dx, df/dy].
    """
    x, y = w[0], w[1]
    df_dx = 2 * (x - 2)
    df_dy = 2 * (y + 2)
    return np.array([df_dx, df_dy])

# Parámetros de la optimización
eta = 0.1           # Tasa de aprendizaje
num_iterations = 1000  # Número de iteraciones
w = np.array([0.0, 0.0])  # Inicialización de (x, y), por ejemplo en (0, 0)

print("Punto inicial:", w)
print("Valor inicial de f:", objective(w))

# Bucle de descenso de gradiente
for i in range(num_iterations):
    # Calcula el gradiente
    g = grad_f(w)

    # Actualiza w en la dirección opuesta al gradiente
    w = w - eta * g

    # (Opcional) Imprimir estado en cada iteración
    print(f"Iteración {i+1}, w = {w}, f(w) = {objective(w)}")

print("\nPunto final (w):", w)
print("Valor final de f:", objective(w))