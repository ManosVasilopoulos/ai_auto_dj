import numpy as np

out = np.array([1., 2., 3., 4., 5., 6., 7., 8., 9., 10.])
for i in range(out.size):
    for j in range(-3, 4):
        if 0 <= i + j < out.size:
            out[i + j] = 1.0 / (1.0 + abs(j))
            print('i:', i, 'j:', j, 'i + j:', i + j, 'value:', 1.0 / (1.0 + abs(j)), out)

print(out)
