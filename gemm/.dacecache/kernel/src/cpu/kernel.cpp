/* DaCe AUTO-GENERATED FILE. DO NOT MODIFY */
#include <dace/dace.h>
#include "../../include/hash.h"
constexpr long long NI = 60;
constexpr long long NJ = 70;
constexpr long long NK = 80;

struct kernel_state_t {
    dace_fpga_context *fpga_context;
};



DACE_EXPORTED void __dace_runstate_0_kernel_0(kernel_state_t *__state, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &__tmp0, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &__tmp1, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &__tmp2, double alpha, double beta, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_A, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_B, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_C);

void __program_kernel_internal(kernel_state_t*__state, double * __restrict__ A, double * __restrict__ B, double * __restrict__ C, double alpha, double beta)
{
    hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> fpga_A;
    fpga_A = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, -1, 4800);
    hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> fpga_B;
    fpga_B = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, -1, 5600);
    hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> fpga_C;
    fpga_C = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, -1, 4200);

    {

        fpga_A.CopyFromHost(0, 60 * 80, A);
        fpga_B.CopyFromHost(0, 80 * 70, B);
        fpga_C.CopyFromHost(0, 60 * 70, C);

    }
    {
        hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> __tmp0;
        __tmp0 = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, -1, 4800);
        hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> __tmp1;
        __tmp1 = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, -1, 4200);
        hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> __tmp2;
        __tmp2 = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, -1, 4200);
        __dace_runstate_0_kernel_0(__state, __tmp0, __tmp1, __tmp2, alpha, beta, fpga_A, fpga_B, fpga_C);

    }
    {

        fpga_C.CopyToHost(0, 60 * 70, C);

    }
}

DACE_EXPORTED void __program_kernel(kernel_state_t *__state, double * __restrict__ A, double * __restrict__ B, double * __restrict__ C, double alpha, double beta)
{
    __program_kernel_internal(__state, A, B, C, alpha, beta);
}
DACE_EXPORTED int __dace_init_xilinx(kernel_state_t *__state);

DACE_EXPORTED kernel_state_t *__dace_init_kernel()
{
    int __result = 0;
    kernel_state_t *__state = new kernel_state_t;


    __result |= __dace_init_xilinx(__state);

    if (__result) {
        delete __state;
        return nullptr;
    }
    return __state;
}

DACE_EXPORTED int __dace_exit_kernel(kernel_state_t *__state)
{
    int __err = 0;
    delete __state;
    return __err;
}

