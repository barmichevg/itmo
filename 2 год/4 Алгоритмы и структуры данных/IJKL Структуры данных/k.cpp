#include <algorithm>
#include <iostream>
#include <random>
#include <vector>

using namespace std;

struct Node {
  long long l;
  long long r;
  long long mx;
  unsigned int priority;
  int left;
  int right;
};

Node pool[300005];
int node_ptr = 0;

int create_node(long long l, long long r, unsigned int priority) {
  node_ptr++;
  pool[node_ptr].l = l;
  pool[node_ptr].r = r;
  pool[node_ptr].mx = r - l + 1;
  pool[node_ptr].priority = priority;
  pool[node_ptr].left = 0;
  pool[node_ptr].right = 0;
  return node_ptr;
}

long long get_max_val(int t) {
  if (t == 0) {
    return 0;
  }
  return pool[t].mx;
}

void update(int t) {
  if (t == 0) {
    return;
  }
  long long current_len = pool[t].r - pool[t].l + 1;
  long long left_mx = get_max_val(pool[t].left);
  long long right_mx = get_max_val(pool[t].right);
  pool[t].mx = max({current_len, left_mx, right_mx});
}

void split(int t, long long key, int& a, int& b) {
  if (t == 0) {
    a = 0;
    b = 0;
    return;
  }
  if (pool[t].l < key) {
    split(pool[t].right, key, pool[t].right, b);
    a = t;
  } else {
    split(pool[t].left, key, a, pool[t].left);
    b = t;
  }
  update(t);
}

int merge(int a, int b) {
  if (a == 0) {
    return b;
  }
  if (b == 0) {
    return a;
  }
  if (pool[a].priority > pool[b].priority) {
    pool[a].right = merge(pool[a].right, b);
    update(a);
    return a;
  } else {
    pool[b].left = merge(a, pool[b].left);
    update(b);
    return b;
  }
}

int find_leftmost(int t, long long size) {
  if (t == 0 || pool[t].mx < size) {
    return 0;
  }
  if (pool[t].left != 0) {
    if (pool[pool[t].left].mx >= size) {
      return find_leftmost(pool[t].left, size);
    }
  }
  if (pool[t].r - pool[t].l + 1 >= size) {
    return t;
  }
  return find_leftmost(pool[t].right, size);
}

int main() {
  long long n;
  int m;
  if (!(cin >> n >> m)) {
    return 0;
  }

  mt19937 rng(1337);
  int root = create_node(1, n, rng());

  vector<long long> alloc_start(m + 1, -1);
  vector<long long> alloc_len(m + 1, 0);

  for (int i = 1; i <= m; ++i) {
    long long query;
    cin >> query;

    if (query > 0) {
      int block_id = find_leftmost(root, query);
      if (block_id == 0) {
        cout << "-1\n";
        alloc_start[i] = -1;
      } else {
        long long b_l = pool[block_id].l;
        long long b_r = pool[block_id].r;
        cout << b_l << "\n";
        alloc_start[i] = b_l;
        alloc_len[i] = query;

        int t1, t2, t3;
        split(root, b_l, t1, t2);
        split(t2, b_l + 1, t2, t3);
        root = merge(t1, t3);

        if (b_l + query <= b_r) {
          int remainder = create_node(b_l + query, b_r, rng());
          int l_part, r_part;
          split(root, b_l + query, l_part, r_part);
          root = merge(merge(l_part, remainder), r_part);
        }
      }
    } else {
      int target_id = (int)(-query);
      if (alloc_start[target_id] != -1) {
        long long l = alloc_start[target_id];
        long long r = l + alloc_len[target_id] - 1;

        int prv_id = 0;
        int curr = root;
        while (curr != 0) {
          if (pool[curr].l < l) {
            prv_id = curr;
            curr = pool[curr].right;
          } else {
            curr = pool[curr].left;
          }
        }
        if (prv_id != 0) {
          if (pool[prv_id].r + 1 == l) {
            l = pool[prv_id].l;
            int t1, t2, t3;
            split(root, pool[prv_id].l, t1, t2);
            split(t2, pool[prv_id].l + 1, t2, t3);
            root = merge(t1, t3);
          }
        }

        int nxt_id = 0;
        curr = root;
        while (curr != 0) {
          if (pool[curr].l > r) {
            nxt_id = curr;
            curr = pool[curr].left;
          } else {
            curr = pool[curr].right;
          }
        }
        if (nxt_id != 0) {
          if (r + 1 == pool[nxt_id].l) {
            r = pool[nxt_id].r;
            int t1, t2, t3;
            split(root, pool[nxt_id].l, t1, t2);
            split(t2, pool[nxt_id].l + 1, t2, t3);
            root = merge(t1, t3);
          }
        }

        int merged = create_node(l, r, rng());
        int l_part, r_part;
        split(root, l, l_part, r_part);
        root = merge(merge(l_part, merged), r_part);
        alloc_start[target_id] = -1;
      }
    }
  }

  return 0;
}