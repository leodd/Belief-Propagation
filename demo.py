from VertexColoringProblem import print_prob, sumprod, maxprod
import numpy as np


A = np.array(
    [[0, 1, 0],
     [1, 0, 1],
     [0, 1, 0]]
)

w = [1, 2]

print(sumprod(A, w, 10))
print(maxprod(A, w, 10))

# you can even print the distribution of each variables
ps = print_prob(A, w, 10, max_prod=False)
for p in ps:
    print(p)
