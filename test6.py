import numpy as np
import math

angle = 90
rad = math.radians(angle % 360)
print(rad)
print(math.cos(rad))
print(math.sin(rad))


sizes = [1,3,5]
broski = [x+y for x, y in [(2,3),(5,3),(2,2)]]
print(broski)

print(np.exp(1))
print(np.exp(0))
print(np.exp([1,0]))

weights = [np.ones((y, x)) for y, x in zip(sizes[:-1], sizes[1:])]
biases = [np.random.randn(1, x) for x in sizes[1:]]
print(biases[0])
print(biases[1])
print(weights[0])
print(weights[0].shape)
print(weights[1])
print(weights[1].shape)
print(weights)
print(np.matmul(weights[0], weights[1]))