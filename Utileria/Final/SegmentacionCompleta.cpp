#include<bits/stdc++.h>

using namespace std;

int n, m;
vector<vector<int>> img, resultado;
vector<vector<bool>> visitados;
bool valido(int, int, int, int);
void dfs(int, int, bool, int, int);

int main() {
    cin >> n >> m;

    img.resize(n, vector<int>(m));
    resultado.resize(n, vector<int>(m));
    visitados.resize(n, vector<bool>(m));

    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> img[i][j];
            img[i][j] = img[i][j] >= 100 ? 255 : 0;
        }
    }

    for(int veces = 0; veces < 2; veces++) {
        for(int i = 0; i < n; i++) {
            dfs(i, veces * (n - 1), true, i, veces * (n - 1));
        }

        for(int j = 0; j < m; j++) {
            dfs(veces * (m - 1), j, true, veces * (m - 1), j);
        }
    }

    for(int i = 1; i < n - 1; i++) {
        for(int j = 1; j < m - 1; j++) {
            if(visitados[i][j])
                continue;
            
            dfs(i, j, false, i, j);
        }
    }

    cout << n << " " << m << "\n";

    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cout << resultado[i][j] << " ";
        }
        cout << "\n";
    }

    return 0;
}

bool valido(int i, int j, int iAnterior, int jAnterior) {
    return i >= 0 && i < n && j >= 0 && j < m && !visitados[i][j] && img[i][j] == img[iAnterior][jAnterior];
}

void dfs(int i, int j, bool borde, int iAnterior, int jAnterior) {
    //cerr << i << " " << j << " " << borde << " " << iAnterior << " " << jAnterior << "\n";
    if(!valido(i, j, iAnterior, jAnterior)){
        return;
    }
    //cerr << i << " " << j << " " << borde << " " << iAnterior << " " << jAnterior << "\n";
    
    visitados[i][j] = true;
    resultado[i][j] = borde ? 0 : 255;

    dfs(i, j + 1, borde, i, j);
    dfs(i + 1, j, borde, i, j);
    dfs(i, j - 1, borde, i, j);
    dfs(i - 1, j, borde, i, j);
}