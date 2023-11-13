from PIL import Image
import argparse

def generar_imagen_desde_txt(entrada_path, salida_path):
    with open(entrada_path, "r") as archivo:
        # Leer las dimensiones de la imagen
        m, n = map(int, archivo.readline().strip().split())

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

def main():
    # Configurar el análisis de argumentos
    parser = argparse.ArgumentParser(description='Genera una imagen a partir de un archivo de texto con niveles de gris.')
    parser.add_argument('entrada_path', help='Ruta del archivo de texto de entrada')
    parser.add_argument('salida_path', help='Ruta de la imagen de salida generada')

    args = parser.parse_args()

    # Llama a la función de generación de imagen con los argumentos proporcionados
    generar_imagen_desde_txt(args.entrada_path, args.salida_path)

if __name__ == "__main__":
    main()
