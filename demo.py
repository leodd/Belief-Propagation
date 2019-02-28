from VertexColoringProblem import sumprod, maxprod
import numpy as np


A = np.array(
    [[0, 1, 1],
     [1, 0, 1],
     [1, 1, 0]]
)

w = [1, 2, 3]

ps = sumprod(A, w, 10)
for p in ps:
    print(p)
