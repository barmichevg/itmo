#include <iostream>
#include <numeric>
#include <vector>

using namespace std;

struct DisjointSetUnion {
  vector<int> parent;
  int cycles;

  DisjointSetUnion(int n) {
    parent.resize(n + 1);
    for (int i = 0; i <= n; ++i) {
      parent[i] = i;
    }
    cycles = 0;
  }

  int find_set(int i) {
    if (parent[i] == i) {
      return i;
    }
    parent[i] = find_set(parent[i]);
    return parent[i];
  }

  void unite_sets(int i, int j) {
    int root_i = find_set(i);
    int root_j = find_set(j);

    if (root_i != root_j) {
      parent[root_i] = root_j;
    } else {
      cycles++;
    }
  }
};

int main() {
  int n;
  if (!(cin >> n)) {
    return 0;
  }

  DisjointSetUnion dsu(n);

  for (int i = 1; i <= n; ++i) {
    int key_location;
    if (cin >> key_location) {
      dsu.unite_sets(i, key_location);
    }
  }

  cout << dsu.cycles << endl;

  return 0;
}