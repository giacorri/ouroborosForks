# GENERATION TEST
# 1 maximum adversarial block per slot
# comparision between normal generation and parallel generation

from forks import *
import time

PLOT = True

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    W = [
            [0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 1, 1],
            [0, 1, 0, 1, 0, 1, 1, 1, 0]
    ]

    times1 = []
    nForks1 = []
    # normal generation (1 core)
    for w in W:

        t = time.time()    
        forks = gen_forks(w)
        times1.append(time.time() - t)
        nForks1.append(len(forks))
        if PLOT:
            for i in range(15):
                forks[i].print()
                forks[i].plot(quick=True)

    times2 = []
    nForks2 = []
    # parallel generation, 1 maximum adversarial block per slot
    for w in W:
        t = time.time()
        forks = parallel_gen_forks(w)
        times2.append(time.time() - t)
        nForks2.append(len(forks))
        if PLOT:
            for i in range(15):
                forks[i].print()
                forks[i].plot(quick=True)

    with open("test_generation_1.txt", "w") as f:
        f.write("GENERATION TEST: 1 maximum adversarial block per slot\n")
        for i in range(len(W)):
            f.write("- w = " + str(W[i]) + "\n")
            if nForks1[i] != nForks2[i]:
                f.write("\tERROR: different number of forks\n")
            else:
                f.write(f"\t{nForks1[i]} forks\n")
            f.write(f"\tsingle-core generation in {times1[i]:.2f} seconds\n")
            f.write(f"\t multi-core generation in {times2[i]:.2f} seconds\n")