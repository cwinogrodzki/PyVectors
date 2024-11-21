#include <dace/dace.h>
typedef void * ataxHandle_t;
extern "C" ataxHandle_t __dace_init_atax();
extern "C" int __dace_exit_atax(ataxHandle_t handle);
extern "C" void __program_atax(ataxHandle_t handle, double * __restrict__ A, double * __restrict__ __return, double * __restrict__ x);
