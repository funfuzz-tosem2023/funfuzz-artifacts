/*
   american fuzzy lop++ - shared memory related code
   -------------------------------------------------

   Originally written by Michal Zalewski

   Forkserver design by Jann Horn <jannhorn@googlemail.com>

   Now maintained by Marc Heuse <mh@mh-sec.de>,
                        Heiko Eißfeldt <heiko.eissfeldt@hexco.de> and
                        Andrea Fioraldi <andreafioraldi@gmail.com>

   Copyright 2016, 2017 Google Inc. All rights reserved.
   Copyright 2019-2022 AFLplusplus Project. All rights reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

     https://www.apache.org/licenses/LICENSE-2.0

   Shared code to handle the shared memory. This is used by the fuzzer
   as well the other components like afl-tmin, afl-showmap, etc...

 */

#define AFL_MAIN

#ifdef __ANDROID__
  #include "android-ashmem.h"
#endif
#include "config.h"
#include "types.h"
#include "debug.h"
#include "alloc-inl.h"
#include "hash.h"
#include "sharedmem.h"
#include "cmplog.h"
#include "list.h"

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <signal.h>
#include <dirent.h>
#include <fcntl.h>

#include <sys/wait.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/resource.h>
#include <sys/mman.h>

#ifndef USEMMAP
  #include <sys/ipc.h>
  #include <sys/shm.h>
#endif

static list_t shm_list = {.element_prealloc_count = 0};


/* Get rid of shared memory. */

void afl_shm_deinit(sharedmem_t *shm) {

  // AFL logics
  if (shm == NULL) { return; }
  list_remove(&shm_list, shm);
  if (shm->shmemfuzz_mode) {

    unsetenv(SHM_FUZZ_ENV_VAR);

  } else {

    unsetenv(SHM_ENV_VAR);

  }

#ifdef USEMMAP
  if (shm->map != NULL) {

    munmap(shm->map, shm->map_size);
    shm->map = NULL;

  }

  if (shm->g_shm_fd != -1) {

    close(shm->g_shm_fd);
    shm->g_shm_fd = -1;

  }

  if (shm->g_shm_file_path[0]) {

    shm_unlink(shm->g_shm_file_path);
    shm->g_shm_file_path[0] = 0;

  }

  if (shm->cmplog_mode) {

    unsetenv(CMPLOG_SHM_ENV_VAR);

    if (shm->cmp_map != NULL) {

      munmap(shm->cmp_map, shm->map_size);
      shm->cmp_map = NULL;

    }

    if (shm->cmplog_g_shm_fd != -1) {

      close(shm->cmplog_g_shm_fd);
      shm->cmplog_g_shm_fd = -1;

    }

    if (shm->cmplog_g_shm_file_path[0]) {

      shm_unlink(shm->cmplog_g_shm_file_path);
      shm->cmplog_g_shm_file_path[0] = 0;

    }

  }

#else
  shmctl(shm->shm_id, IPC_RMID, NULL);
  if (shm->cmplog_mode) { shmctl(shm->cmplog_shm_id, IPC_RMID, NULL); }
#endif

  shm->map = NULL;

}

/* Configure shared memory.
   Returns a pointer to shm->map for ease of use.
*/

