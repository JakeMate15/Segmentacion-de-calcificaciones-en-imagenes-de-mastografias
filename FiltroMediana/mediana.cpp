#include<bits/stdc++.h>

using namespace std;

int dx[] = {1, 0, -1, 0}, dy[] = {0, 1, 0, -1};
vector<int> d = {1, -1}, d2 = {1, -1};

int main() {
    int n, m;
    cin >> m >> n;

    int a[n][m], res[n][m];
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> a[i][j];
            //cout << a[i][j] << " ";

            if(i == 0 || i == n - 1 || j == 0 || j == m - 1) {
                res[i][j] = a[i][j];
            }
        }
        //cout << "\n";
    }

    for(int i = 1; i < n - 1; i++) {
        for(int j = 1; j < m - 1; j++) {
            //cout << a[i][j] << "\n";
            vector<int> aux = {a[i][j]};
            for(int k = 0; k < 4; k++) 
                aux.push_back(a[i + dx[k]][j + dy[k]]);
            
            for(int dir: d)
                for(int dir2: d2)
                    aux.push_back(a[i + dir][j + dir2]);

            sort(aux.begin(), aux.end());

            res[i][j] = aux[4];
        }
    }


    cout << n << " " << m << "\n";
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cout << res[i][j] << " ";

        }
        cout << "\n";
    }

    return 0;
}