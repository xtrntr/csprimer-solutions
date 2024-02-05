#include <stdio.h>

void recurse(int n) {
  printf("Pointer address of n %p. Call #%d\n", &n, n);
  return recurse(n + 1);
}

int main() {
  recurse(0);
  return 0;
}
