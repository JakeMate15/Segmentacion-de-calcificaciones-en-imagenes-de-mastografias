import cv2
import numpy as np

# Cargar la imagen preprocesada en escala de grises
image = cv2.imread('n.png', cv2.IMREAD_GRAYSCALE)

# Obtener las dimensiones de la imagen
height, width = image.shape

# Aplicar el método de umbralización de Otsu
_, thresholded = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Guardar la imagen umbralizada resultante
cv2.imwrite('imagen_umbralizada_otsu.png', thresholded)

# Crear un archivo de texto para guardar la matriz de la imagen
with open('matriz_imagen.txt', 'w') as file:
    # Escribir las dimensiones de la imagen al principio del archivo
    file.write(f"{height} {width}\n")
    
    # Escribir la matriz de la imagen
    for row in thresholded:
        row_data = ' '.join(map(str, row))
        file.write(f"{row_data}\n")
