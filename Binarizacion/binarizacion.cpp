#include <iostream>
#include <vector>
#define UMBRAL 150
#define BLANCO 255
#define NEGRO   0

using namespace std;

vector<vector<int>> binarizacion(const vector<vector<int>>& imagen) {
    int n = imagen.size();
    int m = imagen[0].size();
    vector<vector<int>> imagenBinaria(n, vector<int>(m, 0));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            // Si el valor del pixel es mayor o igual al umbral, se convierte en blanco
            // de lo contrario, se convierte en negro
            imagenBinaria[i][j] = (imagen[i][j] >= UMBRAL) ? BLANCO : NEGRO;
        }
    }

    return imagenBinaria;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> imagen(n, vector<int>(m));

    // Leer la imagen en forma de matriz de grises
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> imagen[i][j];
        }
    }

    // Binarizar la imagen
    vector<vector<int>> imagenBinaria = binarizacion(imagen);

    // Imprimir la imagen binarizada
    for (const auto& fila : imagenBinaria) {
        for (int valor : fila) {
            cout << valor << " ";
        }
        cout << endl;
    }

    return 0;
}
