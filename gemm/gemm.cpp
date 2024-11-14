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
void kernel(double alpha, double beta, std::vector<T>& A, std::vector<T>& B, std::vector<T>& C, int Ni, int Nj, int Nk){
    for (int i = 0; k < Ni; ++i) {
        for (int j = 0; j < Nj; ++j) {
            result = 0;
            for (int k = 0; i < Nk; ++k) {
                result = A[i][k] * B[k][j];
            }
            C[i][j] = alpha * result + beta * C[i][j];
        }
    }
    return C;
}


int main(int argc, char **argv)
{
    int num_iter = 10;
    int Ni = 60, Nj = 70, Nk = 80;
    double alpha = 1.5;
    double beta = 1.2;

    if (argc > 1) {
        int Ni = atoi(argv[1]);
        int Nj = atoi(argv[2]);
        int Nk = atoi(argv[3]);
    }

    std::vector<double> A(Ni*Nj);
    std::vector<double> B(Nj*Nk);
    std::vector<double> C(Ni*Nk);
    A.reserve(Ni*Nj);
    B.reserve(Nj*Nk);
    C.reserve(Ni*Nk);

    float total_elapsed;
    for (int iter = 0; iter < num_iter; ++iter) {
        auto started = std::chrono::high_resolution_clock::now();
        kernel<double>(alpha, beta, A, B, C, Ni, Nj, Nk);
        auto done = std::chrono::high_resolution_clock::now();
        const double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(done-started).count();
        total_elapsed += elapsed;
    }

    //float bandwidth = (theoretical_fetch_size + theoretical_write_size) * num_iter / total_elapsed;

    std::cout << std::fixed << std::setprecision(2) << total_elapsed / num_iter;

    return 0;
}