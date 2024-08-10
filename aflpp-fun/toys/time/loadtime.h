#ifndef AFLPP_FUN_LOADTIME_H
#define AFLPP_FUN_LOADTIME_H

typedef unsigned long long u64;
typedef unsigned int       u32;

#define LEN_1D        (1 << 13)
#define LEN_2D        (LEN_1D * LEN_1D)
#define SIZE_2D_U64   (LEN_2D * sizeof(u64))

u64 get_cur_time_us(void);

#endif  // AFLPP_FUN_LOADTIME_H
