import cv2
import numpy as np

# Carga la imagen
image = cv2.imread('imagenEcualizada.jpg', cv2.IMREAD_GRAYSCALE)

# Definir el filtro Prewitt horizontal
kernel_x = np.array([[-1, 0, 1],
                     [-1, 0, 1],
                     [-1, 0, 1]])

# Definir el filtro Prewitt vertical
kernel_y = np.array([[-1, -1, -1],
                     [0, 0, 0],
                     [1, 1, 1]])

# Aplicar la convolución con los filtros Prewitt
horizontal_edge = cv2.filter2D(image, -1, kernel_x)
vertical_edge = cv2.filter2D(image, -1, kernel_y)

# Aumentar el contraste de las imágenes
horizontal_edge_contrast = cv2.convertScaleAbs(horizontal_edge, alpha=2, beta=0)
vertical_edge_contrast = cv2.convertScaleAbs(vertical_edge, alpha=2, beta=0)

# Mostrar las imágenes resultantes
cv2.imshow('Horizontal Edge (Contrast)', horizontal_edge_contrast)
cv2.imshow('Vertical Edge (Contrast)', vertical_edge_contrast)
cv2.waitKey(0)
cv2.destroyAllWindows()
