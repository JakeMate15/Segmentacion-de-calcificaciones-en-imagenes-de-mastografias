from PIL import Image

# Primera matriz
matriz_1 = [
    [27, 15, 27, 1, 3, 1, 1, 7, 3, 1, 5],
    [15, 27, 3, 27, 23, 3, 3, 32, 23, 3, 3],
    [5, 27, 3, 1, 32, 23, 1, 7, 32, 23, 1],
    [15, 27, 1, 1, 7, 23, 23, 32, 7, 23, 1],
    [27, 5, 5, 23, 32, 32, 32, 46, 32, 32, 15],
    [27, 1, 15, 23, 46, 9, 46, 46, 46, 9, 15],
    [27, 15, 1, 32, 46, 46, 46, 46, 46, 46, 15],
    [27, 27, 3, 5, 46, 5, 46, 32, 46, 5, 5],
    [5, 1, 1, 23, 32, 32, 32, 46, 32, 32, 9],
    [27, 5, 23, 23, 46, 1, 9, 46, 46, 9, 9],
    [27, 1, 1, 32, 46, 46, 5, 9, 46, 46, 9],
    [27, 1, 3, 5, 46, 5, 5, 5, 46, 9, 9]
]

# Segunda matriz
matriz_2 = [
    [1, 2, 1, 85, 224, 255, 239, 208, 224, 225, 3],
    [2, 1, 8, 1, 200, 254, 35, 210, 200, 254, 35],
    [4, 1, 8, 11, 210, 200, 135, 208, 210, 200, 25],
    [2, 1, 7, 147, 208, 200, 200, 210, 208, 200, 20],
    [1, 3, 3, 200, 210, 210, 210, 226, 210, 210, 2],
    [1, 33, 2, 200, 226, 23, 226, 226, 226, 23, 2],
    [1, 2, 19, 210, 226, 226, 226, 226, 226, 226, 2],
    [1, 1, 125, 220, 226, 104, 226, 210, 226, 104, 9],
    [4, 6, 130, 200, 210, 210, 210, 226, 210, 210, 0],
    [1, 4, 200, 200, 226, 123, 23, 226, 226, 23, 0],
    [1, 12, 190, 210, 226, 226, 220, 23, 226, 226, 0],
    [1, 18, 125, 220, 226, 104, 9, 9, 226, 0, 0]
]

def generar_imagen(matriz, nombre_archivo):
    max_valor = max([max(fila) for fila in matriz])
    matriz_normalizada = [[int((pixel / max_valor) * 255) for pixel in fila] for fila in matriz]

    imagen = Image.new("L", (len(matriz[0]), len(matriz)))

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            imagen.putpixel((j, i), matriz_normalizada[i][j])

    imagen.save(nombre_archivo)

# Generar la primera imagen
generar_imagen(matriz_1, "matriz_1.png")

# Generar la segunda imagen
generar_imagen(matriz_2, "matriz_2.png")
