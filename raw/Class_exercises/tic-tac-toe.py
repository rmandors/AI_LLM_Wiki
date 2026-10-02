combinaciones = [
    (0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15),  # Filas
    (0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),  # Columnas
    (0, 5, 10, 15), (3, 6, 9, 12)  # Diagonales
]

def mostrar_tablero(tablero):
    """
    Muestra el tablero en la consola.
    'tablero' es una lista de 16 elementos, cada uno puede ser ' ', 'X' o 'O'.
    """
    print()
    print(f" {tablero[0]} | {tablero[1]} | {tablero[2]} | {tablero[3]} ")
    print("---+---+---+---")
    print(f" {tablero[4]} | {tablero[5]} | {tablero[6]} | {tablero[7]} ")
    print("---+---+---+---")
    print(f" {tablero[8]} | {tablero[9]} | {tablero[10]} | {tablero[11]} ")
    print("---+---+---+---")
    print(f" {tablero[12]} | {tablero[13]} | {tablero[14]} | {tablero[15]} ")
    print()


def hay_ganador(tablero):
    """
    Devuelve 'X' si gana X, 'O' si gana O, o None si no hay ganador.
    """
    # Todas las combinaciones de 4 en raya
    for (a, b, c, d) in combinaciones:
        if tablero[a] == tablero[b] == tablero[c] == tablero[d] and tablero[a] != ' ':
            return tablero[a]
    return None


def tablero_lleno(tablero):
    """
    Devuelve True si el tablero está lleno (sin casillas vacías), de lo contrario False.
    """
    return ' ' not in tablero


def evaluar(tablero):
    """
    Función de evaluación para el estado del tablero.
    Devuelve +1 si gana X, -1 si gana O, o 0 si nadie ha ganado.
    """
    ganador = hay_ganador(tablero)
    if ganador == 'X':
        return +1
    elif ganador == 'O':
        return -1
    else:
        return 0


def movimientos_disponibles(tablero):
    """
    Devuelve una lista con los índices de las casillas libres en el tablero.
    Ya ordenadas, para que el alpha-beta pruning sea más eficiente.
    """
    orden_preferido = [
        5, 6, 9, 10, # Centro
        0, 3, 12, 15, # Esquinas
        1, 2, 4, 7, 8, 11, 13, 14 # Lados
    ]
    return [i for i in orden_preferido if tablero[i] == ' ']


def h_minimax(tablero, es_turno_de_X, alpha=float('-inf'), beta=float('inf'), profundidad=0, max_profundidad=7):
    """
    H-MINIMAX search with Alpha-Beta pruning and a depth-based cutoff test.
    Devuelve una tupla (valor, movimiento) donde:
    - valor: es la evaluación del tablero (+1, 0, -1).
    - movimiento: es el índice de la posición óptima en el tableroque lleva a ese 
      valor (puede ser None si es un estado terminal).
    - alpha: mejor valor (más alto) que MAX puede garantizar hasta ahora (at least).
    - beta: mejor valor (más bajo) que MIN puede garantizar hasta ahora (at most).
    """
    # Primero, revisamos si el estado es terminal (ganador o empate)
    puntaje = evaluar(tablero)
    if puntaje == 1:  # Gana X
        return (puntaje, None)
    if puntaje == -1:  # Gana O
        return (puntaje, None)
    if tablero_lleno(tablero):  # Empate
        return (0, None)

    if is_cutoff(profundidad, max_profundidad):
        return (eval_heuristica(tablero), None)

    # Obtenemos todos los movimientos posibles (casillas libres)
    moves = movimientos_disponibles(tablero)

    if es_turno_de_X:
        # MAXimiza (X)
        mejor_valor = float('-inf')
        mejor_movimiento = None
        for move in moves:
            # Simulamos la jugada
            tablero[move] = 'X'
            valor, _ = h_minimax(tablero, False, alpha, beta, profundidad + 1, max_profundidad)
            tablero[move] = ' '  # Revertir cambio

            # Actualizamos el mejor valor si encontramos una mejor opción
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = move

                # X ya no puede mejorar (MIN root rechazará esta rama)
                alpha = max(alpha, mejor_valor)
                if mejor_valor >= beta:
                    break

        return (mejor_valor, mejor_movimiento)

    else:
        # MINimiza (O)
        mejor_valor = float('inf')
        mejor_movimiento = None
        for move in moves:
            # Simulamos la jugada
            tablero[move] = 'O'
            valor, _ = h_minimax(tablero, True, alpha, beta, profundidad + 1, max_profundidad)
            tablero[move] = ' '  # Revertir cambio

            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = move

                # O ya no puede empeorar (MAX root rechazará esta rama)
                beta = min(beta, mejor_valor)
                if mejor_valor <= alpha:
                    break

        return (mejor_valor, mejor_movimiento)


def is_cutoff(profundidad, max_profundidad):
    """
    Corta si se alcanza el límite de profundidad establecido.
    """
    return profundidad >= max_profundidad


def eval_heuristica(tablero):
    """
    Evaluación heurística para el estado del tablero.
    Devuelve un valor entre -1 y 1.
    """
    score = 0
    weights = {1: 1, 2: 3, 3: 9} # más peso a líneas más avanzadas

    for casilla in combinaciones:
        values = [tablero[i] for i in casilla]
        x_count = values.count('X')
        o_count = values.count('O')

        if x_count > 0 and o_count == 0:
            score += weights.get(x_count, 0)
        elif o_count > 0 and x_count == 0:
            score -= weights.get(o_count, 0)
    
    # Normalizar el score entre -1 y 1
    return max(-1, min(1, score / 90))


def jugar():
    """
    Función principal para jugar un partido humano (O) vs IA (X) usando Minimax.
    """
    # Inicializamos el tablero
    tablero = [' '] * 16

    # Elegimos quién comienza. Aquí forzamos a que el humano (O) comience
    turno = 'O'  # 'O' juega primero

    while True:
        mostrar_tablero(tablero)

        # Comprobamos estado final
        ganador = hay_ganador(tablero)
        if ganador == 'X':
            print("¡La IA (X) ha ganado!")
            break
        elif ganador == 'O':
            print("¡Felicidades, has ganado!")
            break
        elif tablero_lleno(tablero):
            print("¡Es un empate!")
            break

        if turno == 'O':
            # Turno humano
            try:
                movimiento = int(input("Elige una casilla (1-16): ")) - 1
            except ValueError:
                print("Entrada no válida. Inténtalo de nuevo.")
                continue

            if movimiento < 0 or movimiento > 15 or tablero[movimiento] != ' ':
                print("Movimiento inválido. Inténtalo de nuevo.")
                continue

            tablero[movimiento] = 'O'
            turno = 'X'  # Cambiamos el turno a la IA
        else:
            # Turno de la IA (X), utilizamos minimax para encontrar la mejor jugada
            print("La IA está pensando...")
            _, mejor_mov = h_minimax(tablero, True, max_profundidad=7)
            tablero[mejor_mov] = 'X'
            turno = 'O'  # Cambiamos el turno al humano


if __name__ == "__main__":
    jugar()