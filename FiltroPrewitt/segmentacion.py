import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('n.png', 0)  # Lee la imagen en escala de grises

# Aplicar la segmentación por umbral (ajusta el valor del umbral según tus necesidades)
threshold_value = 25
_, thresholded_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

# Mostrar la imagen original y la imagen segmentada
cv2.imshow('Imagen Original', image)
cv2.imshow('Imagen Segmentada', thresholded_image)

# Esperar a que se presione una tecla y luego cerrar las ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()
