#ifndef AFLPP_FUN_DEBUG_H
#define AFLPP_FUN_DEBUG_H

#define cYEL "\x1b[1;93m"
#define cRST "\x1b[0m"

#include <stdio.h>

static inline void log(char *mes) {
  printf(cYEL "[LOG]" cRST " %s\n", mes);
}

#endif  // AFLPP_FUN_DEBUG_H
