import cv2
import numpy as np
import argparse
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageFilter
import math

coord_x = None
coord_y = None
valoresArea = None
valoresPerimetro = None
areaComponente = None
perimetroComponente = None


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

    # Aplica la máscara a la imagen a color
    imagen_resultante = cv2.bitwise_and(imagen_ecualizada, imagen_ecualizada, mask=imagen_umbralizada)

    # Guarda la imagen resultante
    cv2.imwrite('imagen_resultante.jpg', imagen_resultante)

    return imagen_umbralizada

def ajustar_gamma(image, gamma):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(256)]).astype("uint8")

    return cv2.LUT(image, table)

def topBrillante(arr, porcentaje):
    arrOrdenado = np.sort(arr)[::-1]
    porcentaje = porcentaje / 10.0
    numElementos = math.ceil(len(arrOrdenado) * porcentaje)
    topPixel = arrOrdenado[:numElementos]

    return topPixel

def segmentacion(ruta, rutaOriginal):
    image = Image.open(ruta)

    imgGrises = image.convert('L')
    np_image = np.array(imgGrises)
    np_image = ajustar_gamma(np_image, 0.1)
    np_image = ajustar_gamma(np_image, 0.1)

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
        tocandoBorde = np.any(positions[:, 0] == 0) or \
                        np.any(positions[:, 1] == 0) or \
                        np.any(positions[:, 0] == labeled_array.shape[0] - 1) or \
                        np.any(positions[:, 1] == labeled_array.shape[1] - 1)
        
        # Si el componente está tocando el borde, se excluye de la máscara
        if tocandoBorde:
            mask[labeled_array == label_num] = False

    # Aplicar la máscara para obtener la imagen final
    final_image = mascara & mask

    # Convertir la máscara binaria a una imagen PIL y guardarla
    result_image = Image.fromarray((final_image * 255).astype(np.uint8))
    for _ in range(4):
        result_image = result_image.filter(ImageFilter.MedianFilter(size=3))
    
    result_image.save('imagen_umbralizada.png')

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

def etiquetar_objetos(matriz):
    etiqueta = 0
    etiquetas = {}
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 1:
                vecinos = obtener_vecinos(etiquetas, i, j)
                if not vecinos:
                    etiqueta += 1
                    etiquetas[(i, j)] = etiqueta
                else:
                    etiqueta_min = min(vecinos)
                    etiquetas[(i, j)] = etiqueta_min
                    actualizar_etiquetas(etiquetas, vecinos, etiqueta_min)
    return etiquetas

def obtener_vecinos(etiquetas, i, j):
    vecinos = []
    for di, dj in [(-1, 0), (0, -1), (-1, -1), (1, -1)]:
        if (i + di, j + dj) in etiquetas:
            vecinos.append(etiquetas[(i + di, j + dj)])
    return vecinos

def actualizar_etiquetas(etiquetas, vecinos, nueva_etiqueta):
    for posicion in etiquetas:
        if etiquetas[posicion] in vecinos:
            etiquetas[posicion] = nueva_etiqueta

def calcular_area_perimetro(etiquetas, matriz):
    areas = {}
    perimetros = {}
    for posicion, etiqueta in etiquetas.items():
        i, j = posicion
        if etiqueta not in areas:
            areas[etiqueta] = 0
        if etiqueta not in perimetros:
            perimetros[etiqueta] = 0
        areas[etiqueta] += 1
        perimetros[etiqueta] += contar_bordes(matriz, i, j)

    return areas, perimetros

def contar_bordes(matriz, i, j):
    bordes = 0
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= i + di < len(matriz) and 0 <= j + dj < len(matriz[0]):
            if matriz[i + di][j + dj] == 0:
                bordes += 1
        else:
            bordes += 1
    return bordes

