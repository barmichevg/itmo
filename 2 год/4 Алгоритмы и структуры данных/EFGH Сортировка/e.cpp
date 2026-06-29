#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

bool CanPlace(int dist, int k, const vector<int>& stalls) {
  int count = 1;
  int last_pos = stalls[0];

  for (size_t i = 1; i < stalls.size(); ++i) {
    if (stalls[i] - last_pos >= dist) {
      count++;
      last_pos = stalls[i];
    }
  }
  return count >= k;
}

int main() {
  int n;
  int k;
  if (!(cin >> n >> k)) {
    return 0;
  }

  vector<int> stalls(n);
  for (int i = 0; i < n; ++i) {
    cin >> stalls[i];
  }

  int left = 0;
  int right = stalls[n - 1] - stalls[0];
  int result = 0;

  while (left <= right) {
    int mid = left + (right - left) / 2;
    if (CanPlace(mid, k, stalls)) {
      result = mid;
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  cout << result << endl;

  return 0;
}