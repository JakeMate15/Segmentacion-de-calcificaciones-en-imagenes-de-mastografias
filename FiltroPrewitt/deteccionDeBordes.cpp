#include<bits/stdc++.h>
using namespace std;

int horizontalPrewitt[3][3] = {
    {-1, -1, -1},
    {0, 0, 0},
    {1, 1, 1}
};

int verticalPrewitt[3][3] = {
    {-1, 0, 1},
    {-1, 0, 1},
    {-1, 0, 1}
};

vector<vector<int>> operadorPrewitt(const vector<vector<int>>& entrada, const int kernel[3][3]) {
    int n = entrada.size();
    int m = entrada[0].size();
    vector<vector<int>> output(n, vector<int>(m, 0));

    for (int i = 1; i < n - 1; i++) {
        for (int j = 1; j < m - 1; j++) {
            int sum = 0;
            for (int x = -1; x <= 1; x++) {
                for (int y = -1; y <= 1; y++) {
                    sum += entrada[i + x][j + y] * kernel[x + 1][y + 1];
                }
            }
            output[i][j] = sum;
        }
    }

    return output;
}

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


    vector<vector<int>> imagen(n, vector<int>(m));
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> imagen[i][j];
        }
    }

    vector<vector<int>> horizontal = operadorPrewitt(imagen, horizontalPrewitt);
    vector<vector<int>> vertical = operadorPrewitt(imagen, verticalPrewitt);
    vector<vector<int>> gradiente = calculategradiente(horizontal, vertical);

    cout << n << " " << m << "\n";
    for (const auto& x : gradiente) {
        for (int y : x) {
            cout << y << "\t";
        }
        cout << endl;
    }

    return 0;
}