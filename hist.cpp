#include<bits/stdc++.h>
using namespace std;

typedef long double ld;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);

    int n, m;
    cin >> n >> m;

    //Lectura de la imagen y cálculo de sus frecuencias
    int a[n][m];
    map<int, int> his;
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> a[i][j];
            his[a[i][j]]++;
            cout << a[i][j] << "\t";
        }
        cout << "\n";
    }

    cout << "\n\nHistograma original\n";

    //Impresión de las frecuencias de cada valor de gris
    for(auto [g, rep]: his) {
        cout << g << " " << rep << "\n";
    }

    cout << "\n";

    //Cálculo de la probabilidad de aparición de cada nivel de gris
    vector<ld> pg(256);
    for(int i = 0; i <= 255; i++) {
        pg[i] = (1.0) * his[i] / (n * m);
        //cout << "P(" << i << "): " << pg[i] << "\n";
    }

    cout << "\n";

    //Cálculo de gmax y gmin
    int gMin = ((*his.begin()).first), gMx = (*prev(his.end())).first;

    //Cálculo de los nuevos nivel de gris
    vector<int> nuevosValores(256);
    for(int i = 0; i <= 255; i++) {
        nuevosValores[i] = (gMx - gMin) * pg[i] + gMin;
        //cout << "nV(" << i << "): " << nuevosValores[i] << "\n";
    }

    int nvo = 0;
    map<int,int> nvoHist;
    //Reemplazar con los nuevos valores
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            a[i][j] = nuevosValores[a[i][j]];
            nvoHist[a[i][j]]++;
        }
    }

    cout << "Nueva imagen\n";

    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cout << a[i][j] << "\t";
        }
        cout << "\n";
    }

    cout << "Nuevo histograma\n";
    //Impresión de las frecuencias de cada valor de gris del nuevo
    //Histograma
    for(auto [g, rep]: nvoHist) {
        cout << g << " " << rep << "\n";
    }
}