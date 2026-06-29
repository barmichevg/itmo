#include <iostream>
#include <vector>

using namespace std;

int main() {
  int n;
  if (!(cin >> n)) {
    return 0;
  }

  vector<int> a(n);
  for (int i = 0; i < n; ++i) {
    cin >> a[i];
  }

  if (n <= 2) {
    cout << 1 << " " << n << endl;
    return 0;
  }

  int best_l = 0;
  int best_r = 0;
  int max_len = 0;
  int current_l = 0;

  for (int r = 0; r < n; ++r) {
    if (r >= 2 && a[r] == a[r - 1] && a[r] == a[r - 2]) {
      current_l = r - 1;
    }

    int current_len = r - current_l + 1;
    if (current_len > max_len) {
      max_len = current_len;
      best_l = current_l;
      best_r = r;
    }
  }

  cout << best_l + 1 << " " << best_r + 1 << endl;

  return 0;
}
