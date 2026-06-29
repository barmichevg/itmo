#include <iostream>
#include <vector>

using namespace std;

int main() {
  int n;
  int k;
  if (!(cin >> n >> k)) {
    return 0;
  }

  const int MaxPrice = 10000;
  vector<int> freq(MaxPrice + 1, 0);
  long long total_sum = 0;

  for (int i = 0; i < n; ++i) {
    int price;
    cin >> price;
    freq[price]++;
    total_sum += price;
  }

  long long discount = 0;
  int position = 0;

  for (int price = MaxPrice; price >= 1; --price) {
    int count = freq[price];
    while (count > 0) {
      position++;
      if (position % k == 0) {
        discount += price;
      }
      count--;
    }
  }

  cout << total_sum - discount << endl;

  return 0;
}