import time
import torch
import numpy as np

TSTEPS=50
def kernel(A, B):
    for t in range(1, TSTEPS):
        B[1:-1, 1:-1,
        1:-1] = (0.125 * (A[2:, 1:-1, 1:-1] - 2.0 * A[1:-1, 1:-1, 1:-1] +
                            A[:-2, 1:-1, 1:-1]) + 0.125 *
                    (A[1:-1, 2:, 1:-1] - 2.0 * A[1:-1, 1:-1, 1:-1] +
                    A[1:-1, :-2, 1:-1]) + 0.125 *
                    (A[1:-1, 1:-1, 2:] - 2.0 * A[1:-1, 1:-1, 1:-1] +
                    A[1:-1, 1:-1, 0:-2]) + A[1:-1, 1:-1, 1:-1])
        A[1:-1, 1:-1,
        1:-1] = (0.125 * (B[2:, 1:-1, 1:-1] - 2.0 * B[1:-1, 1:-1, 1:-1] +
                            B[:-2, 1:-1, 1:-1]) + 0.125 *
                    (B[1:-1, 2:, 1:-1] - 2.0 * B[1:-1, 1:-1, 1:-1] +
                    B[1:-1, :-2, 1:-1]) + 0.125 *
                    (B[1:-1, 1:-1, 2:] - 2.0 * B[1:-1, 1:-1, 1:-1] +
                    B[1:-1, 1:-1, 0:-2]) + B[1:-1, 1:-1, 1:-1])

def initialize(N, iter, device):
    if(device == 'cpu'):
        print("CPU capability: ", torch.backends.cpu.get_cpu_capability())
        if torch.backends.mkl.is_available(): print("Using oneMKL.")
        if torch.backends.mkldnn.is_available(): print("Using oneDNN.")
    elif(device == 'cuda'):
        #check that CUDA is available
        if not torch.cuda.is_available():
            if not torch.backends.cuda.is_built():
                print("CUDA not available because the current PyTorch install was not "
                "built with CUDA.")
            else:
                print("CUDA not available because no device is detected.")
            device = 'cpu'
        else:
            print("Using device: ", torch.cuda.get_device_name(0))
            torch.backends.cuda.preferred_blas_library(backend='cublas')
    elif(device == 'rocm'):
        #check that ROCm is available
        if not torch.cuda.is_available():
            if not torch.backends.cuda.is_built():
                print("ROCm not available because the current PyTorch install was not "
                "built with ROCm.")
            else:
                print("ROCm not available because no device is detected.")
            device = 'cpu' 
        else:
            print("Using device: ", torch.cuda.get_device_name(0))
            device = 'cuda'
            #torch.backends.cuda.preferred_blas_library(backend='hipblaslt') 
    elif(device == 'mps'):
        #check that MPS is available
        if not torch.backends.mps.is_available():
            if not torch.backends.mps.is_built():
                print("MPS not available because the current PyTorch install was not "
                "built with MPS enabled.")
            else:
                print("MPS not available because the current MacOS version is not 12.3+ "
                "and/or you do not have an MPS-enabled device on this machine.")
            device = 'cpu' 
    else:
        device='cpu'

    # A = torch.rand(size=(nx, ny, nz), dtype=torch.float64, device=device)
    # B = torch.rand_like(A)

    # A = torch.zeros(size=(N, N, N), dtype=torch.float64, device=device)
    # A.apply(lambda i, j, k: (i + j + (N - k)) * 10 / N)
    # B = torch.copy(A)

    A = torch.tensor(np.fromfunction(lambda i, j, k: (i + j + (N - k)) * 10 / N, (N, N, N),
                    dtype=np.float64), device=device)
    B = A.clone()

    print(device)

    total_elapsed = 0
    for k in range(1, iter):
        start = time.perf_counter()
        numpy_result = kernel(A, B)
        elapsed = time.perf_counter() - start
        print(elapsed)
        total_elapsed =+ elapsed

    # start = time.perf_counter()
    # numpy_result = kernel(A, B, nx, ny, nz)
    # total_elapsed = time.perf_counter() - start

    return total_elapsed/iter

