from forks2 import *
from time import time
import sys

# w = [0,1,0,1,0,1,0,1,0,1]
w = [0,1,0,1,0,1,0,1,1]
if __name__ == "__main__":
    multiprocessing.freeze_support()
    start = time()
    forks = parallel_gen_forks(w,2)
    end = time()
    print(f"Time to generate forks: {end-start:.2f}")
    # memoryForks = sys.getsizeof(forks)
    # print(f"forks bytes: {memoryForks}")

