//
// Change string to number
//
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

char *trim(char *str)
{
  char *end;

  // Trim leading space
  while(isspace((unsigned char)*str)) str++;

  if(*str == 0)  // All spaces?
    return str;

  // Trim trailing space
  end = str + strlen(str) - 1;
  while(end > str && isspace((unsigned char)*end)) end--;

  // Write new null terminator character
  end[1] = '\0';

  return str;
}

int main(void) {

  char str[100];

  while (1) {

    fgets(str, 100, stdin);

    char *trim_str = trim(str);

    printf("trim_str=%s\n", trim_str);

    long num = strtol(trim_str, NULL, 10);
    printf("num=%ld\n", num);

  }

}
