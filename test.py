# comprehensive test
from forks import *
import time
import math
from multiprocessing import freeze_support

PLOT = True

W = [ [0, 1, 0, 1], [1, 0, 1, 1, 0], [0, 1, 0, 1, 1, 0], [1, 0, 1, 1, 0, 1, 0], [1, 0, 1, 1, 0, 1, 0, 1]]
K = [2, 4, 7]
S = [2, 5, 8]
TAU = [1/2, 1/3, 1/4]

generationTimes = []
lens = []
cpTimes = []
hcgTimes = []
ecqTimes = []
forkableTimes = []

generationTimes2 = []
lens2 = []
cpTimes2 = []
hcgTimes2 = []
ecqTimes2 = []
forkableTimes2 = []

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
            generationTimes.append(end - start)
            print(f"- w = {w}: ", end="")
            f.write(f"generated {len(forks)} forks in {end - start:.2f} seconds")
            print(f"generated {len(forks)} forks in {end - start:.2f} seconds")
            lens.append(len(forks))
            # k-cp
            f.write(f"\n\tCP")
            wCpTimes = []
            for k in K:
                start = time.time()
                result, counterExample = k_cp(k, w, forks)
                end = time.time()
                wCpTimes.append(end - start)
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
                    if PLOT:
                        counterExample[0].plot()
            cpTimes.append(sum(wCpTimes)/len(wCpTimes))

            # (tau,s)-hcg
            f.write(f"\n\tHCG")
            wHcgTimes = []
            for tau in TAU:
                for s in S:
                    start = time.time()
                    result, counterExample = tau_s_hcg(tau, s, w, forks)
                    end = time.time()
                    wHcgTimes.append(end - start)
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
                        f.write(f"\n\t\tBecause the path after node '{counterExNode}' in tine {counterExTine}\n\t\tis {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f} nodes")
                        print(f"\t\tBecause the path after node '{counterExNode}' in tine {counterExTine}\n\t\tis {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f} nodes")
                        if PLOT:
                            counterExFork.plot()
            hcgTimes.append(sum(wHcgTimes)/len(wHcgTimes))
            # s-ecq
            f.write(f"\n\tECQ")
            wEcqTimes = []
            for s in S:
                start = time.time()
                result, counterExample = s_ecq(s, w, forks)
                end = time.time()
                wEcqTimes.append(end - start)
                f.write(f"\n\t- {s}-ecq? {result}, in {end - start:.2f} seconds")
                print(f"\t- {s}-ecq? {result}, in {end - start:.2f} seconds")
                if not result:
                    counterExFork = counterExample[0]
                    counterExTine = counterExample[1]
                    counterExPortion = counterExample[2]
                    counterExPath = counterExample[3]
                    f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                    print(f"\t\tCounterexample: {counterExFork.get_tines()}")
                    f.write(f"\n\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion}\n\t\tis {counterExPath}, which does not contain honest blocks")
                    print(f"\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion}\n\t\tis {counterExPath}, which does not contain honest blocks")
                    if PLOT:
                        counterExFork.plot()
            ecqTimes.append(sum(wEcqTimes)/len(wEcqTimes))
            # forkable
            f.write(f"\n\tFORKABLE")
            start = time.time()
            result, example = forkable(w, forks)
            end = time.time()
            forkableTimes.append(end - start)
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
                if PLOT:
                        flatFork.plot()

        f.write("\nTESTs, 2 maximum block per slot")
        print("TESTs, 2 maximum block per slot")
        # for i in range(len(W)-1):
        for i in range(len(W)-1):
            w = W[i]
            f.write(f"\n- w = {w}, ")
            # generation
            start = time.time()
            forks = parallel_gen_forks(w, 2)
            end = time.time()
            generationTimes2.append(end - start)
            print(f"- w = {w}: ", end="")
            f.write(f"generated {len(forks)} forks in {end - start:.2f} seconds")
            print(f"generated {len(forks)} forks in {end - start:.2f} seconds")
            lens2.append(len(forks))
            # k-cp
            f.write(f"\n\tCP")
            wCpTimes = []
            for k in K:
                start = time.time()
                result, counterExample = k_cp(k, w, forks)
                end = time.time()
                wCpTimes.append(end - start)
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
                    if PLOT:
                        counterExample[0].plot()
            cpTimes2.append(sum(wCpTimes)/len(wCpTimes))
            # (tau,s)-hcg
            f.write(f"\n\tHCG")
            wHcgTimes = []
            for tau in TAU:
                for s in S:
                    start = time.time()
                    result, counterExample = tau_s_hcg(tau, s, w, forks)
                    end = time.time()
                    wHcgTimes.append(end - start)
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
                        f.write(f"\n\t\tBecause the path after node '{counterExNode}' in tine {counterExTine}\n\t\tis {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f} nodes")
                        print(f"\t\tBecause the path after node '{counterExNode}' in tine {counterExTine}\n\t\tis {counterExPath} which contains {length_tine(counterExTine[counterExNodeIndex:])} < {tau*s:.1f} nodes")
                        if PLOT:
                            counterExFork.plot()
            hcgTimes2.append(sum(wHcgTimes)/len(wHcgTimes))
            # s-ecq
            f.write(f"\n\tECQ")
            wEcqTimes = []
            for s in S:
                start = time.time()
                result, counterExample = s_ecq(s, w, forks)
                end = time.time()
                wEcqTimes.append(end - start)
                f.write(f"\n\t- {s}-ecq? {result}, in {end - start:.2f} seconds")
                print(f"\t- {s}-ecq? {result}, in {end - start:.2f} seconds")
                if not result:
                    counterExFork = counterExample[0]
                    counterExTine = counterExample[1]
                    counterExPortion = counterExample[2]
                    counterExPath = counterExample[3]
                    f.write(f"\n\t\tCounterexample: {counterExFork.get_tines()}")
                    print(f"\t\tCounterexample: {counterExFork.get_tines()}")
                    f.write(f"\n\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion}\n\t\tis {counterExPath}, which does not contain honest blocks")
                    print(f"\t\tBecause the portion of the tine {counterExTine} spanning the {s} slots {counterExPortion}\n\t\tis {counterExPath}, which does not contain honest blocks")
                    if PLOT:
                        counterExFork.plot()
            ecqTimes2.append(sum(wEcqTimes)/len(wEcqTimes))
            # forkable
            f.write(f"\n\tFORKABLE")
            start = time.time()
            result, example = forkable(w, forks)
            end = time.time()
            forkableTimes2.append(end - start)
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
                if PLOT:
                    flatFork.plot()            

    lens2.append("NA")
    generationTimes2.append("NA")
    cpTimes2.append("NA")
    hcgTimes2.append("NA")
    ecqTimes2.append("NA")
    forkableTimes2.append("NA")

    with open("test_results.txt", "w") as f:
            f.write(f"\nlen(w) & len(forks)1 & gen1 & cp1 & hcg1 & ecq1 & forkable1 & len(forks)2 & gen2 & cp2 & hcg2 & ecq2 & forkable2\\\\ \\hline")
            for n in range(len(W)):                    
                # in the last row, handle NA
                if n == len(W)-1:
                    f.write(f"\n{len(W[n])} & {lens[n]} & {generationTimes[n]:.2f} & {cpTimes[n]:.2f} & {hcgTimes[n]:.2f} & {ecqTimes[n]:.2f} & {forkableTimes[n]:.2f} & {lens2[n]} & {generationTimes2[n]} & {cpTimes2[n]} & {hcgTimes2[n]} & {ecqTimes2[n]} & {forkableTimes2[n]} \\\\ \hline")
                else:
                    f.write(f"\n{len(W[n])} & {lens[n]} & {generationTimes[n]:.2f} & {cpTimes[n]:.2f} & {hcgTimes[n]:.2f} & {ecqTimes[n]:.2f} & {forkableTimes[n]:.2f} & {lens2[n]} & {generationTimes2[n]:.2f} & {cpTimes2[n]:.2f} & {hcgTimes2[n]:.2f} & {ecqTimes2[n]:.2f} & {forkableTimes2[n]:.2f} \\\\ \hline")