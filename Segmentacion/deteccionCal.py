import cv2
import numpy as np
import argparse
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def preProcesamiento(ruta):
    img_orignal = ruta
    # Carga la imagen original
    imagen_original = cv2.imread(img_orignal, cv2.IMREAD_GRAYSCALE)
    imagen_ecualizada = cv2.equalizeHist(imagen_original)

    # Carga la imagen para crear la máscara
    imagen = cv2.imread(img_orignal, cv2.IMREAD_GRAYSCALE)  # imagen de la que se crea la máscara

    # Define el número de veces que quieres aplicar el filtro mínimo
    num_repeticiones = 15

    # Aplica el filtro mínimo repetidamente
    for _ in range(num_repeticiones):
        imagen = cv2.erode(imagen, np.ones((3, 3), np.uint8))

    # Umbraliza la imagen
    umbral = 30  # Puedes ajustar este valor según tus necesidades
    imagen_umbralizada = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)[1]

    # cv2.imshow('nc', imagen_original)

    # Aplica la máscara a la imagen a color
    imagen_resultante = cv2.bitwise_and(imagen_ecualizada, imagen_ecualizada, mask=imagen_umbralizada)

    # Guarda la imagen resultante
    cv2.imwrite('imagen_resultante.jpg', imagen_resultante)

    # Muestra la imagen original, la imagen umbralizada y la imagen resultante
    # cv2.imshow('Imagen Original', imagen_original)
    # cv2.imshow('Imagen Umbralizada', imagen_umbralizada)
    # cv2.imshow('Imagen Resultante', imagen_resultante)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return imagen_umbralizada

def ajustar_gamma(image, gamma):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(256)]).astype("uint8")

    return cv2.LUT(image, table)


def segmentacion(ruta, rutaOriginal):
    image = Image.open(ruta)

    imgGrises = image.convert('L')
    np_image = np.array(imgGrises)
    np_image = ajustar_gamma(np_image, 0.1)
    np_image = ajustar_gamma(np_image, 0.1)

    # plt.imshow(np_image, cmap='gray')
    # plt.title(f'Imagen con Gamma {2.0}')
    # plt.axis('off')
    # plt.show()

    # Crear la máscara binaria para el top % más brillante
    umbral = np.percentile(np_image, 98)
    mascara = np_image > umbral

    # Identificar los componentes conectados
    labeled_array, num_features = ndimage.label(mascara)

    # Crear una máscara que será True para los componentes que deseamos mantener
    mask = np.ones_like(labeled_array, dtype=bool)

    # Iterar sobre cada componente conectado
    for label_num in range(1, num_features + 1):
        # Encontrar la posición de los píxeles que pertenecen a este componente
        positions = np.argwhere(labeled_array == label_num)
        
        # Revisar si alguno de los píxeles está en el borde
        touching_border = np.any(positions[:, 0] == 0) or \
                        np.any(positions[:, 1] == 0) or \
                        np.any(positions[:, 0] == labeled_array.shape[0] - 1) or \
                        np.any(positions[:, 1] == labeled_array.shape[1] - 1)
        
        # Si el componente está tocando el borde, se excluye de la máscara
        if touching_border:
            mask[labeled_array == label_num] = False

    # Aplicar la máscara para obtener la imagen final
    final_image = mascara & mask

    # Convertir la máscara binaria a una imagen PIL y guardarla
    result_image = Image.fromarray((final_image * 255).astype(np.uint8))
    result_image.save('imagen_umbralizada.png')

    # Mostrar la imagen resultante
    # plt.imshow(final_image, cmap='gray')
    # plt.axis('off')
    # plt.show()


    # Cargar las imágenes
    imagen1 = Image.open(rutaOriginal).convert("RGB")
    imagen2 = Image.open("imagen_umbralizada.png").convert("RGB")

    pixeles2 = imagen2.load()
    for i in range(imagen2.size[0]):
        for j in range(imagen2.size[1]):
            if pixeles2[i, j] == (255, 255, 255):   # Blanco
                pixeles2[i, j] = (255, 0, 0)        # Rojo

    if imagen1.size != imagen2.size:
        imagen2 = imagen2.resize(imagen1.size)

    # Aplicar la operación OR
    pixeles1 = imagen1.load()
    pixeles2 = imagen2.load()

    for i in range(imagen1.size[0]):
        for j in range(imagen1.size[1]):
            if pixeles2[i, j] == (255, 0, 0):
                pixeles1[i, j] = (255, 0, 0)
            

    # Guardarla imagen resultante
    imagen1.save("imagenSegmentada.jpg")

    return 'imagen_umbralizada.png'


def area_y_perimetro(image_path):
    image = Image.open(image_path)
    imgBn = image.convert('1')

    imgArr = np.array(imgBn)

    # Inverso de la imagen
    imagenInvertida = np.invert(imgArr)
    contornos, _ = cv2.findContours(imagenInvertida.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Suma de las regiones de interes
    area = np.sum(imagenInvertida)

    # Calculo del perimetro calculando la logitud de cada contorno
    perimetro = sum(cv2.arcLength(cnt, True) for cnt in contornos)

    imagen_contorno = np.zeros(imagenInvertida.shape, dtype=np.uint8)
    cv2.drawContours(imagen_contorno, contornos, -1, 255, 1)

    imgContorno = Image.fromarray(imagen_contorno)
    ruta_contorno = image_path.replace('.png', '_contornos.png')
    imgContorno.save(ruta_contorno)

    return area, perimetro, ruta_contorno

def main():
    parser = argparse.ArgumentParser(description='Procesar una imagen.')
    parser.add_argument('ruta', type=str, help='La ruta a la imagen que se procesará')
    args = parser.parse_args()
    ruta = args.ruta
    original = cv2.imread(ruta)

    img_umbralizada = preProcesamiento(ruta)
    mascara_segmentacion = segmentacion('imagen_resultante.jpg', ruta)
    area, perimetro, ruta_contorno = area_y_perimetro('imagen_umbralizada.png')
    img_segmentada = 'imagenSegmentada.jpg'

    areas = mpimg.imread(mascara_segmentacion)
    perimetros = mpimg.imread(ruta_contorno)
    img_segmentada = mpimg.imread('imagenSegmentada.jpg')
    original = mpimg.imread(ruta)

    w, h = areas.shape[:2]
    area = w * h - area

    plt.figure(figsize=(10, 10))

    # Mostrar las imágenes
    plt.subplot(2, 2, 1)
    plt.imshow(areas, cmap = 'gray')
    plt.axis('off')
    plt.title('Áreas')

    plt.subplot(2, 2, 2)
    plt.imshow(perimetros, cmap = 'gray')
    plt.axis('off')
    plt.title('Perímetros')

    plt.subplot(2, 2, 3)
    plt.imshow(original)
    plt.axis('off')
    plt.title('Original')

    plt.subplot(2, 2, 4)
    plt.imshow(img_segmentada)
    plt.axis('off')
    plt.title('Segmentada')

    plt.figtext(0.5, 0.04, f'Área: {int(area)} px, Perímetro: {int(perimetro)} px', ha="center", fontsize=12, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.title("Sementacion de Calcificaciones")

    plt.show()




main()