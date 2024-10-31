#include <iostream>
#include <math.h>
#include <stdio.h>
#include <chrono>
#include <iomanip>
#include <assert.h>
#include <vector>

using precision = double;
using namespace std;

template <typename T>
void kernel(std::vector<T>& f, std::vector<T>& u, int N){
#define u(i, j, k) u[(i) + (j) * N  + (k) * N * N]
#define f(i, j, k) f[(i) + (j) * N  + (k) * N * N]
    
    //Skip boundary points
    for (int k = 0; k < N; ++k) {
        for (int j = 0; j < N; ++j) {
            for (int i = 0; i < N; ++i) {
                //Apply stencil approximation of Laplacian to all interior points
                float u_xx = (u(i + 1, j, k) - 2 * u(i, j, k) + u(i - 1, j, k)) * 0.125;
                float u_yy = (u(i, j + 1, k) - 2 * u(i, j, k) + u(i, j - 1, k)) * 0.125;
                float u_zz = (u(i, j, k + 1) - 2 * u(i, j, k) + u(i, j, k - 1)) * 0.125;
                f(i, j, k) = u_xx + u_yy + u_zz;
            }
        }
    }
#undef u
#undef f
}

int main(int argc, char **argv)
{
    // Default problem size
    size_t N = 100;  // Cube dimensions

    int num_iter = 10;

    if (argc > 1) {N = atoi(argv[1]);}

    size_t nx = N, ny = N, nz = N;

    // Theoretical fetch and write sizes:
    size_t theoretical_fetch_size = (nx * ny * nz - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2) ) * sizeof(precision) * 1e-9;
    size_t theoretical_write_size = ((nx - 2) * (ny - 2) * (nz - 2)) * sizeof(precision) * 1e-9;
    size_t num_elements = nx * ny * nz;
    size_t numbytes = num_elements * sizeof(precision);
    int reads = num_elements - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2);
    int writes = (nx - 2) * (ny - 2) * (nz - 2);
    int memory_trans = reads + writes;
    int flop_count = 10*(nx-2)*(ny-2)*(nz-2);
    int arithmetic_intensity = flop_count / memory_trans;

    std::vector<double> u(N*N*N);
    std::vector<double> f(N*N*N);
    u.reserve(N*N*N);
    f.reserve(N*N*N);

    // Compute Laplacian (1/2) (x(x-1) + y(y-1) + z(z-1)) = 3 for all interior points
    float total_elapsed;
    for (int iter = 0; iter < num_iter; ++iter) {
        auto started = std::chrono::high_resolution_clock::now();
        kernel<double>(f, u, N);
        auto done = std::chrono::high_resolution_clock::now();
        const double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(done-started).count();
        total_elapsed += elapsed;
    }

    float bandwidth = (theoretical_fetch_size + theoretical_write_size) * num_iter / total_elapsed;
   //throughput = flop_count / total_elapsed

    // printf("Laplacian kernel took: %g ms avg, effective memory bandwidth: %g GB/s \n",
    //         total_elapsed / num_iter,
    //         bandwidth
    //         );
    // std::cout << bandwidth;
    // std::cout << "Laplacian kernel took: " << std::fixed << std::setprecision(2) << total_elapsed / num_iter <<
    //              " ms avg, effective memory bandwidth: " << std::fixed << std::setprecision(2) << bandwidth << " GB/s \n";
    std::cout << std::fixed << std::setprecision(2) << total_elapsed / num_iter;

    //print(f"Computational throughput: {throughput * 1e-9 / elapsed_time:.4f} GFLOP/s, arithmetic intensity: {arithmetic_intensity:.4f} FLOPS/byte")

    return 0;
}