#include <stdio.h>
#include <assert.h>

int bitcount(int x) {
    int count = 0;
    while (x > 0) {
      if (x & 0x01) {
        count += 1;
      }
      x = x >> 1;
    }
    printf("%d\n", count);
    return count;
}

int main() {
  assert(bitcount(0) == 0);
  assert(bitcount(1) == 1);
  assert(bitcount(8) == 1);
  assert(bitcount(3) == 2);
  assert(bitcount(0xffffffff) == 32);
}
