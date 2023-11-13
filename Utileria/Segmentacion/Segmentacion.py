from skimage import io
import numpy as np
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt

# Cargar la imagen
image_path = 'enfermo.jpg'
image = Image.open(image_path)

# Convertir a escala de grises
gray_image = image.convert('L')

# Convertir la imagen PIL a un array de numpy
np_image = np.array(gray_image)

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
result_image.save('imagen_resultado.png')

# Mostrar la imagen resultante
plt.imshow(final_image, cmap='gray')
plt.axis('off')
plt.show()
