#include "dace/xilinx/host.h"
#include "dace/dace.h"
#include "dace/xilinx/stream.h"



struct stencil_kernel_state_t {
    dace_fpga_context *fpga_context;
};


DACE_EXPORTED int __dace_init_xilinx(stencil_kernel_state_t *__state, long long N) {
    dace::unset_environment_variable("XCL_EMULATION_MODE");
    dace::unset_environment_variable("XILINX_SDX");
    dace::unset_environment_variable("EMCONFIG_PATH");
    
    
    __state->fpga_context = new dace_fpga_context();
    __state->fpga_context->Get().MakeProgram(DACE_BINARY_DIR "/stencil_kernel_hw.xclbin");
    return 0;
}

DACE_EXPORTED int __dace_exit_xilinx(stencil_kernel_state_t *__state) {
    delete __state->fpga_context;
    return 0;
}

///////////////////////////////////////////////////////////////////////////////
// Kernel: stencil_kernel_0_0
///////////////////////////////////////////////////////////////////////////////

// Signature of kernel function (with raw pointers) for argument matching
DACE_EXPORTED void stencil_kernel_0_0(double * __restrict__ fpga_A_0, double * __restrict__ fpga_B_0, long long N);

DACE_EXPORTED void __dace_runstate_0_stencil_kernel_0(stencil_kernel_state_t *__state, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_A, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_B, long long N) {
    hlslib::ocl::Program program = __state->fpga_context->Get().CurrentlyLoadedProgram();
    std::vector<hlslib::ocl::Event> all_events;
    auto stencil_kernel_0_0_kernel = program.MakeKernel(stencil_kernel_0_0, "stencil_kernel_0_0", fpga_A, fpga_B, N);
    hlslib::ocl::Event stencil_kernel_0_0_event = stencil_kernel_0_0_kernel.ExecuteTaskAsync();
    all_events.push_back(stencil_kernel_0_0_event);
    hlslib::ocl::WaitForEvents(all_events);
}


