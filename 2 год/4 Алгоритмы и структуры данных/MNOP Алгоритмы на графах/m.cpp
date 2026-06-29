#include <algorithm>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

using namespace std;

const int INF = 1e9;

struct NodeState {
  int cost = INF;
  int parent_r = -1;
  int parent_c = -1;
  char step_char = ' ';
};

struct Position {
  int r, c, dist;

  bool operator>(const Position& other) const {
    return dist > other.dist;
  }
};

int main() {
  int n, m, sx, sy, tx, ty;
  cin >> n >> m >> sx >> sy >> tx >> ty;
  --sx;
  --sy;
  --tx;
  --ty;

  vector<string> grid(n);
  for (int i = 0; i < n; ++i) {
    cin >> grid[i];
  }

  vector<vector<NodeState>> state(n, vector<NodeState>(m));
  priority_queue<Position, vector<Position>, greater<Position>> pq;

  int dr[4] = {-1, 1, 0, 0};
  int dc[4] = {0, 0, -1, 1};
  char dir[4] = {'N', 'S', 'W', 'E'};

  state[sx][sy].cost = 0;
  pq.push({sx, sy, 0});

  while (!pq.empty()) {
    Position cur = pq.top();
    pq.pop();

    if (cur.dist != state[cur.r][cur.c].cost) {
      continue;
    }

    if (cur.r == tx && cur.c == ty) {
      break;
    }

    for (int k = 0; k < 4; ++k) {
      int nr = cur.r + dr[k];
      int nc = cur.c + dc[k];

      if (nr < 0 || nr >= n || nc < 0 || nc >= m || grid[nr][nc] == '#') {
        continue;
      }

      int w = (grid[nr][nc] == '.') ? 1 : 2;
      int nd = cur.dist + w;

      if (nd < state[nr][nc].cost) {
        state[nr][nc].cost = nd;
        state[nr][nc].parent_r = cur.r;
        state[nr][nc].parent_c = cur.c;
        state[nr][nc].step_char = dir[k];
        pq.push({nr, nc, nd});
      }
    }
  }

  if (state[tx][ty].cost == INF) {
    cout << -1 << '\n';
    return 0;
  }

  cout << state[tx][ty].cost << '\n';

  string path;
  int r = tx, c = ty;
  while (r != sx || c != sy) {
    path.push_back(state[r][c].step_char);
    int pr = state[r][c].parent_r;
    int pc = state[r][c].parent_c;
    r = pr;
    c = pc;
  }

  reverse(path.begin(), path.end());
  cout << path << '\n';

  return 0;
}