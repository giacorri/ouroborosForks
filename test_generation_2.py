# GENERATION TEST
# 2 maximum adversarial block per slot
# parallel generation

from forks import *
import time

PLOT = True

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    W = [
            [0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1]
    ]

    times = []
    nForks = []

    # parallel generation, 2 maximum adversarial block per slot
    for w in W:
        t = time.time()
        forks = parallel_gen_forks(w, 2)
        times.append(time.time() - t)
        nForks.append(len(forks))
        if PLOT:
            for i in range(15):
                forks[i].print()
                forks[i].plot(quick=True)

    with open("result_generation_2.txt", "w") as f:
        f.write("GENERATION TEST: 2 maximum adversarial block per slot\n")
        for i in range(len(W)):
            f.write("- w = " + str(W[i]) + "\n")
            f.write(f"\t{nForks[i]} forks\n")
            f.write(f"\tmulti-core generation in {times[i]:.2f} seconds\n")