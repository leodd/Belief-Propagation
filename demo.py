from VertexColoringProblem import print_prob, sumprod, maxprod
import numpy as np


A = np.array(
    [[0, 1, 0],
     [1, 0, 1],
     [0, 1, 0]]
)

w = [0, 1]

# ps = print_prob(A, w, 10, max_prod=True)
# for p in ps:
#     print(p)

print(sumprod(A, w, 10))
