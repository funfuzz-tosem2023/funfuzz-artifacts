//
// A toy program that builds non-optimized functions.
//

#include "stdlib.h"
#include "stdio.h"

int minus(int a, int b) {
  int res;
  if (a > 0)  res = a - b;
  else        res = -a - b;
  return res;
}

int add(int a, int b) {
  int res;
  if (a > 0)  res = a + b;
  else        res = -a + b;
  return res;
}

int main(int argc, char **argv) {

  printf("argc=%d\n", argc);

  if (argc != 3) return 1;

  int a = atoi(argv[1]);
  int b = atoi(argv[2]);

  // What if not preserve the return value?
  int val;
  if (a > 0)  val = atoi("123");
  else        val = atoi("345");
  printf("%d", val);


  printf("a=%d, b=%d\n", a, b);

  int c = minus(a, b);
  int d = add(a, b);

  printf("c=%d, d=%d\n", c, d);

  return 0;

}
