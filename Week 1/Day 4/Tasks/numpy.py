#numpy basics
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(arr)
print(type(arr))            # numpy.ndarray
print(arr.shape)            # (5,)
#Arrays
a = np.array([1, 2, 3])
b = np.zeros(5)              # [0. 0. 0. 0. 0.]
c = np.ones((2, 3))          # 2x3 array of ones
d = np.arange(0, 10, 2)      # [0 2 4 6 8]
e = np.array([[1, 2], [3, 4]])  # 2D array (matrix)
#Vectorized Operations
#NumPy lets you apply operations to entire arrays at once — no loop needed.
a = np.array([1, 2, 3, 4])
print(a + 10)        # [11 12 13 14]  -- adds to every element
print(a * 2)          # [2 4 6 8]
print(a ** 2)          # [1 4 9 16]

b = np.array([10, 20, 30, 40])
print(a + b)          # [11 22 33 44]  -- element-wise addition

#Basic Numerical Operations
arr = np.array([4, 8, 15, 16, 23, 42])
print(arr.sum())      # total
print(arr.mean())     # average
print(arr.max())      # largest
print(arr.min())      # smallest
print(arr.std())      # standard deviation
print(np.sort(arr))   # sorted copy