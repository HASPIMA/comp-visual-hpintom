import numpy as np

# 1. Definir una señal de entrada de 15 valores
senal = np.array([2, 4, 6, 8, 10, 8, 6, 4, 2, 0, -2, -4, -6, -8, -10])

# 2. Definir un kernel de tamaño 3
kernel = np.array([1, 0, -1])

# 3. Implementar la función de convolución sin usar numpy.convolve
def convolucion_1d(senal, kernel):
    n = len(senal)
    k = len(kernel)
    salida = []
    pad = k // 2
    senal_padded = np.pad(
        senal, (pad, pad), mode='constant', constant_values=0)
    for i in range(n):
        window = senal_padded[i:i+k]
        valor = np.sum(window * kernel[::-1])
        salida.append(valor)
    return np.array(salida)


resultado = convolucion_1d(senal, kernel)
