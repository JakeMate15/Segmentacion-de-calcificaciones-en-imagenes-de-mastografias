import cv2
import numpy as np
from sklearn.cluster import KMeans

# Cargar la imagen
image = cv2.imread('imagen_umbralizada_otsu.png')
# Convierte la imagen a un formato adecuado (por ejemplo, RGB)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Redimensiona la imagen si es necesario
# image = cv2.resize(image, (nuevo_ancho, nuevo_alto))

# Obtén las dimensiones de la imagen
height, width, _ = image.shape

# Aplanar la imagen para que sea una matriz de píxeles
pixels = image.reshape((-1, 3))

# Especifica el número de clústeres (tissue types) que deseas identificar
num_clusters = 2

# Aplica el algoritmo K-means
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(pixels)

# Obtiene las etiquetas de cluster para cada píxel
cluster_labels = kmeans.labels_

# Reconstruye la imagen segmentada a partir de las etiquetas
segmented_image = cluster_labels.reshape(height, width)

# Puedes visualizar la imagen segmentada
import matplotlib.pyplot as plt

plt.imshow(segmented_image, cmap='viridis')  # cmap es el mapa de colores
plt.axis('off')
plt.show()