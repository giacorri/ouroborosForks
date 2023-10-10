# comprehensive test
from forks import *
import time
import math
from multiprocessing import freeze_support

W = [[1, 0, 1, 1, 0], [1, 0, 1, 1, 0, 1, 0], [1, 0, 1, 1, 0, 1, 0, 1], [1, 0, 1, 1, 0, 1, 0, 1, 0]]
K = [2, 4, 7]
S = [2, 5, 8]
TAU = [1/2, 1/3, 1/4]

if __name__ == '__main__':
    freeze_support()
    with open("test.txt", "w") as f:
        f.write("TESTs, 1 maximum block per slot")
        print("TESTs, 1 maximum block per slot")
        for w in W:
            f.write(f"\n- w = {w}, ")
            # generation
            start = time.time()
            forks = parallel_gen_forks(w)
            end = time.time()
            print(f"- w = {w}: ", end="")
            f.write(f"generated {len(forks)} forks in {end - start:.2f} seconds")
            print(f"generated {len(forks)} forks in {end - start:.2f} seconds")
            # k-cp
            f.write(f"\n\tCP")
            for k in K:
                start = time.time()
                result, counterExample = k_cp(k, w, forks)
                end = time.time()
                f.write(f"\n\t- {k}-cp? {result}, in {end - start:.2f} seconds")
                print(f"\t- {k}-cp? {result}, in {end - start:.2f} seconds")
                if not result:
                    counterExFork = counterExample[0]
                    counterExTine1 = counterExample[1]
                    counterExTine2 = counterExample[2]
                    f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                    print(f"\t\tCounterexample: {counterExFork.get_tines()}")
                    f.write(f"\n\t\tBecause tine {counterExTine1} and {counterExTine2} are such that:")
                    print(f"\t\tBecause tine {counterExTine1} and {counterExTine2} are such that:")
                    f.write(f"\n\t\t{truncate_tine(counterExTine1, k)} is not a prefix of {counterExTine2}")
                    print(f"\t\t{truncate_tine(counterExTine1, k)} is not a prefix of {counterExTine2}")
                    counterExample[0].plot(True)
            # (tau,s)-hcg
            f.write(f"\n\tHCG")
            for tau in TAU:
                for s in S:
                    start = time.time()
                    result, counterExample = tau_s_hcg(tau, s, w, forks)
                    end = time.time()
                    f.write(f"\n\t- ({tau:.2f},{s})-hcg? {result}, in {end - start:.2f} seconds")
                    print(f"\t- ({tau:.2f},{s})-hcg? {result}, in {end - start:.2f} seconds")
                    if not result:
                        counterExFork = counterExample[0]
                        counterExTine = counterExample[1]
                        counterExNode = counterExample[2]
                        counterExPath = counterExample[3]
                        counterExNodeIndex = counterExTine.index(counterExNode)
                        f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                        print(f"\t\tCounterexample: {counterExFork.get_tines()}")
                        f.write(f"\n\t\tBecause the path after node '{counterExNode}' in tine {counterExTine} is {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f} nodes")
                        print(f"\t\tBecause the path after node '{counterExNode}' in tine {counterExTine} is {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f} nodes")
                        counterExFork.plot(True)
            # s-ecq
            f.write(f"\n\tECQ")
            for s in S:
                start = time.time()
                result, counterExample = s_ecq(s, w, forks)
                end = time.time()
                f.write(f"\n\t- {s}-ecq? {result}, in {end - start:.2f} seconds")
                print(f"\t- {s}-ecq? {result}, in {end - start:.2f} seconds")
                if not result:
                    counterExFork = counterExample[0]
                    counterExTine = counterExample[1]
                    counterExPortion = counterExample[2]
                    counterExPath = counterExample[3]
                    f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                    print(f"\t\tCounterexample: {counterExFork.get_tines()}")
                    f.write(f"\n\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion} is {counterExPath}, which does not contain honest blocks")
                    print(f"\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion} is {counterExPath}, which does not contain honest blocks")
                    counterExFork.plot(True)
            # forkable
            f.write(f"\n\tFORKABLE")
            start = time.time()
            result, example = forkable(w, forks)
            end = time.time()   
            f.write(f"\n\t- forkable? {result}, in {end - start:.2f} seconds")
            print(f"\t- forkable? {result}, in {end - start:.2f} seconds")
            if result:
                flatFork = example[0]
                index1 = example[1]
                index2 = example[2]
                f.write(f"\n\t\tFlat fork: {flatFork.get_tines()}")
                print(f"\t\tFlat fork: {flatFork.get_tines()}")
                tines = flatFork.get_tines()
                tine1 = tines[index1]
                tine2 = tines[index2]
                f.write(f"\n\t\tBecause the edge-disjoint tines {tine1} and {tine2} have maximum length")
                print(f"\t\tBecause the edge-disjoint tines {tine1} and {tine2} have maximum length")
                flatFork.plot(True)



        f.write("\nTESTs, 2 maximum block per slot")
        print("TESTs, 2 maximum block per slot")
        for w in range(3):
            f.write(f"\n- w = {w}, ")
            # generation
            start = time.time()
            forks = parallel_gen_forks(w, 2)
            end = time.time()
            print(f"- w = {w}: ", end="")
            f.write(f"generated {len(forks)} forks in {end - start:.2f} seconds")
            print(f"generated {len(forks)} forks in {end - start:.2f} seconds")
            # k-cp
            f.write(f"\n\tCP")
            for k in K:
                start = time.time()
                result, counterExample = k_cp(k, w, forks)
                end = time.time()
                f.write(f"\n\t- {k}-cp? {result}, in {end - start:.2f} seconds")
                print(f"\t- {k}-cp? {result}, in {end - start:.2f} seconds")
                if not result:
                    counterExFork = counterExample[0]
                    counterExTine1 = counterExample[1]
                    counterExTine2 = counterExample[2]
                    f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                    print(f"\t\tCounterexample: {counterExFork.get_tines()}")
                    f.write(f"\n\t\tBecause tine {counterExTine1} and {counterExTine2} are such that:")
                    print(f"\t\tBecause tine {counterExTine1} and {counterExTine2} are such that:")
                    f.write(f"\n\t\t{truncate_tine(counterExTine1, k)} is not a prefix of {counterExTine2}")
                    print(f"\t\t{truncate_tine(counterExTine1, k)} is not a prefix of {counterExTine2}")
                    counterExample[0].plot(True)
            # (tau,s)-hcg
            f.write(f"\n\tHCG")
            for tau in TAU:
                for s in S:
                    start = time.time()
                    result, counterExample = tau_s_hcg(tau, s, w, forks)
                    end = time.time()
                    f.write(f"\n\t- ({tau:.2f},{s})-hcg? {result}, in {end - start:.2f} seconds")
                    print(f"\t- ({tau:.2f},{s})-hcg? {result}, in {end - start:.2f} seconds")
                    if not result:
                        counterExFork = counterExample[0]
                        counterExTine = counterExample[1]
                        counterExNode = counterExample[2]
                        counterExPath = counterExample[3]
                        counterExNodeIndex = counterExTine.index(counterExNode)
                        f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                        print(f"\t\tCounterexample: {counterExFork.get_tines()}")
                        f.write(f"\n\t\tBecause the path after node '{counterExNode}' in tine {counterExTine} is {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f} nodes")
                        print(f"\t\tBecause the path after node '{counterExNode}' in tine {counterExTine} is {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f} nodes")
                        counterExFork.plot(True)
            # s-ecq
            f.write(f"\n\tECQ")
            for s in S:
                start = time.time()
                result, counterExample = s_ecq(s, w, forks)
                end = time.time()
                f.write(f"\n\t- {s}-ecq? {result}, in {end - start:.2f} seconds")
                print(f"\t- {s}-ecq? {result}, in {end - start:.2f} seconds")
                if not result:
                    counterExFork = counterExample[0]
                    counterExTine = counterExample[1]
                    counterExPortion = counterExample[2]
                    counterExPath = counterExample[3]
                    f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                    print(f"\t\tCounterexample: {counterExFork.get_tines()}")
                    f.write(f"\n\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion} is {counterExPath}, which does not contain honest blocks")
                    print(f"\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion} is {counterExPath}, which does not contain honest blocks")
                    counterExFork.plot(True)
            # forkable
            f.write(f"\n\tFORKABLE")
            start = time.time()
            result, example = forkable(w, forks)
            end = time.time()
            f.write(f"\n\t- forkable? {result}, in {end - start:.2f} seconds")
            print(f"\t- forkable? {result}, in {end - start:.2f} seconds")
            if result:
                flatFork = example[0]
                index1 = example[1]
                index2 = example[2]
                f.write(f"\n\t\tFlat fork: {flatFork.get_tines()}")
                print(f"\t\tFlat fork: {flatFork.get_tines()}")
                tines = flatFork.get_tines()
                tine1 = tines[index1]
                tine2 = tines[index2]
                f.write(f"\n\t\tBecause the edge-disjoint tines {tine1} and {tine2} have maximum length")
                print(f"\t\tBecause the edge-disjoint tines {tine1} and {tine2} have maximum length")
                flatFork.plot(True)