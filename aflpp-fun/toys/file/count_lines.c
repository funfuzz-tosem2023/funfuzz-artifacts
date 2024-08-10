//
// Count lines of a file
//
#include <stdlib.h>
#include <stdio.h>



int main(void) {

  char *fpath = "./funcInfo";

  // Declarations.

  FILE  *fp;
  int   lcnt = 0;   /* Counter for lines */


  // Open file and count lines. Each line is info for a function
  // in format <funName>, <funcID>, e.g, "main,123".

  fp = fopen(fpath, "r");

  // Sanitize
  if (fp == NULL) {
    printf("Cannot open funcInfo file `%s`!\n", fpath);
    return -1;
  }

  // Increment count if this character is newline
  for (char c = (char) getc(fp); c != EOF; c = (char) getc(fp))
    if (c == '\n') lcnt = lcnt + 1;

  printf("lcnt=%d\n", lcnt);

  fclose(fp);

  return 0;

}
