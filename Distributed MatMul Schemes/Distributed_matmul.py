

# -------------------------------------------------------------------------------------------- #


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

itns = int(1e5)
n = 32
k = 16
t_array = np.linspace(0.10, 0.14, 9)
print("Timescale: ", t_array)

def CDF(k, t):
    return (1 - (1-np.exp(-(k*t-1)))**k)

def worker_time(dim, lmbda):
    return (np.random.exponential(scale = 1/lmbda, size = dim) + (1/lmbda))



# -------------------------------------------------------------------------------------------- #



# Code A 

# Function to create the Generator matrix  

def Hn(n):
    if(n==2):
        return np.array([[1,0],[1,1]])

    val = Hn(n//2)
    size = val.shape[0]
    return np.vstack((np.hstack((val, np.zeros((size,size)))), np.hstack((val, val))))


# Creating the Reed-Muller Matrix and taking the first 16 rows

mat = Hn(n)
sorting_idx = np.argsort(np.sum(mat, 1))
reedMullerMatrix = np.matrix([mat[i] for i in reversed(sorting_idx)])
reedMullerMatrix = reedMullerMatrix[:k, :]

runtime_partA = []

# Simulation of the Reed-Muller coding

for i in range(itns):

    worker_runtimes = worker_time(n, k)
    indices = np.argsort(worker_runtimes)

    valid_cols = k
    while 1:
        if(np.linalg.matrix_rank( reedMullerMatrix[:, indices[:valid_cols] ] ) == k):
            break
        else:
            valid_cols += 1
    runtime_partA.append(worker_runtimes[indices[valid_cols-1]])

prob_partA = []
runtime_partA = np.array(runtime_partA)

for i in range(len(t_array)):
    total_time = np.sum(runtime_partA > t_array[i])
    p = total_time/itns
    prob_partA.append(p)

print("Reed Muller: ", prob_partA)



# -------------------------------------------------------------------------------------------- #



# Code B

runtime_partB = []

# Simulation of the MDS coding

for i in range(itns):

    worker_runtimes = worker_time(n, k)
    worker_runtimes = sorted(worker_runtimes)
    runtime_partB.append(worker_runtimes[k-1])

runtime_partB = np.array(runtime_partB)
prob_partB = []

for i in range(len(t_array)):
    total_time = np.sum(runtime_partB > t_array[i])
    p = total_time/itns
    prob_partB.append(p)

print("MDS: ", prob_partB)



# -------------------------------------------------------------------------------------------- #



# Code C

# Simulation of the Uncoded scheme

simulations = np.linspace(0.1, 0.14, itns)
prob_partC = CDF(n, simulations)




# -------------------------------------------------------------------------------------------- #



# All three plots for comparison

plt.semilogy(t_array, prob_partA, 'o-', label="Reed-Muller Code", color = 'red')
plt.semilogy(t_array, prob_partB, 'o-', label="MDS Code", color = 'blue')
plt.semilogy(simulations, prob_partC, label="Uncoded", color = 'black')

plt.ylabel(" P(Overall runtime > t) ")
plt.xlabel("t")
plt.title("Plot of P(Overall runtime > t) vs t")
plt.legend()
plt.savefig("EP17BTECH11007-08_A1.pdf")
plt.show()



# -------------------------------------------------------------------------------------------- #



