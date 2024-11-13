#include <iostream>
#include <math.h>
#include <stdio.h>
#include <chrono>
#include <iomanip>
#include <assert.h>
#include <array>

using precision = double;
using namespace std;

template <int m, int n>
void kernel(double (&A)[m][n], double (&x)[n], double (&tmp)[m], double (&y)[n], int M, int N){
    for (i = 0; i < N; i++)
        y[i] = 0;
    for (i = 0; i < M; i++){
        tmp[i] = 0.0;
        for (j = 0; j < N; j++)
            tmp[i] = tmp[i] + A[i][j] * x[j];
        for (j = 0; j < N; j++)
            y[j] = y[j] + A[i][j] * tmp[i];
        }
    //return y;
}

int main(int argc, char **argv)
{
    int num_iter = 10;
    int M = 60, N = 70;

    if (argc > 1) {
        int M = atoi(argv[1]);
        int N = atoi(argv[2]);
    }

    double A[M][N];
    double x[N];
    double tmp[M];
    double y[N];

    double fn = double(N);
    int i, j;

    for (int i = 0; i < N; i++)
        x[i] = 1 + (i / fn);
    for (int i = 0; i < M; i++)
        for (int j = 0; j < N; j++)
            A[i][j] = double(((i+j) % N) / (5*M));

    float total_elapsed;
    for (int iter = 0; iter < num_iter; ++iter) {
        auto started = std::chrono::high_resolution_clock::now();
        kernel(A, x, tmp, y, M, N);
        auto done = std::chrono::high_resolution_clock::now();
        const double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(done-started).count();
        total_elapsed += elapsed;
    }

    //float bandwidth = (theoretical_fetch_size + theoretical_write_size) * num_iter / total_elapsed;

    std::cout << std::fixed << std::setprecision(2) << total_elapsed / num_iter;

    return 0;
}