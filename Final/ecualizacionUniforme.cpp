#include<bits/stdc++.h>
using namespace std;


vector<int> histogramaEqualization(const vector<int>& histograma, long long tamImg) {
    int grises = 255;

    vector<int> cdf(grises);

    // Calcula la función de distribución acumulada (CDF)
    cdf[0] = histograma[0];
    for (int i = 1; i < grises; ++i) {
        cdf[i] = cdf[i - 1] + histograma[i];
    }

    vector<int> ecualizacion(grises);

    // Aplica la ecualización de histogramaa
    for (int i = 0; i < grises; ++i) {
        ecualizacion[i] = round((long double)(cdf[i]) / tamImg * (grises - 1));
    }

    return ecualizacion;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout << fixed << setprecision(10);

    int n, m;
    cin >> n >> m;

    //Lectura de la imagen y cálculo de sus frecuencias
    int a[n][m];
    vector<int> histogramaa(256);
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> a[i][j];
            histogramaa[a[i][j]]++;
        }
        
    }

    vector<int> nvosValores = histogramaEqualization(histogramaa, n * m);
    

    cout << n << " " << m << "\n";
    int nuevaImg[n][m];
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            nuevaImg[i][j] = nvosValores[a[i][j]];
            cout << nuevaImg[i][j] << "\t";
        }
        cout << "\n";
    }

}