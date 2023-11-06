import cv2

# Cargar la imagen preprocesada en escala de grises
image = cv2.imread('n.png', cv2.IMREAD_GRAYSCALE)

# Aplicar el método de umbralización de Otsu
_, thresholded = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Guardar la imagen umbralizada resultante
cv2.imwrite('imagen_umbralizada_otsu.png', thresholded)
