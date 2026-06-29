#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

struct CarState {
  int next_pos;
  int id;

  bool operator<(const CarState& other) const {
    return next_pos < other.next_pos;
  }
};

int main() {
  int n, k, p;
  if (!(cin >> n >> k >> p)) {
    return 0;
  }

  vector<int> history(p);
  vector<vector<int>> future_indices(n + 1);

  for (int i = 0; i < p; ++i) {
    cin >> history[i];
    future_indices[history[i]].push_back(i);
  }

  for (int i = 1; i <= n; ++i) {
    future_indices[i].push_back(1000001);
    reverse(future_indices[i].begin(), future_indices[i].end());
  }

  vector<bool> active(n + 1, false);
  priority_queue<CarState> heap;
  int ans = 0;
  int floor_count = 0;

  for (int i = 0; i < p; ++i) {
    int current_car = history[i];

    future_indices[current_car].pop_back();
    int next_time = future_indices[current_car].back();

    if (active[current_car]) {
      heap.push({next_time, current_car});
      continue;
    }

    ans++;
    if (floor_count < k) {
      floor_count++;
    } else {
      while (!heap.empty()) {
        CarState top = heap.top();
        heap.pop();

        if (active[top.id] && future_indices[top.id].back() == top.next_pos) {
          active[top.id] = false;
          break;
        }
      }
    }

    active[current_car] = true;
    heap.push({next_time, current_car});
  }

  cout << ans << endl;

  return 0;
}