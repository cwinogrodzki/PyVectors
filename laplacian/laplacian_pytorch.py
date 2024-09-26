import time
import sys
import torch
# testing email
def laplacian(f, u, nx, ny, nz, hx, hy, hz):
    # Check that u is a 3D tensor
    u = u.view(nx, ny, nz)
    
    INVHX2 = 1.0 / hx / hx
    INVHY2 = 1.0 / hy / hy
    INVHZ2 = 1.0 / hz / hz
    INVHXYZ2 = -2.0 * (INVHX2 + INVHY2 + INVHZ2)

    f[1:-1, 1:-1, 1:-1] = (u[1:-1, 1:-1, 1:-1] * INVHXYZ2 +
                            (u[2:, 1:-1, 1:-1] + u[:-2, 1:-1, 1:-1]) * INVHX2 +
                            (u[1:-1, 2:, 1:-1] + u[1:-1, :-2, 1:-1]) * INVHY2 +
                            (u[1:-1, 1:-1, 2:] + u[1:-1, 1:-1, :-2]) * INVHZ2)

def main():
    # Default problem size
    nx, ny, nz = 512, 512, 512

    # Default device
    device = 'cpu' 

    if len(sys.argv) > 0:
        nx = int(sys.argv[1])
    if len(sys.argv) > 1:
        ny = int(sys.argv[2])
    if len(sys.argv) > 2:
        nz = int(sys.argv[3])
    if len(sys.argv) > 3:
        device = sys.argv[4]
    if len(sys.argv) > 4:
        precision_str = sys.argv[5]

    if(device == 'cpu'):
        print("CPU capability: ", torch.backends.cpu.get_cpu_capability())
        if torch.backends.mkl.is_available(): print("Using oneMKL.")
        if torch.backends.mkldnn.is_available(): print("Using oneDNN.")
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
        else: device = 'mps'
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
            torch.backends.cuda.preferred_blas_library(backend='hipblaslt')
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

    print(f"nx, ny, nz = {nx}, {ny}, {nz}")

    # Theoretical fetch and write sizes
    num_elements = nx * ny * nz
    precision = torch.float32
    float_bytes = 4
    
    if precision_str=='float64':
        precision = torch.float64
        float_bytes = 8
    elif precision_str=='float16':
        precision = torch.float16
        float_bytes = 2


    theoretical_fetch_size = (num_elements - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2)) * float_bytes * 1e-9
    reads = num_elements - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2)
    theoretical_write_size = ((nx - 2) * (ny - 2) * (nz - 2)) * float_bytes * 1e-9
    writes = (nx - 2) * (ny - 2) * (nz - 2)
    memory_trans = reads + writes
    flop_count = 10*(nx-2)*(ny-2)*(nz-2)
    arithmetic_intensity = flop_count / memory_trans

    print(f"Theoretical fetch size (GB): {theoretical_fetch_size:.4f}")
    print(f"Theoretical write size (GB): {theoretical_write_size:.4f}")

    d_u = torch.zeros((nx, ny, nz), dtype=precision, device=device)
    d_f = torch.zeros_like(d_u)

    # Grid spacings
    hx = 1.0 / (nx - 1)
    hy = 1.0 / (ny - 1)
    hz = 1.0 / (nz - 1)

    # Compute Laplacian
    start_time = time.perf_counter()
    laplacian(d_f, d_u, nx, ny, nz, hx, hy, hz)
    end_time = time.perf_counter()

    # Effective memory bandwidth
    elapsed_time = end_time - start_time
    bandwidth = (theoretical_fetch_size + theoretical_write_size) / elapsed_time
    throughput = flop_count / elapsed_time
    print(f"Laplacian kernel took: {elapsed_time * 1000:.4f} ms, effective memory bandwidth: {bandwidth:.4f} GB/s")
    print(f"Computational throughput: {throughput * 1e-9 / elapsed_time:.4f} GFLOP/s, arithmetic intensity: {arithmetic_intensity:.4f} FLOPS/byte")

if __name__ == "__main__":
    main()
