#include <iostream>

using namespace std;

int main() {
  long long a, b, c, d, k;
  if (!(cin >> a >> b >> c >> d >> k)) {
    return 0;
  }

  long long current = a;

  for (long long i = 1; i <= k; ++i) {
    long long next_val = current * b - c;

    if (next_val <= 0) {
      current = 0;
      break;
    }

    if (next_val > d) {
      next_val = d;
    }

    if (next_val == current) {
      break;
    }

    current = next_val;
  }

  cout << current << endl;

  return 0;
}
