import cv2
import numpy as np
import argparse
from skimage import io
from skimage.exposure import equalize_hist
from PIL import Image
from scipy import ndimage


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

def segmentacion(ruta, rutaOriginal):
    image = Image.open(ruta)

    # Convertir a escala de grises
    imgGrises = image.convert('L')

    # Convertir la imagen PIL a un array de numpy
    np_image = np.array(imgGrises)

    # Crear la máscara binaria para el top 10% más brillante
    p90_threshold = np.percentile(np_image, 90)
    binary_mask = np_image > p90_threshold

    # Identificar los componentes conectados
    labeled_array, num_features = ndimage.label(binary_mask)

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
    final_image = binary_mask & mask

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
    # Load the image and convert it to black and white
    image = Image.open(image_path)
    bw_image = image.convert('1')  # Convert to black-and-white (1 bit per pixel)

    # Convert image to a numpy array
    image_array = np.array(bw_image)

    # Invert the image to consider white as the object for contour detection
    inverted_image_array = np.invert(image_array)

    # Find the contours of the white objects
    contours, _ = cv2.findContours(inverted_image_array.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the area of the white regions
    area = np.sum(inverted_image_array)

    # Calculate the perimetro by summing the length of each contour
    perimetro = sum(cv2.arcLength(cnt, True) for cnt in contours)

    # Create a new black image to draw the contours
    imagen_contorno = np.zeros(inverted_image_array.shape, dtype=np.uint8)

    # Draw the contours on the new image
    cv2.drawContours(imagen_contorno, contours, -1, 255, 1)

    # Convert the new contour image to a PIL Image and save it with a new filename
    contour_pil_image = Image.fromarray(imagen_contorno)
    ruta_contorno = image_path.replace('.png', '_contours.png')
    contour_pil_image.save(ruta_contorno)

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

    areas = cv2.imread(mascara_segmentacion)
    perimetros = cv2.imread(ruta_contorno)

    img_segmentada = cv2.imread(img_segmentada)
    
    mediciones = np.hstack((areas, perimetros))
    resultados = np.hstack((original, img_segmentada))

    cv2.imshow('Resultados', resultados)
    cv2.imshow('Mediciones', mediciones)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





main()