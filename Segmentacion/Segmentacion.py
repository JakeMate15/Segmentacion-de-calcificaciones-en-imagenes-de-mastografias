import argparse
from skimage import io
from skimage.exposure import equalize_hist
import numpy as np
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt

# Cargar la imagen
parser = argparse.ArgumentParser(description='Procesar una imagen.')
parser.add_argument('image_path', type=str, help='La ruta a la imagen que se procesará')
args = parser.parse_args()
image_path = args.image_path
image = Image.open(image_path)

# Convertir a escala de grises
imgGrises = image.convert('L')

# Ecualizar la imagen
imgGrises = equalize_hist(np.array(imgGrises))
imgGrises = Image.fromarray((imgGrises * 255).astype(np.uint8))
imgGrises.save('imgEcualizada.jpg')

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
plt.imshow(final_image, cmap='gray')
plt.axis('off')
plt.show()


# Cargar las imágenes
imagen1 = Image.open(image_path).convert("RGB")
imagen2 = Image.open("imagen_umbralizada.png").convert("RGB")

pixeles2 = imagen2.load()
for i in range(imagen2.size[0]):
    for j in range(imagen2.size[1]):
        if pixeles2[i, j] == (255, 255, 255):  # Blanco
            pixeles2[i, j] = (255, 0, 0)  # Rojo

if imagen1.size != imagen2.size:
    imagen2 = imagen2.resize(imagen1.size)

# Aplicar la operación OR
pixeles1 = imagen1.load()
pixeles2 = imagen2.load()

for i in range(imagen1.size[0]):
    for j in range(imagen1.size[1]):
        r = pixeles1[i, j][0] | pixeles2[i, j][0]
        g = pixeles1[i, j][1] | pixeles2[i, j][1]
        b = pixeles1[i, j][2] | pixeles2[i, j][2]
        pixeles1[i, j] = (r, g, b)

# Guardar o mostrar la imagen resultante
imagen1.save("imagenSegmentada.jpg")