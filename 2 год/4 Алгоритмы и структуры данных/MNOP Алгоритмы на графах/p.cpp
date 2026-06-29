#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

bool can_reach_all(int capacity, const vector<vector<int>>& fuel, bool reverse_mode) {
  int n = static_cast<int>(fuel.size());
  if (n <= 1) {
    return true;
  }

  vector<int> q(n);
  vector<bool> visited(n, false);

  int head = 0;
  int tail = 0;
  q[tail++] = 0;
  visited[0] = true;

  while (head < tail) {
    int current = q[head++];

    for (int neighbor = 0; neighbor < n; ++neighbor) {
      if (visited[neighbor]) {
        continue;
      }

      int cost = reverse_mode ? fuel[neighbor][current] : fuel[current][neighbor];
      if (cost <= capacity) {
        visited[neighbor] = true;
        q[tail++] = neighbor;
      }
    }
  }

  return tail == n;
}

int main() {
  ifstream input_file("avia.in");
  ofstream output_file("avia.out");

  int city_count;
  if (!(input_file >> city_count)) {
    return 0;
  }

  if (city_count <= 1) {
    output_file << 0 << '\n';
    return 0;
  }

  vector<vector<int>> fuel(city_count, vector<int>(city_count));
  for (int i = 0; i < city_count; ++i) {
    for (int j = 0; j < city_count; ++j) {
      input_file >> fuel[i][j];
    }
  }

  int left = 0;
  int right = 1000000000;
  int answer = right;

  while (left <= right) {
    int mid = left + (right - left) / 2;

    if (can_reach_all(mid, fuel, false) && can_reach_all(mid, fuel, true)) {
      answer = mid;
      right = mid - 1;
    } else {
      left = mid + 1;
    }
  }

  output_file << answer << '\n';
  return 0;
}