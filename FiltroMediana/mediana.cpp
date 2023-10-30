#include<bits/stdc++.h>

using namespace std;

/// @brief Arreglos para definir el movimiento dentro del conjunto de datos

int dx[] = {1, 0, -1, 0}, dy[] = {0, 1, 0, -1};
vector<int> d = {1, -1}, d2 = {1, -1};

void mediana ();

int main() {
    mediana();
}

/// @brief Funcion que realiza el filtro
/// Función que realiza el filtro de mediana en una matriz.
void mediana (){
    // Definición del tamaño de la matriz m x n
    int n, m;
    cin >> m >> n;

    // Inicialización de las matrices, la matriz de entrada 'a' y la matriz de salida 'res'.
    int a[n][m], res[n][m];

    // Lectura de la matriz 'a' y copia de los bordes a la matriz 'res'.
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> a[i][j];
            
            // Si se esta en un borde de la matriz, copiamos el valor directamente.
            if(i == 0 || i == n - 1 || j == 0 || j == m - 1) {
                res[i][j] = a[i][j];
            }
        }
    }

    // Proceso para aplicar el filtro de mediana en la matriz.
    for(int i = 1; i < n - 1; i++) {
        for(int j = 1; j < m - 1; j++) {
            // Vector auxiliar que almacena los valore actuales que tiene 
            // la matriz 'a' en la iteracion actual
            vector<int> aux = {a[i][j]};

            // Agregar valores vecinos a la lista 'aux'.
            for(int k = 0; k < 4; k++) 
                aux.push_back(a[i + dx[k]][j + dy[k]]);
            
            for(int dir: d)
                for(int dir2: d2)
                    aux.push_back(a[i + dir][j + dir2]);

            // Ordenamos la lista 'aux' y tomamos el valor de la mediana.
            sort(aux.begin(), aux.end());
            res[i][j] = aux[4];
        }
    }

    // Mostrar el tamaño de la matriz resultante y su contenido.
    cout << n << " " << m << "\n";
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cout << res[i][j] << " ";
        }
        cout << "\n";
    }

}