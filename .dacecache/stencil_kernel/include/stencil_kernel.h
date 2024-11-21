#include <dace/dace.h>
typedef void * stencil_kernelHandle_t;
extern "C" stencil_kernelHandle_t __dace_init_stencil_kernel(long long N);
extern "C" int __dace_exit_stencil_kernel(stencil_kernelHandle_t handle);
extern "C" void __program_stencil_kernel(stencil_kernelHandle_t handle, double * __restrict__ A, double * __restrict__ B, long long N);
