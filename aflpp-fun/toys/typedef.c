//
// Define a type
//
#include <stdio.h>
#include <stdlib.h>

typedef unsigned char u8;

typedef struct atype {

  u8 *c_str;
  u8  a_u8;

} atype;

typedef unsigned int u32;

int main() {

  atype *t = calloc(1, sizeof (atype));

  printf("t->c_str=%s, t->a_u8=%d(%c)\n", t->c_str, t->a_u8, t->a_u8);

  t->c_str = (u8 *) getenv("TYPE_STR");
  t->a_u8  = 123;

  printf("t->c_str=%s, t->a_u8=%d(%c)\n", t->c_str, t->a_u8, t->a_u8);
  printf("(u32)-1=%d\n", (u32)(-1));

  return 0;

}
