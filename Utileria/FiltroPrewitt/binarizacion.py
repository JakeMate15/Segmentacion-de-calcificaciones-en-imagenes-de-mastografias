import cv2

# Carga la imagen en escala de grises
imagen = cv2.imread('resultado_prewitt.jpg', cv2.IMREAD_GRAYSCALE)

# Especifica un umbral (threshold)
umbral = 20

# Aplica la binarización
_, imagen_binaria = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)

# Guarda la imagen binaria
cv2.imwrite('imagen_binaria.jpg', imagen_binaria)

# Muestra la imagen binaria
cv2.imshow('Imagen Binarizada', imagen_binaria)
cv2.waitKey(0)
cv2.destroyAllWindows()
