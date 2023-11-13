#include<bits/stdc++.h>
using namespace std;

// Definición de los núcleos (kernels) Prewitt para la detección de bordes.
int horizontalPrewitt[3][3] = {
    {-1, 0, 1},
    {-1, 0, 1},
    {-1, 0, 1}
};

int verticalPrewitt[3][3] = {
    {1, 1, 1},
    {0, 0, 0},
    {-1, -1, -1}
};

// Función para aplicar el operador Prewitt a una imagen dada.
vector<vector<int>> operadorPrewitt(const vector<vector<int>>& entrada, const int kernel[3][3]) {
    int n = entrada.size();
    int m = entrada[0].size();
    vector<vector<int>> salida(n, vector<int>(m, 0));

    for (int i = 1; i < n - 1; i++) {
        for (int j = 1; j < m - 1; j++) {
            int sum = 0;
            for(int k = -1; k < 2; k++) {
                for(int l = -1; l < 2; l++) {
                    sum += (entrada[i + k][j + l] * kernel[1 + k][l + 1]);
                }
            }
            salida[i][j] = sum;
        }
    }

    return salida;
}

// Función para calcular el gradiente de una imagen a partir de gradientes horizontales y verticales.
vector<vector<int>> calculategradiente(const vector<vector<int>>& horizontal, const vector<vector<int>>& vertical) {
    int n = horizontal.size();
    int m = horizontal[0].size();
    vector<vector<int>> gradiente(n, vector<int>(m, 0));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            gradiente[i][j] = sqrt(horizontal[i][j] * horizontal[i][j] + vertical[i][j] * vertical[i][j]);
        }
    }

    return gradiente;
}

int main() {
    int n, m;
    cin >> n >> m;

    // Lectura de la imagen de entrada.
    vector<vector<int>> imagen(n, vector<int>(m));
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> imagen[i][j];
        }
    }

    // Aplicar los operadores Prewitt para calcular gradientes horizontales y verticales.
    vector<vector<int>> horizontal = operadorPrewitt(imagen, horizontalPrewitt);
    vector<vector<int>> vertical = operadorPrewitt(imagen, verticalPrewitt);

    // Calcular el gradiente a partir de gradientes horizontales y verticales.
    vector<vector<int>> gradiente = calculategradiente(horizontal, vertical);

    // Imprimir resultados.
    cout << "horizontal\n";
    for(auto x: horizontal) {
        for(auto y: x) {
            cout << y << "\t";
        }
        cout << "\n";
    }
    cout << "\n\n";

    cout << "vertical\n";
    for(auto x: vertical) {
        for(auto y: x) {
            cout << y << "\t";
        }
        cout << "\n";
    }
    cout << "\n\n";

    cout << n << " " << m << "\n";
    for (const auto& x : gradiente) {
        for (int y : x) {
            cout << y << "\t";
        }
        cout << endl;
    }

    return 0;
}
