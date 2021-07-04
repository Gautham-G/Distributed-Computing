import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

df = pd.read_csv('out.txt')



df['(m'] =  df['(m'].apply(lambda x: x.replace('(','').replace(')','')) 
df[' Mean Time)'] =  df[' Mean Time)'].apply(lambda x: x.replace('(','').replace(')',''))
df.columns = ['m', 'n', 'Workers', 'Mean Time']


A = np.array(df).astype(np.float)
L1 = []
L2 = []
for i in range (len(A)):
    if A[i][0] == 9000 and A[i][1] == 9000:
        L1.append(A[i][:])
    else:
        L2.append(A[i][:])
La = pd.DataFrame(L1, columns = ['m', 'n', 'Workers', 'Mean Time'])
Lb = pd.DataFrame(L2, columns = ['m', 'n', 'Workers', 'Mean Time'])



plt.scatter(La['Workers'], La['Mean Time'])
plt.plot(La['Workers'], La['Mean Time'], label = 'mxn = 9000x9000')
plt.scatter(Lb['Workers'], Lb['Mean Time'])
plt.plot(Lb['Workers'], Lb['Mean Time'], label = 'mxn = 9000x4500')
plt.xlabel('Workers')
plt.ylabel('Mean Time')
plt.title('Number of Workers vs Mean Computation Time')
plt.legend()
plt.savefig('plot.pdf')
# plt.show()

