#NumPy Arrays & Shapes
import numpyExercise as np
a = np.array([1, 2, 3, 4])
print(a.shape)          # (4,)
b = np.array([[1,2,3],[4,5,6]])
print(b.shape)           # (2, 3) -> 2 rows, 3 columns

#indexing
b = np.array([[1,2,3],[4,5,6]])
print(b[0])       # first row: [1 2 3]
print(b[1, 2])    # row 1, col 2: 6
print(b[:, 0])    # all rows, col 0: [1 4]
#BROADCASTING
a = np.array([1, 2, 3])
print(a + 10)          # [11 12 13] 10 is "broadcast" to every element
b = np.array([[1,2,3],[4,5,6]])
print(b + a)             # a is added to every row
#MATHEMATICAL  Operaions
a = np.array([1, 2, 3, 4])
print(a.sum(), a.mean(), a.std(), a.max(), a.min())
print(np.sqrt(a))

