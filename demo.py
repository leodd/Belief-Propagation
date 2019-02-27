from VertexColoringProblem import maxprod
import numpy as np


A = np.array(
    [[0, 1, 1],
     [1, 0, 1],
     [1, 1, 0]]
)

w = [1, 4, 2]

print(maxprod(A, w, 10))
