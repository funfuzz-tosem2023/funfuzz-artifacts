//
// Read a file by line
//
#include <stdlib.h>
#include <stdio.h>

int main(void) {

  char *fn = "./staticFS";

  FILE * fp;
  char * line = NULL;
  size_t len = 0;
  ssize_t read;
  int cnt = 0;

  fp = fopen(fn, "r");
  if (fp == NULL)
    exit(EXIT_FAILURE);

//  while ((read = getline(&line, &len, fp)) != -1) {
//    printf("Retrieved line of length %zu:\n", read);
//    printf("%s", line);
//    printf("as double: %lf\n", strtod(line, NULL));
//  }

  while (getline(&line, &len, fp) != -1) {

    printf("cnt=%d, line=%s", ++cnt, line);
    printf("as double: %lf\n", strtod(line, NULL));

  }
  printf("cnt_final=%d\n", cnt);

  fclose(fp);
  if (line)
    free(line);
  exit(EXIT_SUCCESS);

}
