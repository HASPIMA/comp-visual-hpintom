from pathlib import Path

import matplotlib.pyplot as plt
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

# Crear carpeta graficos si no existe
folder = Path('graficos')
folder.mkdir(exist_ok=True)

# Graficar y guardar señal original
plt.figure(figsize=(6, 3))
plt.stem(senal)
plt.title('Señal de entrada')
plt.tight_layout()
plt.savefig(folder / 'señal_original.png')
plt.close()

# Graficar y guardar kernel
plt.figure(figsize=(6, 3))
plt.stem(kernel)
plt.title('Kernel')
plt.tight_layout()
plt.savefig(folder / 'kernel.png')
plt.close()

# Graficar y guardar resultado
plt.figure(figsize=(6, 3))
plt.stem(resultado)
plt.title('Resultado de la convolución')
plt.tight_layout()
plt.savefig(folder / 'resultado.png')
plt.close()

# 4. Graficar la señal, el kernel y el resultado
fig, axs = plt.subplots(3, 1, figsize=(8, 8))
axs[0].stem(senal)
axs[0].set_title('Señal de entrada')
axs[1].stem(kernel)
axs[1].set_title('Kernel')
axs[2].stem(resultado)
axs[2].set_title('Resultado de la convolución')
plt.tight_layout()
plt.show()
