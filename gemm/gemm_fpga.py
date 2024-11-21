import dace.dtypes
import numpy as np
import dace as dc
import pytest
import argparse
from dace.fpga_testing import fpga_test, xilinx_test
from dace.transformation.interstate import FPGATransformSDFG, InlineSDFG
from dace.transformation.dataflow import StreamingMemory, StreamingComposition
from dace.transformation.auto.auto_optimize import auto_optimize
from dace.config import set_temporary

NI, NJ, NK = (dc.symbol(s, dtype=dc.int64) for s in ('NI', 'NJ', 'NK'))
#NI, NJ, NK = 60, 70, 80

@dc.program
def kernel(alpha: dc.float64, beta: dc.float64, C: dc.float64[NI, NJ],
           A: dc.float64[NI, NK], B: dc.float64[NK, NJ]):

    C[:] = alpha * A @ B + beta * C

def initialize(NI, NJ, NK, dtype=np.float64):
    A = np.fromfunction(lambda i, k: (i * (k + 1) % NK) / NK, (NI, NK),
                        dtype=dtype)
    B = np.fromfunction(lambda k, j: (k * (j + 2) % NJ) / NJ, (NK, NJ),
                        dtype=dtype)
    C = np.fromfunction(lambda i, j: ((i * j + 1) % NI) / NI, (NI, NJ),
                        dtype=dtype)

    return A, B, C

def run_gemm(device_type: dc.dtypes.DeviceType):
    # INItialize data
    NI, NJ, NK = 60, 70, 80
    alpha = np.float64(1.5)
    beta = np.float64(1.2)
    A, B, C = initialize(NI, NJ, NK)
    C_ref = np.copy(C)

    if device_type in {dc.dtypes.DeviceType.CPU, dc.dtypes.DeviceType.GPU}:
        # Parse the SDFG and apply auto-opt
        sdfg = kernel.to_sdfg()
        sdfg = auto_optimize(sdfg, device_type)
        sdfg(alpha, beta, C, A, B, NI=NI, NJ=NJ, NK=NK)
    elif device_type == dc.dtypes.DeviceType.FPGA:
        # Parse SDFG and apply FPGA friendly optimization
        sdfg = kernel.to_sdfg(simplify=True)
        applied = sdfg.apply_transformations([FPGATransformSDFG])
        assert applied == 1
        from dace.libraries.blas import Gemm
        Gemm.default_implementation = "FPGA1DSystolic"
        sdfg.expand_library_nodes()
        sdfg.apply_transformations_repeated([InlineSDFG], print_report=True)
        #sdfg.specialize(dict(NI=NI, NJ=NJ, NK=NK))
        sdfg(alpha, beta, A, B, C, NI=NI, NJ=NJ, NK=NK)

    # Compute ground truth and validate
    kernel.f(alpha, beta, C_ref, A, B)
    assert np.allclose(C, C_ref)
    return sdfg


#def iNItialize():
if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-t", "--target", default='cpu', choices=['cpu', 'gpu', 'fpga'], help='Target platform')

    # args = vars(parser.parse_args())
    # target = args["target"]
    target = "fpga"

    if target == "cpu":
        run_gemm(dc.dtypes.DeviceType.CPU)
    elif target == "gpu":
        run_gemm(dc.dtypes.DeviceType.GPU)
    elif target == "fpga":
        run_gemm(dc.dtypes.DeviceType.FPGA)