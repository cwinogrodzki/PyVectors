import time
import sys
import numpy as np


def main():
    # Check that MPS is available
    # if not torch.backends.mps.is_available():
    #     if not torch.backends.mps.is_built():
    #         print("MPS not available because the current PyTorch install was not "
    #           "built with MPS enabled.")
    #     else:
    #         print("MPS not available because the current MacOS version is not 12.3+ "
    #           "and/or you do not have an MPS-enabled device on this machine.")
    # else: mps_device = torch.device("mps")
    
    # Default problem size
    nx, ny, nz = 512, 512, 512

    if len(sys.argv) > 0:
        nx = int(sys.argv[1])
    if len(sys.argv) > 1:
        ny = int(sys.argv[2])
    if len(sys.argv) > 2:
        nz = int(sys.argv[3])

    print(f"nx, ny, nz = {nx}, {ny}, {nz}")

    # Theoretical fetch and write sizes
    precision = np.float32
    float_bytes = 4
    num_elements = nx * ny * nz

    theoretical_fetch_size = (num_elements - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2)) * float_bytes * 1e-9
    reads = num_elements - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2)
    theoretical_write_size = ((nx - 2) * (ny - 2) * (nz - 2)) * float_bytes * 1e-9
    writes = (nx - 2) * (ny - 2) * (nz - 2)
    memory_trans = reads + writes
    flop_count = 10*(nx-2)*(ny-2)*(nz-2)
    arithmetic_intensity = flop_count / memory_trans
    peak_flops = 13600 #GFLOPS FP32

    print(f"Theoretical fetch size (GB): {theoretical_fetch_size:.4f}")
    print(f"Theoretical write size (GB): {theoretical_write_size:.4f}")

    d_u = torch.zeros((nx, ny, nz), dtype=precision, device='mps')
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
    print(f"Computational throughput: {throughput * 1e-9 / elapsed_time} GFLOP/s, arithmetic intensity: {arithmetic_intensity} FLOPS/byte")



if __name__ == "__main__":
    main()