#include <algorithm>
#include <deque>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
  string s;
  if (!(cin >> s)) {
    return 0;
  }

  vector<long long> weights(26);
  for (int i = 0; i < 26; ++i) {
    cin >> weights[i];
  }

  vector<int> freq(26, 0);
  for (char c : s) {
    freq[c - 'a']++;
  }

  vector<int> order(26);
  for (int i = 0; i < 26; ++i) {
    order[i] = i;
  }

  sort(order.begin(), order.end(), [&](int a, int b) {
    if (weights[a] != weights[b]) {
      return weights[a] > weights[b];
    }
    return a > b;
  });

  deque<char> edges;
  string middle = "";

  for (int i = 0; i < 26; ++i) {
    int idx = order[i];
    if (freq[idx] == 1) {
      middle += static_cast<char>(idx + 'a');
      freq[idx] = 0;
    }
  }

  for (int i = 25; i >= 0; --i) {
    int idx = order[i];
    if (freq[idx] >= 2) {
      edges.push_front(static_cast<char>(idx + 'a'));
      edges.push_back(static_cast<char>(idx + 'a'));
      for (int k = 0; k < freq[idx] - 2; ++k) {
        middle += static_cast<char>(idx + 'a');
      }
    }
  }

  int half = static_cast<int>(edges.size()) / 2;
  for (int i = 0; i < half; ++i) {
    cout << edges[i];
  }
  cout << middle;
  for (int i = half; i < static_cast<int>(edges.size()); ++i) {
    cout << edges[i];
  }
  cout << endl;

  return 0;
}