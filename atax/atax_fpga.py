import numpy as np
import dace as dc
from dace.transformation.interstate import FPGATransformSDFG
from dace.libraries.blas import Gemv
from dace.transformation.dataflow import StreamingMemory
from dace.transformation.interstate import InlineSDFG
from dace.transformation.auto.auto_optimize import fpga_auto_opt

M, N  = 60, 70

@dc.program
def atax(A: dc.float64[M, N], x: dc.float64[N]):
    return (A @ x) @ A

def initialize(M, N, dtype=np.float64):
    fn = dtype(N)
    x = np.fromfunction(lambda i: 1 + (i / fn), (N, ), dtype=dtype)
    A = np.fromfunction(lambda i, j: ((i + j) % N) / (5 * M), (M, N),
                        dtype=dtype)
    return x, A

def run_gemm(device_type: dc.dtypes.DeviceType):
    # to do: add CPU and GPU optimizations
    x, A = initialize(M, N)
    x_ref = np.copy(x)

    sdfg = atax.to_sdfg()
    sdfg.apply_transformations(FPGATransformSDFG)
    Gemv.default_implementation = "FPGA_Accumulate"
    sdfg.expand_library_nodes(recursive=False)
    sdfg.specialize(dict(M=M, N=N))
    sdfg.apply_transformations_repeated([InlineSDFG, StreamingMemory],
                                                            [{}, {
                                                                'storage': dc.StorageType.FPGA_Local
                                                            }],
                                                            print_report=True)
    fpga_auto_opt.fpga_rr_interleave_containers_to_banks(sdfg, num_banks = 4, memory_type = "DDR")
    #y = sdfg(A,x)
    sdfg

    atax.f(A, x_ref)
    assert np.allclose(x, x_ref)

if __name__ == "__main__":
    target = "fpga"

    if target == "cpu":
        run_gemm(dc.dtypes.DeviceType.CPU)
    elif target == "gpu":
        run_gemm(dc.dtypes.DeviceType.GPU)
    elif target == "fpga":
        run_gemm(dc.dtypes.DeviceType.FPGA)