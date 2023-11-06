import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

# Obtener la ruta actual
ruta_actual = os.getcwd()

# Crear una ventana principal
ventana = tk.Tk()
ventana.title("Segmentación de Imágenes")

# Función para abrir una imagen
def abrir_imagen():
    # Abre un cuadro de diálogo para seleccionar una imagen con la ruta actual
    ruta_imagen = filedialog.askopenfilename(initialdir=ruta_actual, filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ppm;*.pgm")])
    
    if ruta_imagen:
        # Abre la imagen con PIL (Python Imaging Library)
        imagen = Image.open(ruta_imagen)
        imagen.thumbnail((400, 400))  # Redimensiona la imagen a un tamaño máximo
        
        # Convierte la imagen de PIL a un formato Tkinter PhotoImage
        imagen_tk = ImageTk.PhotoImage(imagen)
        
        # Muestra la imagen en un widget de etiqueta
        etiqueta_imagen.config(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk

def grises():
    print('hoa')

# Botón para abrir una imagen
boton_abrir = tk.Button(ventana, text="Abrir Imagen", command=abrir_imagen)
boton_abrir.grid(row=0, column=0)

boton_gris = tk.Button(ventana, text="Grises", command=grises)
boton_gris.grid(row=0, column=1)

# Widget de etiqueta para mostrar la imagen
etiqueta_imagen = tk.Label(ventana)
etiqueta_imagen.grid(row=1, column=0, columnspan=2)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
