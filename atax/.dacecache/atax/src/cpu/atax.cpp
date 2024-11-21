/* DaCe AUTO-GENERATED FILE. DO NOT MODIFY */
#include <dace/dace.h>
#include "../../include/hash.h"
constexpr long long M = 60;
constexpr long long N = 70;

struct atax_state_t {
    dace_fpga_context *fpga_context;
};



DACE_EXPORTED void __dace_runstate_0_atax_0(atax_state_t *__state, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &__tmp0, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_A, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga___return, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_x);

void __program_atax_internal(atax_state_t*__state, double * __restrict__ A, double * __restrict__ __return, double * __restrict__ x)
{
    hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> fpga_A;
    fpga_A = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 1, 4200);
    hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> fpga_x;
    fpga_x = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 2, 70);
    hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> fpga___return;
    fpga___return = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 3, 70);

    {

        fpga_A.CopyFromHost(0, 60 * 70, A);
        fpga_x.CopyFromHost(0, 70, x);
        fpga___return.CopyFromHost(0, 70, __return);

    }
    {
        hlslib::ocl::Buffer <double, hlslib::ocl::Access::readWrite> __tmp0;
        __tmp0 = __state->fpga_context->Get().MakeBuffer<double, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 0, 60);
        __dace_runstate_0_atax_0(__state, __tmp0, fpga_A, fpga___return, fpga_x);

    }
    {

        fpga___return.CopyToHost(0, 70, __return);

    }
}

DACE_EXPORTED void __program_atax(atax_state_t *__state, double * __restrict__ A, double * __restrict__ __return, double * __restrict__ x)
{
    __program_atax_internal(__state, A, __return, x);
}
DACE_EXPORTED int __dace_init_xilinx(atax_state_t *__state);

DACE_EXPORTED atax_state_t *__dace_init_atax()
{
    int __result = 0;
    atax_state_t *__state = new atax_state_t;


    __result |= __dace_init_xilinx(__state);

    if (__result) {
        delete __state;
        return nullptr;
    }
    return __state;
}

DACE_EXPORTED int __dace_exit_atax(atax_state_t *__state)
{
    int __err = 0;
    delete __state;
    return __err;
}

