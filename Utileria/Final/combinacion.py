import cv2
import numpy as np

# Carga la imagen en color
imagen_color = cv2.imread('img5.jpg')

# Carga la imagen en blanco y negro
imagen_bn = cv2.imread('imagen_binaria.png', cv2.IMREAD_GRAYSCALE)

# Asegúrate de que ambas imágenes tengan el mismo tamaño
imagen_bn = cv2.resize(imagen_bn, (imagen_color.shape[1], imagen_color.shape[0]))

# Convierte la imagen en blanco y negro a una imagen de un solo canal (escala de grises)
imagen_roja = cv2.merge([imagen_bn, np.zeros_like(imagen_bn), np.zeros_like(imagen_bn)])

# Superponer la imagen en blanco y negro (roja) en la imagen en color
superpuesta = cv2.addWeighted(imagen_color, 1, imagen_roja, 0.7, 0)

# Guarda la imagen superpuesta
cv2.imwrite('imagen_superpuesta.jpg', superpuesta)

# Muestra la imagen superpuesta (opcional)
cv2.imshow('Imagen Superpuesta', superpuesta)
cv2.waitKey(0)
cv2.destroyAllWindows()
