import os
import time

import torch
import torch.multiprocessing as mp
import torch.nn as nn
import numpy as np
import ray


@ray.remote
def f(i, x):
    x[i][i] = 1


def g(i, x):
    x[i][i] = 1


def main():
    ray.init(num_cpus=8)

    # x is modified
    x = torch.zeros(8, 8)
    x_id = ray.put(x)
    ray.wait([f.remote(i, x_id) for i in range(8)], num_returns=8)
    x = ray.get(x_id)
    print(x)

    print("----")

    # x is not modified
    x = torch.zeros(8, 8)
    workers = [mp.Process(target=g, args=(i, x,)) for i in range(8)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    print(x)

    print("----")

    # x is modified
    x = torch.zeros(8, 8)
    x = x.share_memory_()
    workers = [mp.Process(target=g, args=(i, x,)) for i in range(8)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    print(x)

if __name__ == "__main__":
    main()
