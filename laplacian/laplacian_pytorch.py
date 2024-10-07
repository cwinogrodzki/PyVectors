import time
import torch

def kernel(A, B, nx, ny, nz):
    # Grid spacings
    hx = 1.0 / (nx - 1)
    hy = 1.0 / (ny - 1)
    hz = 1.0 / (nz - 1)

    INVHX2 = 1.0 / hx / hx
    INVHY2 = 1.0 / hy / hy
    INVHZ2 = 1.0 / hz / hz
    INVHXYZ2 = -2.0 * (INVHX2 + INVHY2 + INVHZ2)

    B[1:-1, 1:-1, 1:-1] = (A[1:-1, 1:-1, 1:-1] * INVHXYZ2 +
                            (A[2:, 1:-1, 1:-1] + A[:-2, 1:-1, 1:-1]) * INVHX2 +
                            (A[1:-1, 2:, 1:-1] + A[1:-1, :-2, 1:-1]) * INVHY2 +
                            (A[1:-1, 1:-1, 2:] + A[1:-1, 1:-1, :-2]) * INVHZ2)

def initialize(nx, ny, nz, iter):
    # if(device == 'cpu'):
    #     print("CPU capability: ", torch.backends.cpu.get_cpu_capability())
    #     if torch.backends.mkl.is_available(): print("Using oneMKL.")
    #     if torch.backends.mkldnn.is_available(): print("Using oneDNN.")
    # elif(device == 'mps'):
    #     #check that MPS is available
    #     if not torch.backends.mps.is_available():
    #         if not torch.backends.mps.is_built():
    #             print("MPS not available because the current PyTorch install was not "
    #             "built with MPS enabled.")
    #         else:
    #             print("MPS not available because the current MacOS version is not 12.3+ "
    #             "and/or you do not have an MPS-enabled device on this machine.")
    #         device = 'cpu' 
    #     else: device = 'mps'
    # elif(device == 'rocm'):
    #     #check that ROCm is available
    #     if not torch.cuda.is_available():
    #         if not torch.backends.cuda.is_built():
    #             print("ROCm not available because the current PyTorch install was not "
    #             "built with ROCm.")
    #         else:
    #             print("ROCm not available because no device is detected.")
    #         device = 'cpu' 
    #     else:
    #         print("Using device: ", torch.cuda.get_device_name(0))
    #         device = 'cuda'
    #         torch.backends.cuda.preferred_blas_library(backend='hipblaslt')
    # elif(device == 'cuda'):
    #     #check that CUDA is available
    #     if not torch.cuda.is_available():
    #         if not torch.backends.cuda.is_built():
    #             print("CUDA not available because the current PyTorch install was not "
    #             "built with CUDA.")
    #         else:
    #             print("CUDA not available because no device is detected.")
    #         device = 'cpu' 
    #     else:
    #         print("Using device: ", torch.cuda.get_device_name(0))
    #         torch.backends.cuda.preferred_blas_library(backend='cublas')

    A = torch.fromfunction(lambda i, j, k: (i + j + (nx - k)) * 10 / nx, (nx, ny, nz),
                    dtype=torch.float64)
    B = torch.copy(A)

    total_elapsed = 0
    for k in range(1, iter):
        start = time.perf_counter()
        numpy_result = kernel(A, B, nx, ny, nz)
        elapsed = time.perf_counter() - start
        total_elapsed =+ elapsed

    return total_elapsed

