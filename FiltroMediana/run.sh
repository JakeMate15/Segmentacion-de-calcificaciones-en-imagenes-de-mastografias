""" 
    Script en bash para conectar el script en python con la salida generada con 
    el programa en C++, la salida, es pues, un archivo de texto que se dirige al
    script genImg.py, donde se procesa el archivo de texto para llevarla a una imagen
"""

python3 grises.py
g++ mediana.cpp
./a.out < gris1.txt > sal.txt
python3 genImg.py