#include <deque>
#include <iostream>

using namespace std;

struct GoblinQueue {
  deque<int> head;
  deque<int> tail;

  void balance() {
    if (head.size() < tail.size()) {
      head.push_back(tail.front());
      tail.pop_front();
    } else if (head.size() > tail.size() + 1) {
      tail.push_front(head.back());
      head.pop_back();
    }
  }

  void push_end(int id) {
    tail.push_back(id);
    balance();
  }

  void push_mid(int id) {
    tail.push_front(id);
    balance();
  }

  int pop_first() {
    int res = head.front();
    head.pop_front();
    balance();
    return res;
  }
};

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n;
  if (!(cin >> n)) {
    return 0;
  }

  GoblinQueue q;

  for (int i = 0; i < n; ++i) {
    char op;
    cin >> op;

    if (op == '-') {
      cout << q.pop_first() << "\n";
    } else {
      int id;
      cin >> id;
      if (op == '+') {
        q.push_end(id);
      } else {
        q.push_mid(id);
      }
    }
  }

  return 0;
}