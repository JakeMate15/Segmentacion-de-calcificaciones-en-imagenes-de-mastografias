import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('nc.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar el operador Prewitt en la dirección X
kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
image_prewitt_x = cv2.filter2D(image, -1, kernel_x)

# Aplicar el operador Prewitt en la dirección Y
kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
image_prewitt_y = cv2.filter2D(image, -1, kernel_y)

# Combinar las imágenes resultantes en la dirección X e Y para obtener el gradiente total
gradient_magnitude = cv2.addWeighted(image_prewitt_x, 0.5, image_prewitt_y, 0.5, 0)

# Guardar el resultado en un archivo
cv2.imwrite('resultado_prewitt.jpg', gradient_magnitude)

# Mostrar las imágenes resultantes
cv2.imshow('Imagen original', image)
cv2.imshow('Operador Prewitt en X', image_prewitt_x)
cv2.imshow('Operador Prewitt en Y', image_prewitt_y)
cv2.imshow('Gradiente total', gradient_magnitude)

cv2.waitKey(0)
cv2.destroyAllWindows()
