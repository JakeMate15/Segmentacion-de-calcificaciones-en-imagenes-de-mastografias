from PIL import Image

# Lee el archivo y obtén los valores de n, m y la matriz de datos
with open('res.txt', 'r') as archivo:
    n, m = map(int, archivo.readline().split())
    matriz = []
    for linea in archivo:
        fila = list(map(int, linea.split()))
        matriz.append(fila)

# Convierte la matriz en una imagen binaria
imagen_binaria = Image.new('1', (m, n))  # '1' indica que estamos creando una imagen binaria (blanco y negro)

for i in range(n):
    for j in range(m):
        pixel_value = matriz[i][j]
        if pixel_value == 255:
            imagen_binaria.putpixel((j, i), 255)  # Establece el píxel como blanco
        else:
            imagen_binaria.putpixel((j, i), 0)  # Establece el píxel como negro

# Guarda la imagen binaria en un archivo
imagen_binaria.save('imagen_binaria.png')
