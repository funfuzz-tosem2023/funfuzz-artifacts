//
// Test aflpp-fun instrumentation
//
#include <stdio.h>

#define cCYA "\x1b[0;36m"
#define cRST "\x1b[0m"

#define FUN_FUNC_NUM  (2U << 12)
#define FUN_AREA_SIZE (FUN_FUNC_NUM * FUN_FUNC_NUM)

typedef unsigned int  u32;
typedef unsigned char u8;

FILE *logfile;

//extern u32 *__fun_area_ptr;

//static u32  __fun_area_init[FUN_AREA_SIZE];
//u32 *__fun_area_ptr = __fun_area_init;
//extern u8  *__afl_area_ptr;
//extern u8  *__afl_area_ptr_dummy;

static int cnt = 0;

void show() {

//  printf(cCYA "CALL_SHOW(%d)" cRST
//        "__fun_area_ptr-addr %p, __fun_area_ptr[0] %d, "
//         "__fun_area_ptr[10086] %d, FUN_FUNC_NUM %u\n",
//         ++cnt, __fun_area_ptr, __fun_area_ptr[0],
//         __fun_area_ptr[10086], FUN_FUNC_NUM);
  printf(cCYA "CALL_SHOW(%d)\n" cRST, ++cnt);

}

int main(void) {

  show();

//  __fun_area_ptr[10086] = 10086;
//  __afl_area_ptr[0] = 1;
//  __afl_area_ptr_dummy[0] = 1;

  show();
  show();
  show();

  // Print all
//  printf(cCYA "PRINT ALL: \n" cRST);
//  const int size = 3;
//  for (int i = 0 ; i <= size; ++i) {
//    for (int j = 0 ; j <= size; ++j) {
//      int idx = i * FUN_FUNC_NUM + j;
//      printf(cCYA "CALL_PRINTF " cRST
//                  "call_cnts[%d][%d]=__fun_area_ptr[%d]=%d\n",
//             i, j, idx, __fun_area_ptr[idx]);
//    }
//  }
//  printf("__afl_area_ptr %p\n", __afl_area_ptr);
//  printf("__afl_area_ptr_dummy %p\n", __afl_area_ptr_dummy);

  return 0;

}

