#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Uso: $0 <nombreArchivo.jpg>"
    exit 1
fi
nombreArchivo="$1"
python3 escalaGris.py "$nombreArchivo" gris.jpg


g++ ecualizacionUniforme.cpp -o ecualizacionUniforme.exe
./ecualizacionUniforme.exe < gris1.txt > ecualizacion.txt
python3 generaImagen.py ecualizacion.txt imagenEcualizada.jpg

g++ filtroMediana.cpp -o filtroMediana.exe
./filtroMediana.exe < ecualizacion.txt > filtroMediana.txt
python3 generaImagen.py filtroMediana.txt imagenConFiltro.jpg

g++ deteccionDeBordes.cpp -o deteccionDeBordes.exe
python3 prewitt.py 

g++ binarizacion.cpp -o binarizacion.exe
python3 otus.py

g++ SegmentacionCompleta.cpp -o segmentacionCompleta.exe
python3 obtenMat.py
./segmentacionCompleta.exe < sal.txt > res.txt
python3 genIm.py

python3 combinacion.py

