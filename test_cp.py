# cp TEST

from forks import *
import time

# if __name__ == "__main__":
#     multiprocessing.freeze_support()
K = [1, 2, 3, 4]
W = [
        [0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1]
]
with open("test_cp.txt", "w") as f:
    f.write("CP TEST")
    for n in range(len(W)):
        w = W[n]
        f.write(f"\n- w = {W[n]}: ")
        forks = parallel_gen_forks(w)
        f.write(f"{len(forks)} forks")
        for k in K:
            f.write(f"\n\t- {k}-cp: ")
            begin = time.time()
            result, counterExample = k_cp(k, W[n], forks)
            end = time.time()
            f.write(f"{result} in {(end-begin):.2f} seconds")
            if not result:
                counterExFork = counterExample[0]
                counterExTine1 = counterExample[1]
                counterExTine2 = counterExample[2]
                f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                f.write(f"\n\t\tBecause tine {counterExTine1} and {counterExTine2} are such that:")
                f.write(f"\n\t\t{truncate_tine(counterExTine1, k)} is not a prefix of {counterExTine2}")
                # counterExFork.plot()