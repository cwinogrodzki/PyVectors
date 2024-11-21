/* DaCe AUTO-GENERATED FILE. DO NOT MODIFY */
#include <dace/dace.h>
#include "../../include/hash.h"

struct stencil_kernel_state_t {
    dace_fpga_context *fpga_context;
};



DACE_EXPORTED void __dace_runstate_0_stencil_kernel_0(stencil_kernel_state_t *__state, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_A, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_B, long long N);

void __program_stencil_kernel_internal(stencil_kernel_state_t*__state, double * __restrict__ A, double * __restrict__ B, long long N)
{
    hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> fpga_A;
    fpga_A = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 0, ((((N * N) * (N - 1)) + (N * (N - 1))) + N));
    hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> fpga_B;
    fpga_B = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 1, ((((N * N) * (N - 1)) + (N * (N - 1))) + N));

    {

        fpga_A.CopyFromHost(0, N * N * N, A);
        fpga_B.CopyFromHost(0, N * N * N, B);

    }
    {
        __dace_runstate_0_stencil_kernel_0(__state, fpga_A, fpga_B, N);

    }
    {

        fpga_B.CopyToHost(0, N * N * N, B);
        fpga_A.CopyToHost(0, N * N * N, A);

    }
}

DACE_EXPORTED void __program_stencil_kernel(stencil_kernel_state_t *__state, double * __restrict__ A, double * __restrict__ B, long long N)
{
    __program_stencil_kernel_internal(__state, A, B, N);
}
DACE_EXPORTED int __dace_init_xilinx(stencil_kernel_state_t *__state, long long N);

DACE_EXPORTED stencil_kernel_state_t *__dace_init_stencil_kernel(long long N)
{
    int __result = 0;
    stencil_kernel_state_t *__state = new stencil_kernel_state_t;


    __result |= __dace_init_xilinx(__state, N);

    if (__result) {
        delete __state;
        return nullptr;
    }
    return __state;
}

DACE_EXPORTED int __dace_exit_stencil_kernel(stencil_kernel_state_t *__state)
{
    int __err = 0;
    delete __state;
    return __err;
}

