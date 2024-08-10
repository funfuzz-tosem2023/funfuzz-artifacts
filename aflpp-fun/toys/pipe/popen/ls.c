#include <stdio.h>

#define PATH_MAX 1024

int main(void) {

  FILE *fp;
  int status;
  char path[PATH_MAX];

  fp = popen("ls *", "r");
  if (fp == NULL)
    /* Handle error */;

  while (fgets(path, PATH_MAX, fp) != NULL)
    printf("%s", path);


  status = pclose(fp);
  if (status == -1) {

    /* Error reported by pclose() */
    perror("pclose() failed!");

  } else {

    /* Use macros described under wait() to inspect `status' in order
       to determine success/failure of command executed by popen() */
    printf("status=%d\n", status);

  }

}
