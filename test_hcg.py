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
TAU = [1/2, 1/3, 1/4, 1/5, 1/6]
S = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

with open("test_hcg.txt", "w") as f:
    f.write("HCG TEST")
    for n in range(len(W)):
        w = W[n]
        f.write(f"\n- w = {W[n]}: ")
        forks = parallel_gen_forks(w)
        f.write(f"{len(forks)} forks")
        for tau in TAU:
            for s in S:
                f.write(f"\n\t- (tau={tau:.2f}, s={s})-hcg: ")
                begin = time.time()
                result, counterExample = tau_s_hcg(tau, s, W[n], forks)
                end = time.time()
                f.write(f"{result} in {(end-begin):.2f} seconds")
                if not result:
                    counterExFork = counterExample[0]
                    counterExTine = counterExample[1]
                    counterExNode = counterExample[2]
                    counterExPath = counterExample[3]
                    counterExNodeIndex = counterExTine.index(counterExNode)
                    f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                    f.write(f"\n\t\tBecause the path after node '{counterExNode}' in tine {counterExTine} is {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f}nodes")
                    counterExFork.plot(True)