def cal_area_y_perimetro(rutaImagen):
    image = Image.open(rutaImagen)
    imgBn = image.convert('1')  # Convertir a imagen binaria (blanco y negro)

    imgArr = np.array(imgBn)  # Convertir a matriz numpy

    # Invertir la imagen: en PIL, '1' es blanco y '0' es negro
    matriz_binaria = imgArr.astype(int)  # Convertir a matriz binaria de 0 y 1

    etiquetas = etiquetar_objetos(matriz_binaria)
    areas, perimetros = calcular_area_perimetro(etiquetas, matriz_binaria)

    matriz_areas = [[0 for _ in range(len(matriz_binaria[0]))] for _ in range(len(matriz_binaria))]
    matriz_perimetros = [[0 for _ in range(len(matriz_binaria[0]))] for _ in range(len(matriz_binaria))]

    for (i, j), etiqueta in etiquetas.items():
        matriz_areas[i][j] = areas[etiqueta]
        matriz_perimetros[i][j] = perimetros[etiqueta]

    # Calculando el número total de componentes
    numero_componentes = len(areas)

    # Calculando la suma total del área y el perímetro
    suma_area_total = sum(areas.values())
    suma_perimetro_total = sum(perimetros.values())

    return matriz_areas, matriz_perimetros, numero_componentes, suma_area_total, suma_perimetro_total




def deteccionBordes(rutaImagen):
    # Cargar la imagen y convertirla a escala de grises
    image = Image.open(rutaImagen)
    img_gray = image.convert('L')
    img_array = np.array(img_gray)

    # Aplicar el filtro Laplaciano
    img_laplacian = cv2.Laplacian(img_array, cv2.CV_64F)

    # Normalizar y convertir a uint8
    img_laplacian = np.clip(img_laplacian, 0, 255)
    img_laplacian = np.absolute(img_laplacian)  # Obtener el valor absoluto para asegurar que todos los valores sean positivos
    img_laplacian = np.uint8(img_laplacian)

    # Binarizar la imagen
    _, img_bin = cv2.threshold(img_laplacian, 50, 255, cv2.THRESH_BINARY)

    # Guardar la imagen resultante
    img_contorno = Image.fromarray(img_bin)
    ruta_contorno = rutaImagen.replace('.png', '_contornos_laplacian.png')
    img_contorno.save(ruta_contorno)

    return ruta_contorno

def on_move(event):
    global coord_x, coord_y, texto_area_perimetro
    # Asegúrate de que el movimiento sea dentro de un eje
    if event.inaxes is not None:
        coord_x, coord_y = event.xdata, event.ydata

        # Asegúrate de que las coordenadas estén dentro del rango
        if 0 <= int(coord_y) < len(valoresArea) and 0 <= int(coord_x) < len(valoresArea[0]):
            areaComponente = valoresArea[int(coord_y)][int(coord_x)]
            perimetroComponente = valoresPerimetro[int(coord_y)][int(coord_x)]

            # Actualiza el texto con los nuevos valores
            texto_area_perimetro.set_text(f'Área: {areaComponente} px, Perímetro: {perimetroComponente} px')
            plt.draw()  # Actualiza la figura

def main():
    parser = argparse.ArgumentParser(description='Procesar una imagen.')
    parser.add_argument('ruta', type=str, help='La ruta a la imagen que se procesará')
    args = parser.parse_args()
    ruta = args.ruta
    original = cv2.imread(ruta)

    preProcesamiento(ruta)
    mascara_segmentacion = segmentacion('imagen_resultante.jpg', ruta)
    ruta_contorno = deteccionBordes('imagen_umbralizada.png')

    global valoresArea, valoresPerimetro, areaComponente, perimetroComponente
    valoresArea, valoresPerimetro, numeroComponentes, suma_area_total, suma_perimetro_total = cal_area_y_perimetro('imagen_umbralizada.png')
    img_segmentada = 'imagenSegmentada.jpg'

    areas = mpimg.imread(mascara_segmentacion)
    perimetros = mpimg.imread(ruta_contorno)
    img_segmentada = mpimg.imread('imagenSegmentada.jpg')
    original = mpimg.imread(ruta)

    plt.figure(figsize=(12, 12))

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

    infoGeneral = f'Número de Componentes: {numeroComponentes}\n' \
                    f'Área Total: {suma_area_total} px\n' \
                    f'Perímetro Total: {suma_perimetro_total} px'
    plt.figtext(0.5, 0.92, infoGeneral, ha="center", fontsize=12, 
                bbox={"facecolor":"orange", "alpha":0.5, "pad":5})


    global texto_area_perimetro
    texto_area_perimetro = plt.figtext(0.5, 0.04, 'Área: 0 px, Perímetro: 0 px', ha="center", fontsize=12, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    fig = plt.gcf()  # Obtiene la figura actual
    cid = fig.canvas.mpl_connect('motion_notify_event', on_move)

    plt.show()



main()