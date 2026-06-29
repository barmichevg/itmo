#include <iostream>
#include <vector>

using namespace std;

int main() {
  int n, k;
  if (!(cin >> n >> k)) {
    return 0;
  }

  vector<int> numbers(n);
  for (int i = 0; i < n; ++i) {
    cin >> numbers[i];
  }

  vector<int> q_indices(n);
  int head = 0;
  int tail = 0;

  for (int i = 0; i < n; ++i) {
    if (head < tail && q_indices[head] <= i - k) {
      head++;
    }

    while (head < tail && numbers[q_indices[tail - 1]] >= numbers[i]) {
      tail--;
    }

    q_indices[tail] = i;
    tail++;

    if (i >= k - 1) {
      cout << numbers[q_indices[head]] << " ";
    }
  }

  return 0;
}