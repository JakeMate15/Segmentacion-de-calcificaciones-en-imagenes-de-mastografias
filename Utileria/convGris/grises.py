from PIL import Image

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

# Uso del programa
imagen_path = "img1.gif"  # Cambiar por la ruta de tu imagen
salida_path = "gris1.gif"  # Ruta donde se guardará la imagen en escala de grises

convertir_a_gris(imagen_path, salida_path)
