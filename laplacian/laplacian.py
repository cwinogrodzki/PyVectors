import sys
import laplacian_numpy
#import laplacian_pytorch
import laplacian_naive
#import laplacian_fpga
# lap_cpp

def main():
  # pass device, framework args from shell script
  # module load needed modules
  # load correct conda env + runtime from script

  # Defaults
  N = 10
  device = 'cpu'
  iter = 10
  framework = 'naive'

  if (len(sys.argv) > 1):
    framework = sys.argv[1]
  if (len(sys.argv) > 2):
    device = sys.argv[2]
  if (len(sys.argv) > 3):
    iter = int(sys.argv[3])
  if (len(sys.argv) > 4):
    N = int(sys.argv[4])

  nx, ny, nz = N, N, N
  # Theoretical fetch and write sizes: size of grid - edges * float bytes * GB scale factor
  num_elements = nx * ny * nz
  reads = num_elements - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2)
  theoretical_fetch_size = reads * 8 * 1e-9
  writes = (nx - 2) * (ny - 2) * (nz - 2)
  theoretical_write_size = writes * 8 * 1e-9
  memory_transactions = reads + writes
  flop_count = 10 * (nx-2) * (ny-2) * (nz-2)
  arithmetic_intensity = flop_count / memory_transactions

  # kernel_str = kernel + "_" + framework

  # Run kernel
  # module_filename = "{m}.py".format(m=self.info["module_name"])
  # module_pypath = "npbench.benchmarks.{r}.{m}".format(r=self.info["relative_path"].replace('/', '.'),
  #                                                     m=self.info["module_name"])
  # exec_str = "from {m} import {i}".format(m=module_pypath, i=self.info["init"]["func_name"])
  # try:
  #   exec(exec_str, data)
  # except Exception as e:
  #   print("Module Python file {m} could not be opened.".format(m=module_filename))
  #   raise (e)
  
  # print(kernel_str)
  # time = 0
  # exec_str = "time = " + kernel + "_" + framework + ".initialize(nx, ny, nz, 1)"
  # namespace = {'time': 0}
  # exec(exec_str , globals())

  framework = "naive"
  if (framework=="numpy"):
    time = laplacian_numpy.initialize(N, iter, device)
  # elif (framework=="pytorch"):
  #   time = laplacian_pytorch.initialize(N, iter, device)
  elif (framework=="naive"):
    time = laplacian_naive.initialize(N, iter, device)
  # elif (framework=="fpga"):
  #   time = laplacian_fpga.initialize(N, iter, device)
  
  # Effective memory bandwidth
  bandwidth = (theoretical_fetch_size + theoretical_write_size) / time
  
  print(f"{time * 1000:.4f}")
  # print(f"kernel took: {time * 1000:.4f} ms, effective memory bandwidth: {bandwidth:.4f} GB/s")
  # print(f"Numpy kernel time: {t1 * 1000:.4f} ms, effective memory bandwidth: {numpy_bandwidth:.4f} GB/s")
  # print(f"For loop kernel time: {t2 * 1000:.4f} ms, effective memory bandwidth: {for_bandwidth:.4f} GB/s")

if __name__ == "__main__":
  main()