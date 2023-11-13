from PIL import Image
import argparse

def convertir_a_gris(imagen_path, salida_path):
    # Abrir la imagen
    imagen = Image.open(imagen_path)
    
    # Convertir a escala de grises
    imagen_gris = imagen.convert('L')
    
    # Obtener las dimensiones de la imagen
    n, m = imagen_gris.size
    
    # Guardar la imagen en escala de grises
    imagen_gris.save(salida_path)
    
    # Obtener los valores de los píxeles en escala de grises
    pixeles = list(imagen_gris.getdata())
    
    # Crear el archivo de texto
    with open("gris1.txt", "w") as archivo:
        # Escribir las dimensiones
        archivo.write(f"{n} {m}\n")
        
        # Escribir la matriz de píxeles
        for i in range(0, n*m, n):
            fila = pixeles[i:i+n]
            archivo.write(" ".join(map(str, fila)) + "\n")

def main():
    # Configurar el análisis de argumentos
    parser = argparse.ArgumentParser(description='Convierte una imagen a escala de grises.')
    parser.add_argument('imagen_path', help='Ruta de la imagen de entrada')
    parser.add_argument('salida_path', help='Ruta de la imagen de salida en escala de grises')

    args = parser.parse_args()

    # Llama a la función de conversión a escala de grises con los argumentos proporcionados
    convertir_a_gris(args.imagen_path, args.salida_path)

if __name__ == "__main__":
    main()