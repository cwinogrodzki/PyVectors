#!/bin/bash

#framework, kernel, iter, device
KERNEL=$1
FRAMEWORK=$2
DEVICE=$3
N=$4
ITER=$5

eval "$(conda shell.bash hook)"

if [ "$DEVICE" = "cuda" ]; then
	#salloc -p shared-devkit-40g
        module load cuda
        module load miniconda3
        source activate arm-nvidia
elif [ "$DEVICE" = "rocm" ]; then
	#salloc -p shared-gpu-amd-mi100
	#module load rocm
        #module load miniconda3
        source activate rocm-mkl
elif [ "$DEVICE" = "intel" ]; then
        # salloc -p skylake-gold
        # module load oneAPI
        conda activate idp
elif [ "$DEVICE" = "amdcpu" ]; then
	#salloc -p shared-gpu-amd-mi100
        conda activate amd-cpu
elif [ "$DEVICE" = "arm" ]; then
	#salloc -p shared-hopper-devkit
        module load miniconda3
        source activate arm-nvidia
elif [ "$DEVICE" = "mps" ]; then
        conda activate silicon
fi

# if  [ "$ENV" = "idp" ]; then
# 	conda activate idp
# elif [ "$ENV" = "amd-cpu" ]; then
# 	conda activate amd-cpu
# elif [ "$ENV" = "arm" ]; then
# 	conda activate arm
# elif [ "$ENV" = "silicon" ]; then
# 	conda activate silicon
# elif [ "$ENV" = "openblas" ]; then
# 	conda activate openblas
# else [ "$ENV" = "base" ]
# 	conda activate base-pkgs
# fi

echo "conda env: $CONDA_DEFAULT_ENV"
echo "kernel/framework: $KERNEL $FRAMEWORK"
echo "problem size: $N"
echo "iterations: $ITER"

print_progress_bar() {
    local percent=$(( ($1 * 100) / $2 ))
    local done_chars=$(( ($percent * 3) / 10 ))
    local left_chars=$(( 30 - $done_chars ))

    printf "\rProgress: [%-30s] %d%%" \
           $(printf '#%.0s' $(seq $done_chars)) \
           $percent
}

results=()
for (( i=1; i <= $ITER; ++i ))
do
	result=$(python3 $KERNEL/$KERNEL.py $FRAMEWORK $ITER $DEVICE $N)

        if [ $? -eq 0 ]; then
                results+=($result)
        else
                echo "program failed on run $i."
                #results+=("N/A")
        fi

        #if (( $i % 10 == 0 )); then
	       print_progress_bar $i $ITER
        #fi
done

printf '\nkernel time per iteration (ms)\n'
printf '%s\n' "${results[@]}"

echo ${results[@]} | awk 'NF {sum=0;for (i=1;i<=NF;i++)sum+=$i; print "average: " sum / NF; }'

# (IFS=$'\n'; echo "${results[*]}")


