//
// Simulate afl-compiler-rt.o, which initialize shm before fuzzing.
//
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>

#include "common.h"

#define CTOR_PRIO 3

static int  __area_init[1];
int         *__area_ptr = __area_init;

// Default 0, used as NULL
long long   __area_addr = 0;

// Function called before running main.
__attribute__((constructor(CTOR_PRIO)))
static void __init(void) {

  printf("__init()[start], __area_ptr-p %p\n", __area_ptr);

  printf("__init(), build mmap_shm...\n");
  int fd = open(GCC_MMAP_FILE, O_RDONLY);

  // Bind ptr
  __area_ptr = mmap(0, FSIZE, PROT_READ, MAP_SHARED, fd, 0);

  // Log at the end
  printf("__init()[after shmat()], __area_ptr-p %p\n", __area_ptr);

}
