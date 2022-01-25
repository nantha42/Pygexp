import time
import numpy as np


x = np.random.random((100,100))


X = x.tolist()
Y = x.tolist()

result = (x*0).tolist()


st = time.time()

# iterate through rows of X
for i in range(len(X)):
   # iterate through columns of Y
   for j in range(len(Y[0])):
       # iterate through rows of Y
       for k in range(len(Y)):
           result[i][j] += X[i][k] * Y[k][j]
cal = time.time()-st
print(np.array(result).shape)
print(np.array(result)[:2,:2])
print("Hard: ",cal)



st = time.time()
g =  x.dot(x)
print(g.shape)
print(g[:2,:2])
print("Numpy :",time.time()-st)
