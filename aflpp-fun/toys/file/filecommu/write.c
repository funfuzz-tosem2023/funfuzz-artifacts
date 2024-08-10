//
// Test can we write one line?
//
#include <stdlib.h>
#include <stdio.h>

int main(void) {

  char *path = "./test.txt";
  FILE *fp = fopen(path, "w");


  for (int i = 100 ; i >= 0; --i) {
    char num_str[100];
    sprintf(num_str, "%d\n", i);
    fputs(num_str, fp);
    rewind(fp);
  }

  fclose(fp);

}