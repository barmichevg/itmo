#include <cctype>
#include <iostream>
#include <stack>
#include <string>
#include <vector>

using namespace std;

struct Element {
  char type;
  int id;
};

bool IsPair(char a, char b) {
  if (tolower(a) != tolower(b)) {
    return false;
  }
  return a != b;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  string s;
  if (!(cin >> s)) {
    return 0;
  }

  int n = s.length() / 2;
  vector<int> result(n + 1);
  stack<Element> st;

  int animal_count = 0;
  int trap_count = 0;

  for (char c : s) {
    int current_id;
    bool is_animal = (c >= 'a' && c <= 'z');

    if (is_animal) {
      current_id = ++animal_count;
    } else {
      current_id = ++trap_count;
    }

    if (!st.empty() && IsPair(st.top().type, c)) {
      if (is_animal) {
        result[st.top().id] = current_id;
      } else {
        result[current_id] = st.top().id;
      }
      st.pop();
    } else {
      st.push({c, current_id});
    }
  }

  if (st.empty()) {
    cout << "Possible" << endl;
    for (int i = 1; i <= n; ++i) {
      cout << result[i] << (i == n ? "" : " ");
    }
    cout << endl;
  } else {
    cout << "Impossible" << endl;
  }

  return 0;
}
