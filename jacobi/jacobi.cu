/**
 * jacobi2D.cu: This file is part of the PolyBench/GPU 1.0 test suite.
 *
 *
 * Contact: Scott Grauer-Gray <sgrauerg@gmail.com>
 * Will Killian <killian@udel.edu>
 * Louis-Noel Pouchet <pouchet@cse.ohio-state.edu>
 * Web address: http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 */

#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
#include <math.h>
#include "jacobi2D.cuh"

/* Problem size. */
#define TSTEPS 5
#define Ni 1000
#define Nj 1100
#define Nk 1200

#define DATATYPE = double
#define RUN_ON_CPU
using namespace std;


void init_array(array A, array B)
{
	int i, j;
	for (i = 0; i < n; i++)
	{
		for (j = 0; j < n; j++)
		{
			A[i][j] = ((DATA_TYPE) i*(j+2) / N);
			B[i][j] = ((DATA_TYPE) i*(j+3) / N);
		}
	}
    return A, B;
}


void runJacobi2DCpu(int tsteps, int n, DATA_TYPE POLYBENCH_2D(A,N,N,n,n), DATA_TYPE POLYBENCH_2D(B,N,N,n,n))
{
	for (int t = 0; t < TSTEPS; t++)
	{
    	for (int i = 1; i < N - 1; i++)
		{
			for (int j = 1; j < N - 1; j++)
			{
	  			B[i][j] = 0.2f * (A[i][j] + A[i][(j-1)] + A[i][(1+j)] + A[(1+i)][j] + A[(i-1)][j]);
			}
		}
		
    	for (int i = 1; i < N-1; i++)
		{
			for (int j = 1; j < N-1; j++)
			{
	  			A[i][j] = B[i][j];
			}
		}
	}
}


__global__ void runJacobiCUDA_kernel1(int n, DATA_TYPE* A, DATA_TYPE* B)
{
	int i = blockIdx.y * blockDim.y + threadIdx.y;
	int j = blockIdx.x * blockDim.x + threadIdx.x;

	if ((i >= 1) && (i < (N-1)) && (j >= 1) && (j < (N-1)))
	{
		B[i*N + j] = 0.2f * (A[i*N + j] + A[i*N + (j-1)] + A[i*N + (1 + j)] + A[(1 + i)*N + j] + A[(i-1)*N + j]);	
	}
}

__global__ void runJacobiCUDA_kernel2(int n, DATA_TYPE* A, DATA_TYPE* B)
{
	int i = blockIdx.y * blockDim.y + threadIdx.y;
	int j = blockIdx.x * blockDim.x + threadIdx.x;
	
	if ((i >= 1) && (i < (N-1)) && (j >= 1) && (j < (N-1)))
	{
		A[i*N + j] = B[i*N + j];
	}
}

void compareResults(int n, DATA_TYPE POLYBENCH_2D(a,N,N,n,n), DATA_TYPE POLYBENCH_2D(a_outputFromGpu,N,N,n,n), DATA_TYPE POLYBENCH_2D(b,N,N,n,n), DATA_TYPE POLYBENCH_2D(b_outputFromGpu,N,N,n,n))
{
	int i, j, fail;
	fail = 0;   

	// Compare output from CPU and GPU
	for (i=0; i<n; i++) 
	{
		for (j=0; j<n; j++) 
		{
			if (percentDiff(a[i][j], a_outputFromGpu[i][j]) > PERCENT_DIFF_ERROR_THRESHOLD) 
			{
				fail++;
			}
        }
	}
  
	for (i=0; i<n; i++) 
	{
       	for (j=0; j<n; j++) 
		{
        		if (percentDiff(b[i][j], b_outputFromGpu[i][j]) > PERCENT_DIFF_ERROR_THRESHOLD) 
			{
        			fail++;
        		}
       	}
	}

	// Print results
	printf("Non-Matching CPU-GPU Outputs Beyond Error Threshold of %4.2f Percent: %d\n", PERCENT_DIFF_ERROR_THRESHOLD, fail);
}

void runCUDA(int tsteps, int n, DATA_TYPE A, DATA_TYPE B, DATA_TYPE A_outputFromGpu, DATA_TYPE B_outputFromGpu)
{
	DATA_TYPE* Agpu;
	DATA_TYPE* Bgpu;

	cudaMalloc(&Agpu, N * N * sizeof(DATA_TYPE));
	cudaMalloc(&Bgpu, N * N * sizeof(DATA_TYPE));
	cudaMemcpy(Agpu, A, N * N * sizeof(DATA_TYPE), cudaMemcpyHostToDevice);
	cudaMemcpy(Bgpu, B, N * N * sizeof(DATA_TYPE), cudaMemcpyHostToDevice);

	dim3 block(DIM_THREAD_BLOCK_X, DIM_THREAD_BLOCK_Y);
	dim3 grid((unsigned int)ceil( ((float)N) / ((float)block.x) ), (unsigned int)ceil( ((float)N) / ((float)block.y) ));
	
	/* Start timer. */

	for (int t = 0; t < TSTEPS; t++)
	{
		runJacobiCUDA_kernel1<<<grid,block>>>(n, Agpu, Bgpu);
		cudaThreadSynchronize();
		runJacobiCUDA_kernel2<<<grid,block>>>(n, Agpu, Bgpu);
		cudaThreadSynchronize();
	}

	/* Stop timer. */
    elapsed =
	
	cudaMemcpy(A_outputFromGpu, Agpu, sizeof(DATA_TYPE) * N * N, cudaMemcpyDeviceToHost);
	cudaMemcpy(B_outputFromGpu, Bgpu, sizeof(DATA_TYPE) * N * N, cudaMemcpyDeviceToHost);

	cudaFree(Agpu);
	cudaFree(Bgpu);

    return elepsed;
}

int main(int argc, char** argv)
{
	/* Retrieve problem size. */
	int n = N;
	int tsteps = TSTEPS;

    DATATYPE A[n][n];
    DATATYPE B[n][n];

	A, B = init_array(int n, array A, array B);

    //if GPU run = true
        //START TIMER
        runCUDA(tsteps, n, A, B, a_outputFromGpu, b_outputFromGpu);
        //end timer
    //if CPU run = true
        //start timer
        runCPU(tsteps, n, POLYBENCH_ARRAY(a), POLYBENCH_ARRAY(b));
        //end timer
	
	compareResults(n, POLYBENCH_ARRAY(a), POLYBENCH_ARRAY(a_outputFromGpu), POLYBENCH_ARRAY(b), POLYBENCH_ARRAY(b_outputFromGpu));


	FREE_ARRAY(a);
	FREE_ARRAY(a_outputFromGpu);
	FREE_ARRAY(b);
	FREE_ARRAY(b_outputFromGpu);

	return 0;
}