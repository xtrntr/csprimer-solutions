#include <stdio.h>
#include <stdlib.h>

struct Box {
  char* name;
  size_t* value;
};

int main() {
  size_t n = 5;
  struct Box b1 = { "foo", &n };

  printf("b1 pvalue: %p, b1 pvalue+1: %p\n", b1.value, b1.value + 1);
  printf("b1 pvalue: %zu\n", *b1.value);

  void* ptr = malloc(8);
  printf("ptr: %p\n", ptr);
  printf("ptr: %p\n", ptr + 8);


}
