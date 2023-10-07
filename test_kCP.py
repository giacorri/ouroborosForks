# kCP TEST

from forks import *
import time

if __name__ == "__main__":
    multiprocessing.freeze_support()
    k = 1
    W = [
            [0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1]
    ]

    for n in range(len(W)):
        w = W[n]
        result, counterExample = kCP(k, W[n])
        print(f"w={W[n]} satisfied {k}-CP? {result}")
        if not result:
            counterExFork = counterExample[0]
            counterExTine1 = counterExample[1]
            counterExTine2 = counterExample[2]
            print(f"\tCounterexample: ", end="")
            counterExFork.print()
            print(f"\tBecause tine {counterExTine1} and {counterExTine2} are such that:")
            # the k-truncation the one with smaller label is not a prefix of the other
            print(f"\t\t{truncate_tine(counterExTine1, k)} is not a prefix of {counterExTine2}")
            counterExFork.plot()