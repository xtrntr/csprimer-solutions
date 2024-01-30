#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


bool ispangram(char *s) {
  int letters[26] = {0};
  int length = strlen(s);
  for (int i = 0; i < length; i++) {
    char ch = tolower(s[i]);
    int index = ch - 'a';
    letters[index]++;
  }

  for (int i = 0; i < 26; i++) {
    if (letters[i] == 0) {
      return false;
    }
  }

  return true;
}

int main() {
  size_t len;
  ssize_t read;
  char *line = NULL;
  while ((read = getline(&line, &len, stdin)) != -1) {
    if (ispangram(line))
      printf("%s", line);
  }

  if (ferror(stdin))
    fprintf(stderr, "Error reading from stdin");

  free(line);
  fprintf(stderr, "ok\n");
}
