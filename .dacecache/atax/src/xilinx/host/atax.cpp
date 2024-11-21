#include "dace/xilinx/host.h"
#include "dace/dace.h"
#include "dace/xilinx/stream.h"


constexpr long long M = 60;
constexpr long long N = 70;

struct atax_state_t {
    dace_fpga_context *fpga_context;
};


DACE_EXPORTED int __dace_init_xilinx(atax_state_t *__state) {
    dace::unset_environment_variable("XCL_EMULATION_MODE");
    dace::unset_environment_variable("XILINX_SDX");
    dace::unset_environment_variable("EMCONFIG_PATH");
    
    
    __state->fpga_context = new dace_fpga_context();
    __state->fpga_context->Get().MakeProgram(DACE_BINARY_DIR "/atax_hw.xclbin");
    return 0;
}

DACE_EXPORTED int __dace_exit_xilinx(atax_state_t *__state) {
    delete __state->fpga_context;
    return 0;
}

///////////////////////////////////////////////////////////////////////////////
// Kernel: atax_0_0
///////////////////////////////////////////////////////////////////////////////

// Signature of kernel function (with raw pointers) for argument matching
DACE_EXPORTED void atax_0_0(double * __restrict__ __tmp0_0, double * __restrict__ fpga_A_0, double * __restrict__ fpga___return_0, double * __restrict__ fpga_x_0);

DACE_EXPORTED void __dace_runstate_0_atax_0(atax_state_t *__state, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &__tmp0, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_A, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga___return, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_x) {
    hlslib::ocl::Program program = __state->fpga_context->Get().CurrentlyLoadedProgram();
    std::vector<hlslib::ocl::Event> all_events;
    auto atax_0_0_kernel = program.MakeKernel(atax_0_0, "atax_0_0", __tmp0, fpga_A, fpga___return, fpga_x);
    hlslib::ocl::Event atax_0_0_event = atax_0_0_kernel.ExecuteTaskAsync();
    all_events.push_back(atax_0_0_event);
    hlslib::ocl::WaitForEvents(all_events);
}


