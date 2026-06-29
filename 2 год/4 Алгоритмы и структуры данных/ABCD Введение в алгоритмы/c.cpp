#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

int main() {
  unordered_map<string, int> current_values;
  vector<pair<string, int>> history;

  string line;
  while (cin >> line) {
    if (line == "{") {
      history.push_back({"{", 0});
    } else if (line == "}") {
      while (!history.empty() && history.back().first != "{") {
        current_values[history.back().first] = history.back().second;
        history.pop_back();
      }
      if (!history.empty()) {
        history.pop_back();
      }
    } else {
      size_t pos = line.find('=');
      string var_left = line.substr(0, pos);
      string right = line.substr(pos + 1);

      int new_val;
      if (isdigit(right[0]) || right[0] == '-') {
        new_val = stoi(right);
      } else {
        new_val = current_values[right];
        cout << new_val << "\n";
      }

      history.push_back({var_left, current_values[var_left]});
      current_values[var_left] = new_val;
    }
  }

  return 0;
}
