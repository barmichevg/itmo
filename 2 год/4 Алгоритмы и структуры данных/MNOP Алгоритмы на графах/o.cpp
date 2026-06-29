#include <iostream>
#include <queue>
#include <vector>

using namespace std;

int main() {
  int n;
  int m;
  if (!(cin >> n >> m)) {
    return 0;
  }

  vector<vector<int>> g(n + 1);
  for (int i = 0; i < m; ++i) {
    int u;
    int v;
    if (cin >> u >> v) {
      g[u].push_back(v);
      g[v].push_back(u);
    }
  }

  vector<int> color(n + 1, -1);

  for (int start = 1; start <= n; ++start) {
    if (color[start] == -1) {
      queue<int> q;
      color[start] = 0;
      q.push(start);

      while (!q.empty()) {
        int v = q.front();
        q.pop();

        for (int to : g[v]) {
          if (color[to] == -1) {
            color[to] = 1 - color[v];
            q.push(to);
          } else {
            if (color[to] == color[v]) {
              cout << "NO" << endl;
              return 0;
            }
          }
        }
      }
    }
  }

  cout << "YES" << endl;
  return 0;
}