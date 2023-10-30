from PIL import Image

def generar_imagen_desde_txt(entrada_path, salida_path):
    with open(entrada_path, "r") as archivo:
        # Leer las dimensiones de la imagen
        n, m = map(int, archivo.readline().strip().split())

        # Leer la matriz de niveles de gris
        matriz_gris = []
        for _ in range(n):
            fila = list(map(int, archivo.readline().strip().split()))
            matriz_gris.extend(fila)

        # Crear una imagen a partir de la matriz de niveles de gris
        imagen = Image.new("L", (m, n))  # intercambio de m y n
        imagen.putdata(matriz_gris)

        # Guardar la imagen
        imagen.save(salida_path)

# Uso del programa
entrada_path = "sal.txt"  # Cambiar por la ruta de tu archivo de texto
salida_path = "resultado.jpg"  # Ruta donde se guardará la imagen generada

generar_imagen_desde_txt(entrada_path, salida_path)