u8 *afl_shm_init(sharedmem_t *shm, size_t map_size,
                 unsigned char non_instrumented_mode) {

  shm->map_size = 0;

  shm->map = NULL;
  shm->cmp_map = NULL;

#ifdef USEMMAP

  shm->g_shm_fd = -1;
  shm->cmplog_g_shm_fd = -1;

  const int shmflags = O_RDWR | O_EXCL;

  /* ======
  generate random file name for multi instance

  thanks to f*cking glibc we can not use tmpnam securely, it generates a
  security warning that cannot be suppressed
  so we do this worse workaround */
  snprintf(shm->g_shm_file_path, L_tmpnam, "/afl_%d_%ld", getpid(), random());

  #ifdef SHM_LARGEPAGE_ALLOC_DEFAULT
  /* trying to get large memory segment optimised and monitorable separately as
   * such */
  static size_t sizes[4] = {(size_t)-1};
  static int    psizes = 0;
  int           i;
  if (sizes[0] == (size_t)-1) { psizes = getpagesizes(sizes, 4); }

  /* very unlikely to fail even if the arch supports only two sizes */
  if (likely(psizes > 0)) {

    for (i = psizes - 1; shm->g_shm_fd == -1 && i >= 0; --i) {

      if (sizes[i] == 0 || map_size % sizes[i]) { continue; }

      shm->g_shm_fd =
          shm_create_largepage(shm->g_shm_file_path, shmflags, i,
                               SHM_LARGEPAGE_ALLOC_DEFAULT, DEFAULT_PERMISSION);

    }

  }

  #endif

  /* create the shared memory segment as if it was a file */
  if (shm->g_shm_fd == -1) {

    shm->g_shm_fd =
        shm_open(shm->g_shm_file_path, shmflags | O_CREAT, DEFAULT_PERMISSION);

  }

  if (shm->g_shm_fd == -1) { PFATAL("shm_open() failed"); }

  /* configure the size of the shared memory segment */
  if (ftruncate(shm->g_shm_fd, map_size)) {

    PFATAL("setup_shm(): ftruncate() failed");

  }

  /* map the shared memory segment to the address space of the process */
  shm->map =
      mmap(0, map_size, PROT_READ | PROT_WRITE, MAP_SHARED, shm->g_shm_fd, 0);
  if (shm->map == MAP_FAILED) {

    close(shm->g_shm_fd);
    shm->g_shm_fd = -1;
    shm_unlink(shm->g_shm_file_path);
    shm->g_shm_file_path[0] = 0;
    PFATAL("mmap() failed");

  }

  /* If somebody is asking us to fuzz instrumented binaries in non-instrumented
     mode, we don't want them to detect instrumentation, since we won't be
     sending fork server commands. This should be replaced with better
     auto-detection later on, perhaps? */

  if (!non_instrumented_mode) setenv(SHM_ENV_VAR, shm->g_shm_file_path, 1);

  if (shm->map == (void *)-1 || !shm->map) PFATAL("mmap() failed");

  if (shm->cmplog_mode) {

    snprintf(shm->cmplog_g_shm_file_path, L_tmpnam, "/afl_cmplog_%d_%ld",
             getpid(), random());

    /* create the shared memory segment as if it was a file */
    shm->cmplog_g_shm_fd =
        shm_open(shm->cmplog_g_shm_file_path, O_CREAT | O_RDWR | O_EXCL,
                 DEFAULT_PERMISSION);
    if (shm->cmplog_g_shm_fd == -1) { PFATAL("shm_open() failed"); }

    /* configure the size of the shared memory segment */
    if (ftruncate(shm->cmplog_g_shm_fd, map_size)) {

      PFATAL("setup_shm(): cmplog ftruncate() failed");

    }

    /* map the shared memory segment to the address space of the process */
    shm->cmp_map = mmap(0, map_size, PROT_READ | PROT_WRITE, MAP_SHARED,
                        shm->cmplog_g_shm_fd, 0);
    if (shm->cmp_map == MAP_FAILED) {

      close(shm->cmplog_g_shm_fd);
      shm->cmplog_g_shm_fd = -1;
      shm_unlink(shm->cmplog_g_shm_file_path);
      shm->cmplog_g_shm_file_path[0] = 0;
      PFATAL("mmap() failed");

    }

    /* If somebody is asking us to fuzz instrumented binaries in
       non-instrumented mode, we don't want them to detect instrumentation,
       since we won't be sending fork server commands. This should be replaced
       with better auto-detection later on, perhaps? */

    if (!non_instrumented_mode)
      setenv(CMPLOG_SHM_ENV_VAR, shm->cmplog_g_shm_file_path, 1);

    if (shm->cmp_map == (void *)-1 || !shm->cmp_map)
      PFATAL("cmplog mmap() failed");

  }

#else
  u8 *shm_str;

  // for qemu+unicorn we have to increase by 8 to account for potential
  // compcov map overwrite
  // int shmget(key_t private|public, size_t size_of_shmem, int mode_bits);
  shm->shm_id =
      shmget(IPC_PRIVATE, map_size == MAP_SIZE ? map_size + 8 : map_size,
             IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION);
  if (shm->shm_id < 0) {

    PFATAL("shmget() failed, try running afl-system-config");

  }

  if (shm->cmplog_mode) {

    shm->cmplog_shm_id = shmget(IPC_PRIVATE, sizeof(struct cmp_map),
                                IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION);

    if (shm->cmplog_shm_id < 0) {

      shmctl(shm->shm_id, IPC_RMID, NULL);  // do not leak shmem
      PFATAL("shmget() failed, try running afl-system-config");

    }

  }

  if (!non_instrumented_mode) {

    shm_str = alloc_printf("%d", shm->shm_id);

    /* If somebody is asking us to fuzz instrumented binaries in
       non-instrumented mode, we don't want them to detect instrumentation,
       since we won't be sending fork server commands. This should be replaced
       with better auto-detection later on, perhaps? */

    setenv(SHM_ENV_VAR, shm_str, 1);

    ck_free(shm_str);

  }

  if (shm->cmplog_mode && !non_instrumented_mode) {

    shm_str = alloc_printf("%d", shm->cmplog_shm_id);

    setenv(CMPLOG_SHM_ENV_VAR, shm_str, 1);

    ck_free(shm_str);

  }

  // https://www.ibm.com/docs/en/zos/2.1.0?topic=functions-shmat-shared-memory-attach-operation
  // The shmat() function attaches the shared memory segment associated with the shared memory
  // identifier, shmid, to the address space of the calling process.
  shm->map = shmat(shm->shm_id, NULL, 0);
  FUN_LOG("afl_shm_init, after shmat, shm->cc_map %p, shm->map %p",
            shm->cc_map, shm->map);

  if (shm->map == (void *)-1 || !shm->map) {

    // shmctl() -- Perform Shared Memory Control Operations
    shmctl(shm->shm_id, IPC_RMID, NULL);  // do not leak shmem

    if (shm->cmplog_mode) {

      shmctl(shm->cmplog_shm_id, IPC_RMID, NULL);  // do not leak shmem

    }

    PFATAL("shmat() failed");

  }

  if (shm->cmplog_mode) {

    shm->cmp_map = shmat(shm->cmplog_shm_id, NULL, 0);

    if (shm->cmp_map == (void *)-1 || !shm->cmp_map) {

      shmctl(shm->shm_id, IPC_RMID, NULL);  // do not leak shmem

      shmctl(shm->cmplog_shm_id, IPC_RMID, NULL);  // do not leak shmem

      PFATAL("shmat() failed");

    }

  }

#endif

  shm->map_size = map_size;
  list_append(&shm_list, shm);

  return shm->map;

}

