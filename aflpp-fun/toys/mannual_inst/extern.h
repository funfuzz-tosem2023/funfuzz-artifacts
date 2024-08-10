//
// Header for defining global.
//

#ifndef AFLPP_FUN_EXTERN_H
#define AFLPP_FUN_EXTERN_H

// 2D array
#define FUNC_NUM 4
#define TWP_D_SIZE (FUNC_NUM+1)*(FUNC_NUM+1) // 4*4

static int area[TWP_D_SIZE];

int *area_ptr = area;

#endif  // AFLPP_FUN_EXTERN_H
