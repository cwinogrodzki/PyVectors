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

# Data set sizes
# NI, NJ, NK
sizes = {
    "mini": (20, 25, 30),
    "small": (60, 70, 80),
    "medium": (200, 220, 240),
    "large": (1000, 1100, 1200),
    "extra-large": (2000, 2300, 2600)
}

Nx, Ny, Nz = (dc.symbol(s, dtype=dc.int64) for s in ('Nx', 'Ny', 'Nz'))

@dc.program
def stencil_kernel(A: dc.float64[Nx, Ny, Nz], B: dc.float64[Nx, Ny, Nz], INVHX2: dc.int64, INVHY2: dc.int64, INVHZ2: dc.int64, INVHXYZ2: dc.int64):
    B[1:-1, 1:-1, 1:-1] = (A[1:-1, 1:-1, 1:-1] * INVHXYZ2 +
                            (A[2:, 1:-1, 1:-1] + A[:-2, 1:-1, 1:-1]) * INVHX2 +
                            (A[1:-1, 2:, 1:-1] + A[1:-1, :-2, 1:-1]) * INVHY2 +
                            (A[1:-1, 1:-1, 2:] + A[1:-1, 1:-1, :-2]) * INVHZ2)


def initialize(Nx, Ny, Nz, datatype=np.float64):
    # alpha = datatype(1.5)
    # beta = datatype(1.2)
    # C = np.fromfunction(lambda i, j: ((i * j + 1) % NI) / NI, (NI, NJ), dtype=datatype)
    # A = np.fromfunction(lambda i, k: (i * (k + 1) % NK) / NK, (NI, NK), dtype=datatype)
    # B = np.fromfunction(lambda k, j: (k * (j + 2) % NJ) / NJ, (NK, NJ), dtype=datatype)

    # A = np.fromfunction(lambda i, j, k: np.rand, (Nx, Ny, Nz),
    #                 dtype=datatype)
    # A = np.random.rand(Nx, Ny, Nz)
    A = np.fromfunction(lambda i, j, k: (i + j + (Nx - k)) * Nx / Nx, (Nx, Ny, Nz),
                    dtype=datatype)
    B = np.copy(A)

    hx = 1.0 / (Nx - 1)
    hy = 1.0 / (Ny - 1)
    hz = 1.0 / (Nz - 1)

    INVHX2 = 1.0 / hx / hx
    INVHY2 = 1.0 / hy / hy
    INVHZ2 = 1.0 / hz / hz
    INVHXYZ2 = -2.0 * (INVHX2 + INVHY2 + INVHZ2)

    return A, B, INVHX2, INVHY2, INVHZ2, INVHXYZ2


def run_stencil(device_type: dace.dtypes.DeviceType):
    '''
    Runs laplacian stencil for the given device
    :return: the SDFG
    '''

    # Initialize data (polybench small size)
    Nx, Ny, Nz = sizes["small"]
    A, B, INVHX2, INVHY2, INVHZ2, INVHXYZ2 = initialize(Nx, Ny, Nz)
    B_ref = np.copy(B)

    if device_type in {dace.dtypes.DeviceType.CPU, dace.dtypes.DeviceType.GPU}:
        # Parse the SDFG and apply auto-opt
        sdfg = stencil_kernel.to_sdfg()
        sdfg = auto_optimize(sdfg, device_type)
        sdfg.specialize(dict(Nx=Nx, Ny=Ny, Nz=Nz))
        sdfg(A, B, INVHX2, INVHY2, INVHZ2, INVHXYZ2)
    elif device_type == dace.dtypes.DeviceType.FPGA:
        # # Parse SDFG and apply FPGA friendly optimization
        # # Transformation creates additional pre- and post-states to perform memory transfers between host and device
        # sdfg = stencil_kernel.to_sdfg(simplify=True)
        # applied = sdfg.apply_transformations([FPGATransformSDFG])
        # assert applied == 1

        # # Use FPGA Expansion for lib nodes, and expand them to enable further optimizations
        # # from dace.libraries.blas import Gemm
        # # Gemm.default_implementation = "FPGA1DSystolic"
        # # sdfg.expand_library_nodes()
        # # sdfg.apply_transformations_repeated([InlineSDFG], print_report=True)
        # sdfg.specialize(dict(Nx=Nx, Ny=Ny, Nz=Nz))
        # # sdfg.expand_library_nodes(recursive=False)
        # sdfg(A, B, INVHX2, INVHY2, INVHZ2, INVHXYZ2)
        
        sdfg = stencil_kernel.to_sdfg()
        sdfg = auto_optimize(sdfg, dace.dtypes.DeviceType.FPGA)
        sdfg.expand_library_nodes()
        sdfg.specialize(dict(Nx=Nx, Ny=Ny, Nz=Nz))
        sdfg

    # Compute ground truth and validate
    # stencil_kernel.f(A, B_ref, INVHX2, INVHY2, INVHZ2, INVHXYZ2)
    # assert np.allclose(B, B_ref)
    # return sdfg


def test_cpu():
    run_stencil(dace.dtypes.DeviceType.CPU)


@pytest.mark.gpu
def test_gpu():
    run_stencil(dace.dtypes.DeviceType.GPU)


@fpga_test(assert_ii_1=False, xilinx=True)
def test_fpga():
    return run_stencil(dace.dtypes.DeviceType.FPGA)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", default='cpu', choices=['cpu', 'gpu', 'fpga'], help='Target platform')

    args = vars(parser.parse_args())
    target = args["target"]

    if target == "cpu":
        run_stencil(dace.dtypes.DeviceType.CPU)
    elif target == "gpu":
        run_stencil(dace.dtypes.DeviceType.GPU)
    elif target == "fpga":
        run_stencil(dace.dtypes.DeviceType.FPGA)