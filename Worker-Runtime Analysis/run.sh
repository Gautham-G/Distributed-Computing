# Code Execution Instructions
# Execute "./run.sh > out.txt"
# Execute "python make_plots.py"
# out.txt stores output information like dimensions, number of workers, mean time taken

module load mpi/openmpi-x86_64
export OPENBLAS_NUM_THREADS=1

echo "(m, n, Workers, Mean Time)"
mpiexec -n 2 python code.py 9000 9000
mpiexec -n 3 python code.py 9000 9000
mpiexec -n 5 python code.py 9000 9000
mpiexec -n 7 python code.py 9000 9000

mpiexec -n 2 python code.py 9000 4500
mpiexec -n 3 python code.py 9000 4500
mpiexec -n 5 python code.py 9000 4500
mpiexec -n 7 python code.py 9000 4500