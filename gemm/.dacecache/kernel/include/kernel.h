#include <dace/dace.h>
typedef void * kernelHandle_t;
extern "C" kernelHandle_t __dace_init_kernel();
extern "C" int __dace_exit_kernel(kernelHandle_t handle);
extern "C" void __program_kernel(kernelHandle_t handle, double * __restrict__ A, double * __restrict__ B, double * __restrict__ C, double alpha, double beta);
