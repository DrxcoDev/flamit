import random

# Función para generar datos de ejemplo
def generar_datos(num_puntos):
    X = [2 * random.random() for _ in range(num_puntos)]
    y = [4 + 3 * x + random.uniform(-1, 1) for x in X]
    return X, y

# Función para entrenar el modelo de regresión lineal
def entrenar_modelo(X, y, learning_rate, epsilon):
    # Inicializar parámetros del modelo
    theta0 = random.uniform(0, 1)
    theta1 = random.uniform(0, 1)

    prev_mse = float('inf')  # Inicializar con un valor grande

    epoch = 0
    while True:
        # Calcular predicciones
        predictions = [theta0 + theta1 * x for x in X]

        # Calcular errores
        errors = [pred - actual for pred, actual in zip(predictions, y)]

        # Calcular el error cuadrático medio (MSE)
        mse = sum(error**2 for error in errors) / len(X)

        # Imprimir el MSE en cada época
        print(f"Época {epoch+1}, MSE: {mse}")

        # Condición de parada basada en la variación del MSE
        if abs(prev_mse - mse) < epsilon:
            break

        prev_mse = mse

        # Actualizar parámetros del modelo
        theta0 -= learning_rate * sum(errors) / len(X)
        theta1 -= learning_rate * sum(x * error for x, error in zip(X, errors)) / len(X)

        epoch += 1

    return theta0, theta1

# Generar datos de entrenamiento
X, y = generar_datos(100)

# Entrenar el modelo con parada automática
learning_rate = 0.01
epsilon = 1e-6  # Umbral de variación del MSE para detener el entrenamiento
theta0, theta1 = entrenar_modelo(X, y, learning_rate, epsilon)

# Imprimir resultados finales
print("\nEntrenamiento completado.")
print("Parámetros del modelo:")
print("Theta0:", theta0)
print("Theta1:", theta1)
