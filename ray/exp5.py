import os
import time

import torch
import numpy as np
import ray


@ray.remote
def f(i, x):
    x[i][i] = 1


def g(x):
    x_id = ray.put(x)
    ray.wait([f.remote(i, x_id) for i in range(8)], num_returns=8)
    y = ray.get(x_id)
    print(y)


def main():
    ray.init(num_cpus=8)

    # data in the object store is modified by the remote!
    x = torch.zeros(8, 8)
    g(x)

    # data in the object store is not modified by the remote
    x = [[0 for i in range(8)] for j in range(8)]
    g(x)

    # ValueError: assignment destination is read-only
    x = np.zeros((8, 8))
    g(x)


if __name__ == "__main__":
    main()
