//
// Simulate afl-compiler-rt.o, which initialize shm before fuzzing.
//
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/shm.h>

#include "common.h"

#define CTOR_PRIO 3

static int  __area_init[1];
int         *__area_ptr = __area_init;

// Default 0, used as NULL
long long   __area_addr = 0;

// Function called before running main.
__attribute__((constructor(CTOR_PRIO)))
static void __init(void) {

  char *shm_id_str;
  int   shm_id;

  printf("__init()[start], __area_ptr-p %p\n", __area_ptr);

  printf("__init(), get shm_id from env...\n");
  do {
    shm_id_str = getenv(SHM_ID);
    sleep(1);
    printf("__init(), shm_id_str=%s\n", shm_id_str);
  } while (!shm_id_str);
  shm_id  = atoi(shm_id_str);
  printf("__init(), shm_id %d\n", shm_id);

  // Attach
  __area_ptr = (int *) shmat(shm_id, (void *)__area_addr, 0);

  // Log at the end
  printf("__init()[after shmat()], __area_ptr-p %p\n", __area_ptr);

}
