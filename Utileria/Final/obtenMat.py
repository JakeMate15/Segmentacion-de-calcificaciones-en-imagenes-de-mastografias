from PIL import Image
import numpy as np

# Abre la imagen en formato PNG
imagen = Image.open('imgaenSegmentada.jpg')

# Convierte la imagen a una matriz NumPy
matriz = np.array(imagen)

# Umbraliza la matriz: 255 si el valor es mayor a 100, 0 en caso contrario
matriz_umbralizada = np.where(matriz > 100, 255, 0)

# Nombre del archivo de salida
nombre_archivo = "sal.txt"

# Abre el archivo en modo escritura
with open(nombre_archivo, "w") as archivo:
    # Escribe las dimensiones n y m en el archivo
    n_filas, n_columnas = matriz.shape[0], matriz.shape[1]
    archivo.write(f"{n_filas} {n_columnas}\n")

    # Escribe la matriz umbralizada en el archivo
    for fila in matriz_umbralizada:
        fila_str = ' '.join(map(str, fila))
        archivo.write(fila_str + "\n")

