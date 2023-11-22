import cv2
import numpy as np
from scipy import ndimage

def procesar_imagen(ruta_imagen):
    # Cargar la imagen
    img = cv2.imread(ruta_imagen)

    # Convertir a escala de grises
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro mínimo 15 veces
    for _ in range(15):
        gris = cv2.erode(gris, None)

    # Aplicar filtro mediana
    mediana = cv2.medianBlur(gris, 9)

    # Aplicar el filtro Sobel
    dx = ndimage.sobel(mediana, axis=0)
    dy = ndimage.sobel(mediana, axis=1)
    sobel = np.hypot(dx, dy)
    sobel = sobel / np.max(sobel)  # Normalización

    # Convertir a formato de imagen en escala de grises
    sobel = (sobel * 255).astype(np.uint8)

    _, umbralizada = cv2.threshold(sobel, 5, 255, cv2.THRESH_BINARY)


    return umbralizada

# Usar la función con una ruta de imagen específica
ruta_imagen = 'img_1_enfermo.jpg'
imagen_procesada = procesar_imagen(ruta_imagen)

# Guardar o mostrar la imagen resultante
cv2.imwrite('imagen_procesada.jpg', imagen_procesada)
cv2.imshow('Imagen Procesada', imagen_procesada)
cv2.waitKey(0)
cv2.destroyAllWindows()
