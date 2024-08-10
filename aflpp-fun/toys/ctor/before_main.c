//
// Test constructor order
//
#include "mydebug.h"

/// When priorities are different, call ctors by the given priorities.

__attribute__((constructor(3)))
static void __ctor3(void) {
  log("__ctor3");
}

__attribute__((constructor(1)))
static void __ctor1(void) {
  log("__ctor1");
}

__attribute__((constructor(2)))
static void __ctor2(void) {
  log("__ctor2");
}

/// When priorities are equal, call ctors by declaration order.

__attribute__((constructor(4)))
static void __ctor4_3(void) {
  log("__ctor4_3");
}

__attribute__((constructor(4)))
static void __ctor4_1(void) {
  log("__ctor4_1");
}

__attribute__((constructor(4)))
static void __ctor4_2(void) {
  log("__ctor4_2");
}

/// ((constructor())) implies "assigning priority as the declaration order".

__attribute__((constructor()))
static void __ctor_2(void) {
  log("__ctor_2");
}

__attribute__((constructor(0)))
static void __ctor0(void) {
  log("__ctor0");
}

__attribute__((constructor()))
static void __ctor_1(void) {
  log("__ctor_1");
}

