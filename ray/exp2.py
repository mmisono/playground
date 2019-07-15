import time

import numpy as np
import ray


@ray.remote
def f(x):
    px, _ = x.__array_interface__['data']
    return px


def main():
    ray.init(num_cpus=8)
    x = np.ndarray((1000, 1000))

    # for each remote function call, data is stored in the object store (inefficient)
    s = time.time()
    result = [f.remote(x) for i in range(8)]
    result = ray.get(result)
    e = time.time()
    t1 = e - s
    for r in result:
        print(f"{r:x}")

    print("----")

    # in the following case, every remote function process the same data in the object store
    # This is much faster than the before
    s = time.time()
    x = ray.put(x)
    result = [f.remote(x) for i in range(8)]
    result = ray.get(result)
    e = time.time()
    t2 = e - s
    for r in result:
        print(f"{r:x}")

    print(t1, t2)
    assert(t2 < t1)


if __name__ == "__main__":
    main()
