/*
   american fuzzy lop++ - shared memory related header
   ---------------------------------------------------

   Originally written by Michal Zalewski

   Forkserver design by Jann Horn <jannhorn@googlemail.com>

   Now maintained by Marc Heuse <mh@mh-sec.de>,
                     Heiko Eißfeldt <heiko.eissfeldt@hexco.de>,
                     Andrea Fioraldi <andreafioraldi@gmail.com>,
                     Dominik Maier <mail@dmnk.co>

   Copyright 2016, 2017 Google Inc. All rights reserved.
   Copyright 2019-2022 AFLplusplus Project. All rights reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

     https://www.apache.org/licenses/LICENSE-2.0

   Shared code to handle the shared memory. This is used by the fuzzer
   as well the other components like afl-tmin, afl-showmap, etc...

 */

#ifndef __AFL_SHAREDMEM_H
#define __AFL_SHAREDMEM_H

#include "types.h"

// Type of bits shm. Note that here the struct name (sharedmem) and
// type name (sharedmem_t) are different.
typedef struct sharedmem {

  // extern unsigned char *trace_bits;

#ifdef USEMMAP
  /* ================ Proteas ================ */
  int  g_shm_fd;
  char g_shm_file_path[L_tmpnam];
  int  cmplog_g_shm_fd;
  char cmplog_g_shm_file_path[L_tmpnam];
/* ========================================= */
#else
  s32 shm_id;                           /* ID of the SHM region */
  s32 cmplog_shm_id;
#endif

  u8 *map;                              /* shared memory region */

  size_t map_size;                      /* actual allocated size */

  int             cmplog_mode;
  int             shmemfuzz_mode;
  struct cmp_map *cmp_map;

  // @FUN

  int fun_mode;     /* Whether using fun mode */

  // CC SHMs

  // TODO: to remove, does not work
  s32   cc_hot_id_shm_id;
  s32  *cc_hot_id_map;

  // SHM built by mmap to pass the id currently hot cc_shm
  u8   *cc_hot_id_mmap;

  u32   cc_map_size;
  s32   cc_shm_id[SHM_IDX];
  u64  *cc_map[SHM_IDX];

  // FS SHM

  u32     fs_map_size;
  s32     fs_shm_id[SHM_IDX];
  double *fs_map[SHM_IDX];

} sharedmem_t;

u8  *afl_shm_init(sharedmem_t *, size_t, unsigned char non_instrumented_mode);
void afl_shm_deinit(sharedmem_t *);

// @FUN

s32    *fun_cc_hot_id_shm_init(sharedmem_t *);
u64    *fun_cc_shm_init(sharedmem_t *, size_t, u8);
double *fun_fs_shm_init(sharedmem_t *, size_t, u8);
void    fun_cc_shm_activate(sharedmem_t *, u8);
void    fun_activate_cc_shm(sharedmem_t *, u8);
void    fun_shm_deinit(sharedmem_t *);

#endif

