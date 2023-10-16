from forks import *
from multiprocessing import freeze_support
import random
import numpy

def findFlats(forks):
    flats = []
    for fork in forks:
        isFlat, indexes = fork.is_flat()
        if isFlat:
            flats.append( [fork, indexes] )
            print(f"appending {fork.get_tines()}")
    return flats

def myPrint(text, write=True):
    if write:
        with open("prop3proof.txt", "a") as f:
            f.write(text)
    else:
        print(text, end="")

if __name__ == "__main__":
    freeze_support()

    flats = []
    while len(flats) == 0:
        w = []
        for i in range(6):
            w.append(numpy.random.choice([0, 1], p=[0.475, 0.525]))
        # if number of 1 is too much, then skip
        if sum(w) > 4:
            continue
        forks = parallel_gen_forks(w, 2)
        myPrint(f"- {w}\n")
        flats = findFlats(forks)
        for flat in flats:
            flatFork = flat[0]
            indexes = flat[1]
            index1 = indexes[0]
            index2 = indexes[1]
            tine1 = flatFork.get_tines()[index1]
            tine2 = flatFork.get_tines()[index2]
            closure = flatFork.closure()
            tine1inClosure = flatFork.prefix_of_tine_in_closure(tine1)
            tine2inClosure = flatFork.prefix_of_tine_in_closure(tine2)
            tHat = closure.get_maximal_tines()[0]
            pairs = [[flatFork, closure]]
            plot_couple_of_forks(pairs)
            myPrint(f"\n\t- flatFork = {flatFork.get_tines()}")
            myPrint(f"\n\t\ttine1 = {tine1}, tine2 = {tine2}")
            myPrint(f"\n\t\t\tclosure = {closure.get_tines()}")
            myPrint(f"\n\t\t\ttine1 in closure = {tine1inClosure}")
            myPrint(f"\n\t\t\ttine2 in closure = {tine2inClosure}")
            myPrint(f"\n\t\t\ttHat = {tHat}")
            myPrint(f"\n\t\t\treach of tine1inClosure = {closure.reach(tine1inClosure)}")
            myPrint(f"\n\t\t\treach of tine2inClosure = {closure.reach(tine2inClosure)}")