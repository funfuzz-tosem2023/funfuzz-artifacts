//
// A toy program with many functions.
//

#include <stdio.h>


void f1() {
  printf("f1()\n");
}

void f2() {
  printf("f2()\n");
  int a = 1;
  int b = 2;
  int c = a + b;
}

// Call f1, f2
void f3() {
  printf("f3()\n");
  f1();
  f2();
}

int main() {

  f3();

  return 0;

}
