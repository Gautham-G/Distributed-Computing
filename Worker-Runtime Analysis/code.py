# Code Execution Instructions
# Execute "./run.sh > out.txt"
# Execute "python make_plots.py"
# out.txt stores output information like dimensions, number of workers, mean time taken


import numpy as np
from mpi4py import MPI
import time
import sys

time_arr = []

def get_partitions(mat, k):
    partitions = []
    val = mat.shape[0]//k
    temp = val
    while(temp<=mat.shape[0]):
        partitions.append(mat[temp-val:temp, :])
        temp+=val
    return partitions

count = 0
num_of_iterations = 20
for i in range(num_of_iterations):
    count+=1

    comm = MPI.COMM_WORLD
    num_of_workers = comm.Get_size()-1
    rank = comm.Get_rank()

    m = int(sys.argv[1])
    n = int(sys.argv[2])

    if(rank==0):
        A = np.random.rand(m,n)
        partitions = get_partitions(A, num_of_workers)

        for i in range(1, num_of_workers+1):
            comm.Send(partitions[i-1], dest=i, tag = i)

        x = np.random.rand(n)
        info = MPI.Status()
        final_result = np.empty(m)
        worker_result = np.empty(int(m/num_of_workers))

    else:
        A_recvd = np.empty((int(m/num_of_workers), n))
        comm.Recv(A_recvd, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        x = np.empty(n)


    if(rank==0):
        t_init = MPI.Wtime()

    comm.Bcast(x, root=0)

    if(rank!=0):
        calc = A_recvd.dot(x)
        comm.Send(calc, dest = 0, tag = rank)

    if(rank==0):
        for i in range(1,num_of_workers+1):
            comm.Recv(worker_result, source=MPI.ANY_SOURCE, tag = MPI.ANY_TAG, status=info)
            source = info.Get_source()
            final_result[(source-1)*worker_result.shape[0] : source*worker_result.shape[0]] = worker_result

        time_taken = MPI.Wtime() - t_init
        time_arr.append(time_taken)

        if(count==num_of_iterations):
            print(m, n, num_of_workers, np.mean(time_arr))

        time.sleep(0.5)
