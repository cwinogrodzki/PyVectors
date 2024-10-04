import sys
import laplacian_numpy as lap_np
import laplacian_pytorch as lap_torch
import laplacian_for as lap_for
# lap_cpp

def main():
  # pass device, framework args from shell script
  # module load needed modules
  # load correct conda env + runtime from script

  # Default problem size
  nx, ny, nz = 70, 70, 70

  if (len(sys.argv) > 0):
    nx = int(sys.argv[1])
  if (len(sys.argv) > 1):
    ny = int(sys.argv[2])
  if (len(sys.argv) > 2):
    nz = int(sys.argv[3])

  # prompt for which framework- numpy, torch, numpy_slow, cpp, all
  framework = input("Enter problem size: ")

  # Theoretical fetch and write sizes: size of grid - edges * float bytes * GB scale factor
  num_elements = nx * ny * nz
  reads = num_elements - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2)
  theoretical_fetch_size = reads * 8 * 1e-9
  writes = (nx - 2) * (ny - 2) * (nz - 2)
  theoretical_write_size = writes * 8 * 1e-9
  memory_transactions = reads + writes
  flop_count = 10 * (nx-2) * (ny-2) * (nz-2)
  arithmetic_intensity = flop_count / memory_transactions

  # Run kernel
  time = lap_np.initialize(nx, ny, nz)
  
  # Effective memory bandwidth
  bandwidth = (theoretical_fetch_size + theoretical_write_size) / time
  
  print(f"kernel took: {time * 1000:.4f} ms, effective memory bandwidth: {bandwidth:.4f} GB/s")
  # print(f"Numpy kernel time: {t1 * 1000:.4f} ms, effective memory bandwidth: {numpy_bandwidth:.4f} GB/s")
  # print(f"For loop kernel time: {t2 * 1000:.4f} ms, effective memory bandwidth: {for_bandwidth:.4f} GB/s")

if __name__ == "__main__":
    main()