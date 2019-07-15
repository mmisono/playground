import numpy as np
import ray


@ray.remote
def f(x, i):
    # XXX: data in the object store is immutable
    # therefore copy is needed to modify data
    x = np.copy(x)
    x[i] = i


def main():
    ray.init()
    x = np.ndarray((1000, 1000))

    x = ray.put(x)
    result = [f.remote(x, i) for i in range(10)]
    ray.get(result)


if __name__ == "__main__":
    main()