// @FUN

/// Prepare to SHMs for call counts monitoring
/// @param idx: index of cc_shm, can be 0 or 1
u64 *fun_cc_shm_init(sharedmem_t *shm, size_t size, u8 idx) {

  if (!shm->fun_mode) return NULL;

  // Debug
  FUN_LOG("fun_cc_shm_init(), idx=%d", idx);

  u32 map_size;

  // Sanitize and initialize
  if (shm->cc_map_size > 0) {

    if (shm->cc_map_size != size) {

      PFATAL("@FUN, Unequal map_size, cc_map_size %u, size %lu",
             shm->cc_map_size, size);

    } else {

      map_size = shm->cc_map_size;

    }

  } else {

    shm->cc_map_size = 0;
    map_size = size;

  }

  // Initialize map ptr
  shm->cc_map[idx] = NULL;

  // shmget
  shm->cc_shm_id[idx] =
      shmget(IPC_PRIVATE, map_size, IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION);

  if (shm->cc_shm_id[idx] < 0) {

    PFATAL("@FUN, fun_cc_shm_init(), shmget() failed");

  }

  // https://www.ibm.com/docs/en/zos/2.1.0?topic=functions-shmat-shared-memory-attach-operation
  // The shmat() function attaches the shared memory segment associated with the shared memory
  // identifier, shmid, to the address space of the calling process.
  shm->cc_map[idx] = shmat(shm->cc_shm_id[idx], NULL, 0);

  if (shm->cc_map[idx] == (void *)-1 || !shm->cc_map[idx]) {

    // shmctl() -- Perform Shared Memory Control Operations
    shmctl(shm->cc_shm_id[idx], IPC_RMID, NULL);  // do not leak shmem
    PFATAL("@FUN, fun_cc_shm_init(), shmctl() failed");

  }

  // Prepare one hot cc_shm for writing and one cold cc_shm for reading.
  if (idx == CC_IDX_HOT) {

    // Make the hot cc_shm visible to the instrumented PUT
    u8 *id_str = alloc_printf("%d", shm->cc_shm_id[idx]);
    setenv(FUN_CC_SHM_ENV_VAR, id_str, 1);
    ck_free(id_str);

  }

  // Keep map_size info.
  if (!shm->cc_map_size) shm->cc_map_size = map_size;

  FUN_LOG("fun_cc_shm_init(), shm->cc_shm_id[%d] %d, shm->cc_map[%d] %p, shm->cc_map_size %u",
          idx, shm->cc_shm_id[idx], idx, shm->cc_map[idx], shm->cc_map_size);

  return shm->cc_map[idx];

}


