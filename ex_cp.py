# example from the Ouroboros paper
from forks import *
w = [0, 1, 0, 1, 0, 0, 1, 1, 0]
result, counterExample = k_cp(2, w)
print(result)
counterExample[0].plot()