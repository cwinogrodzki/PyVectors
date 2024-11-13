# Based on ETH Zurich - SPCL example
# Original application code: NPBench - https://github.com/spcl/npbench
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

N = 100
TSTEPS = 50
#N = (dc.symbol('N', dtype=dc.int64))
#TSTEPS = (dc.symbol('TSTEPS', dtype=dc.int64))

@dc.program
def stencil_kernel(A: dc.float64[N, N, N], B: dc.float64[N, N, N]):
    for t in range(1, TSTEPS):
        B[1:-1, 1:-1, 1:-1] = (0.125 * (A[2:, 1:-1, 1:-1] - 2.0 * A[1:-1, 1:-1, 1:-1] + A[:-2, 1:-1, 1:-1]) + 
                               0.125 * (A[1:-1, 2:, 1:-1] - 2.0 * A[1:-1, 1:-1, 1:-1] + A[1:-1, :-2, 1:-1]) + 
                               0.125 * (A[1:-1, 1:-1, 2:] - 2.0 * A[1:-1, 1:-1, 1:-1] + A[1:-1, 1:-1, 0:-2]) + A[1:-1, 1:-1, 1:-1])
        
        A[1:-1, 1:-1, 1:-1] = (0.125 * (B[2:, 1:-1, 1:-1] - 2.0 * B[1:-1, 1:-1, 1:-1] + B[:-2, 1:-1, 1:-1]) + 
                               0.125 * (B[1:-1, 2:, 1:-1] - 2.0 * B[1:-1, 1:-1, 1:-1] + B[1:-1, :-2, 1:-1]) + 
                               0.125 * (B[1:-1, 1:-1, 2:] - 2.0 * B[1:-1, 1:-1, 1:-1] + B[1:-1, 1:-1, 0:-2]) + B[1:-1, 1:-1, 1:-1])
# @dc.program
# def stencil_kernel(TSTEPS: dc.int64, A: dc.float64[N, N, N], B: dc.float64[N, N, N]):

#     for t in range(1, TSTEPS):
#         B[1:-1, 1:-1,
#           1:-1] = (SF * (A[2:, 1:-1, 1:-1] - 2.0 * A[1:-1, 1:-1, 1:-1] +
#                             A[:-2, 1:-1, 1:-1]) + SF *
#                    (A[1:-1, 2:, 1:-1] - 2.0 * A[1:-1, 1:-1, 1:-1] +
#                     A[1:-1, :-2, 1:-1]) + SF *
#                    (A[1:-1, 1:-1, 2:] - 2.0 * A[1:-1, 1:-1, 1:-1] +
#                     A[1:-1, 1:-1, 0:-2]) + A[1:-1, 1:-1, 1:-1])
#         A[1:-1, 1:-1,
#           1:-1] = (SF * (B[2:, 1:-1, 1:-1] - 2.0 * B[1:-1, 1:-1, 1:-1] +
#                             B[:-2, 1:-1, 1:-1]) + SF *
#                    (B[1:-1, 2:, 1:-1] - 2.0 * B[1:-1, 1:-1, 1:-1] +
#                     B[1:-1, :-2, 1:-1]) + SF *
#                    (B[1:-1, 1:-1, 2:] - 2.0 * B[1:-1, 1:-1, 1:-1] +
#                     B[1:-1, 1:-1, 0:-2]) + B[1:-1, 1:-1, 1:-1])

def initialize(N, datatype=np.float64):
    A = np.fromfunction(lambda i, j, k: (i + j + (N - k)) * 10 / N, (N, N, N),
                    dtype=datatype)
    B = np.fromfunction(lambda i, j, k: (i + j + (N - k)) * 10 / N, (N, N, N),
                    dtype=datatype)
    #B = np.copy(A)

    return A, B


def run_stencil(device_type: dc.dtypes.DeviceType):
    '''
    Runs laplacian stencil for the given device
    :return: the SDFG
    '''

    # Initialize data
    A, B = initialize(N)
    B_ref = np.copy(B)

    if device_type in {dc.dtypes.DeviceType.CPU, dc.dtypes.DeviceType.GPU}:
        # Parse the SDFG and apply auto-opt
        sdfg = stencil_kernel.to_sdfg()
        sdfg = auto_optimize(sdfg, device_type)
        sdfg(A, B, N=N)
    elif device_type == dc.dtypes.DeviceType.FPGA:
        # Parse SDFG and apply FPGA friendly optimization
        # Transformation creates additional pre- and post-states to perform memory transfers between host and device
        sdfg = stencil_kernel.to_sdfg()
        #sdfg.apply_transformations(FPGATransformSDFG)
        sdfg = auto_optimize(sdfg, dc.dtypes.DeviceType.FPGA)
        #sdfg.expand_library_nodes()
        sdfg.specialize(N=N)
        sdfg(A, B)

    # Compute ground truth and validate
    stencil_kernel.f(A, B_ref)
    assert np.allclose(B, B_ref)
    return sdfg

if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-t", "--target", default='cpu', choices=['cpu', 'gpu', 'fpga'], help='Target platform')

    # args = vars(parser.parse_args())
    # target = args["target"]
    target="fpga"

    if target == "cpu":
        run_stencil(dc.dtypes.DeviceType.CPU)
    elif target == "gpu":
        run_stencil(dc.dtypes.DeviceType.GPU)
    elif target == "fpga":
        run_stencil(dc.dtypes.DeviceType.FPGA)