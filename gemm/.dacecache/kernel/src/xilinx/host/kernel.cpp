#include "dace/xilinx/host.h"
#include "dace/dace.h"
#include "dace/xilinx/stream.h"


constexpr long long NI = 60;
constexpr long long NJ = 70;
constexpr long long NK = 80;

struct kernel_state_t {
    dace_fpga_context *fpga_context;
};


DACE_EXPORTED int __dace_init_xilinx(kernel_state_t *__state) {
    dace::unset_environment_variable("XCL_EMULATION_MODE");
    dace::unset_environment_variable("XILINX_SDX");
    dace::unset_environment_variable("EMCONFIG_PATH");
    
    
    __state->fpga_context = new dace_fpga_context();
    __state->fpga_context->Get().MakeProgram(DACE_BINARY_DIR "/kernel_hw.xclbin");
    return 0;
}

DACE_EXPORTED int __dace_exit_xilinx(kernel_state_t *__state) {
    delete __state->fpga_context;
    return 0;
}

///////////////////////////////////////////////////////////////////////////////
// Kernel: kernel_0_0
///////////////////////////////////////////////////////////////////////////////

// Signature of kernel function (with raw pointers) for argument matching
DACE_EXPORTED void kernel_0_0(double * __restrict__ __tmp0_0, double * __restrict__ __tmp1_0, double * __restrict__ __tmp2_0, double alpha, double beta, double * __restrict__ fpga_A_0, double * __restrict__ fpga_B_0, double * __restrict__ fpga_C_0);

DACE_EXPORTED void __dace_runstate_0_kernel_0(kernel_state_t *__state, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &__tmp0, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &__tmp1, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &__tmp2, double alpha, double beta, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_A, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_B, hlslib::ocl::Buffer<double, hlslib::ocl::Access::readWrite> &fpga_C) {
    hlslib::ocl::Program program = __state->fpga_context->Get().CurrentlyLoadedProgram();
    std::vector<hlslib::ocl::Event> all_events;
    auto kernel_0_0_kernel = program.MakeKernel(kernel_0_0, "kernel_0_0", __tmp0, __tmp1, __tmp2, alpha, beta, fpga_A, fpga_B, fpga_C);
    hlslib::ocl::Event kernel_0_0_event = kernel_0_0_kernel.ExecuteTaskAsync();
    all_events.push_back(kernel_0_0_event);
    hlslib::ocl::WaitForEvents(all_events);
}


