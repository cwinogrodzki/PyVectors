choose kernel equation
	cd kernel/directory
choose problem size
choose BLAS libraary: OneAPI+MKL, MKL only, openBLAS, BLIS(AMD)
	conda activate (BLAS backend)
choose framework (numpy, pytorch, naive C++)
	python3 (kernel_name)_(framework).py args: blas, problem size,