double *fun_fs_shm_init(sharedmem_t *shm, size_t size, u8 idx) {

  if (!shm->fun_mode) return NULL;

  // Debug
  FUN_LOG("fun_fs_shm_init(), idx=%d", idx);

  u32 map_size;

  // Sanitize and initialize
  if (shm->fs_map_size > 0) {

    if (shm->fs_map_size != size) {

      PFATAL("@FUN, Unequal map_size, fs_map_size %u, size %lu",
             shm->fs_map_size, size);

    } else {

      map_size = shm->fs_map_size;

    }

  } else {

    shm->fs_map_size = 0;
    map_size = size;

  }

  // Initialize map ptr
  shm->fs_map[idx] = NULL;

  // shmget
  shm->fs_shm_id[idx] =
      shmget(IPC_PRIVATE, map_size, IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION);

  if (shm->fs_shm_id[idx] < 0) {

    PFATAL("@FUN, fs_map(), shmget() failed");

  }

  // https://www.ibm.com/docs/en/zos/2.1.0?topic=functions-shmat-shared-memory-attach-operation
  // The shmat() function attaches the shared memory segment associated with the shared memory
  // identifier, shmid, to the address space of the calling process.
  shm->fs_map[idx] = shmat(shm->fs_shm_id[idx], NULL, 0);

  if (shm->fs_map[idx] == (void *)-1 || !shm->fs_map[idx]) {

    // shmctl() -- Perform Shared Memory Control Operations
    shmctl(shm->fs_shm_id[idx], IPC_RMID, NULL);  // do not leak shmem

    PFATAL("@FUN, fs_map(), shmctl() failed");
  }

  // Keep map_size info.
  if (!shm->fs_map_size) shm->fs_map_size = map_size;

  FUN_LOG("fun_fs_shm_init(), shm->fs_shm_id[%d] %d, shm->fs_map[%d] %p, shm->fs_map_size %u",
          idx, shm->fs_shm_id[idx], idx, shm->fs_map[idx], shm->fs_map_size);

  return shm->fs_map[idx];

}


void fun_shm_deinit(sharedmem_t *shm){

  // Debug
  FUN_LOG("fun_shm_deinit()");

  if (shm == NULL)    return ;

  if (!shm->fun_mode) return ;

  // Remove shm obj. May not necessary.
  // list_remove(&shm_list, shm);

  // Unset env
  unsetenv(FUN_CC_SHM_ENV_VAR);

  // Free shm

  shmctl(shm->cc_hot_id_shm_id, IPC_RMID, NULL);
  shm->cc_hot_id_map = NULL;

  for (u8 idx = 0; idx < SHM_IDX; ++idx) {

    shmctl(shm->cc_shm_id[idx], IPC_RMID, NULL);
    shm->cc_map[idx] = NULL;

    shmctl(shm->fs_shm_id[idx], IPC_RMID, NULL);
    shm->fs_map[idx] = NULL;

  }

}


s32 *fun_cc_hot_id_shm_init(sharedmem_t *shm) {

  // Debug
  FUN_LOG("fun_cc_hot_id_shm_init()");

  // Only preserving one integer
  u32 map_size = sizeof(s32);
  u8 *shm_str;

  // Initialize map ptr
  shm->cc_hot_id_map = NULL;

  // shmget
  shm->cc_hot_id_shm_id =
      shmget(IPC_PRIVATE, map_size, IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION);

  if (shm->cc_hot_id_shm_id < 0) {

    PFATAL("fun_cc_hot_id_shm_init(), shmget() failed");

  }

  // https://www.ibm.com/docs/en/zos/2.1.0?topic=functions-shmat-shared-memory-attach-operation
  // The shmat() function attaches the shared memory segment associated with the shared memory
  // identifier, shmid, to the address space of the calling process.
  shm->cc_hot_id_map = shmat(shm->cc_hot_id_shm_id, NULL, 0);

  // To avoid memory leak.
  if (shm->cc_hot_id_map == (void *)-1 || !shm->cc_hot_id_map) {

    // shmctl() -- Perform Shared Memory Control Operations
    shmctl(shm->cc_hot_id_shm_id, IPC_RMID, NULL);  // do not leak shmem

    PFATAL("fun_cc_hot_id_shm_init(), shmctl() failed");
  }

  FUN_LOG("fun_cc_hot_id_shm_init(), shm->cc_hot_id_shm_id %d, shm->cc_hot_id_map %p, map_size %u",
          shm->cc_hot_id_shm_id, shm->cc_hot_id_map, map_size);

  // Set to env
  shm_str = alloc_printf("%d", shm->cc_hot_id_shm_id);
  setenv(FUN_CC_SHM_ENV_VAR, shm_str, 1);
  ck_free(shm_str);

  return shm->cc_hot_id_map;

}


