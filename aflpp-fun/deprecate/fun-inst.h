////
//// Fun macros and global variables. Include this in "afl-compiler-rt.o.c"
//// can make all dereferences to the runtime variable `__fun_area_ptr` work.
//
//// See also the implementation of AFL bitmap, i.e.,
//// 1. `__afl_area_ptr` in "instrumentation/afl-compiler-rt.o.c"
//// 2. `AFLMapPtr`, `MapPtr`, etc, in "instrumentation/SanitizerCoveragePCGUARD.so.cc"
////
//
//#include "types.h"
//#include "config.h"
//#include "debug.h"
//
//#ifndef AFLPP_FUN_INST_H
//#define AFLPP_FUN_INST_H
//
///// Declarations
//
//static u32  __fun_area_init[FUN_AREA_SIZE];
//static u32  *__fun_area_ptr_dummy = __fun_area_init;
//
//// Runtime ptr
//u32 *__fun_area_ptr = __fun_area_init;
//
//// Already initialized flags
//u32 __fun_already_initialized_shm;
//
//// Lots of variables
//u32 __fun_map_size = FUN_AREA_SIZE;
//u64 __fun_map_addr;
//
//// Declarations
//static void __fun_map_shm(void);
//static void __fun_unmap_shm(void);
//
//
//#endif  // AFLPP_FUN_AFL_FUN_H
