//
// Test read from file directly
//
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  char *path = "./test.txt";
  char *line = NULL;
  size_t len = 0;
  FILE *fp = fopen(path, "r");

  size_t res = getline(&line, &len, fp);
//  size_t res = getline(&line, NULL, fp);

  printf("res=%ld, line=`%s`\n", res, line);
}
