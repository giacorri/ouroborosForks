# hcg TEST

from forks import *
import time
import math

W = [
        [0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1]
]

S = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

with open("test_ecq.txt", "w") as f:
    f.write("ECQ TEST")
    for n in range(len(W)):
        w = W[n]
        f.write(f"\n- w = {W[n]}: ")
        forks = parallel_gen_forks(w)
        f.write(f"{len(forks)} forks")
        for s in S:
            if s > len(w):
                break
            f.write(f"\n\t- s={s}-ecq: ")
            begin = time.time()
            result, counterExample = s_ecq(s, W[n], forks)
            end = time.time()
            f.write(f"{result} in {(end-begin):.2f} seconds")
            if not result:
                f.write(f"\n\t\tCounterexample: ")
                counterExFork = counterExample[0]
                counterExTine = counterExample[1]
                counterExPortion = counterExample[2]
                counterExPath = counterExample[3]
                f.write(f"{counterExFork.get_tines()}")
                f.write(f"\n\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion} is {counterExPath}, which does not contain honest blocks")