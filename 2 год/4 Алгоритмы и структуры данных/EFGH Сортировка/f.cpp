#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

bool IsBetter(const string& a, const string& b) {
  return a + b > b + a;
}

void Merge(vector<string>& arr, int left, int mid, int right) {
  int n1 = mid - left + 1;
  int n2 = right - mid;
  vector<string> L(n1);
  vector<string> R(n2);

  for (int i = 0; i < n1; i++) {
    L[i] = arr[left + i];
  }
  for (int j = 0; j < n2; j++) {
    R[j] = arr[mid + 1 + j];
  }

  int i = 0;
  int j = 0;
  int k = left;
  while (i < n1 && j < n2) {
    if (IsBetter(L[i], R[j])) {
      arr[k++] = L[i++];
    } else {
      arr[k++] = R[j++];
    }
  }
  while (i < n1) {
    arr[k++] = L[i++];
  }
  while (j < n2) {
    arr[k++] = R[j++];
  }
}

void MergeSort(vector<string>& arr, int left, int right) {
  if (left < right) {
    int mid = left + (right - left) / 2;
    MergeSort(arr, left, mid);
    MergeSort(arr, mid + 1, right);
    Merge(arr, left, mid, right);
  }
}

int main() {
  vector<string> parts;
  string s;
  while (cin >> s) {
    parts.push_back(s);
  }

  if (!parts.empty()) {
    MergeSort(parts, 0, static_cast<int>(parts.size()) - 1);
  }

  for (const string& part : parts) {
    cout << part;
  }
  cout << endl;

  return 0;
}