import cv2
import numpy as np

img_orignal = '1.jpg'
# Carga la imagen a color
imagen_color = cv2.imread(img_orignal)  # Asegúrate de que '1.jpg' es la ruta a tu imagen a color
# Carga la imagen para crear la máscara
imagen = cv2.imread(img_orignal, cv2.IMREAD_GRAYSCALE)  # '1.jpg' es la imagen de la que se crea la máscara

# Define el número de veces que quieres aplicar el filtro mínimo
num_repeticiones = 15

# Aplica el filtro mínimo repetidamente
for _ in range(num_repeticiones):
    imagen = cv2.erode(imagen, np.ones((3, 3), np.uint8))

# Umbraliza la imagen
umbral = 30  # Puedes ajustar este valor según tus necesidades
imagen_umbralizada = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)[1]

# Aplica la máscara a la imagen a color
imagen_resultante = cv2.bitwise_and(imagen_color, imagen_color, mask=imagen_umbralizada)

# Guarda la imagen resultante
cv2.imwrite('imagen_resultante.jpg', imagen_resultante)

# Muestra la imagen original, la imagen umbralizada y la imagen resultante
cv2.imshow('Imagen Original', imagen_color)
cv2.imshow('Imagen Umbralizada', imagen_umbralizada)
cv2.imshow('Imagen Resultante', imagen_resultante)
cv2.waitKey(0)
cv2.destroyAllWindows()
