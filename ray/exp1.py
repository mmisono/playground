import numpy as np
import ray


def main():
    ray.init()

    x = np.ndarray((10, 10))
    x_id = ray.put(x)  # store data in the object store
    y = ray.get(x_id)  # y is the data in the object store
    z = ray.get(x_id)  # same as y

    px, _ = x.__array_interface__['data']
    py, _ = y.__array_interface__['data']
    pz, _ = z.__array_interface__['data']

    print(f"{px:x}, {py:x}, {pz:x}")
    assert(px != py)
    assert(py == pz)


if __name__ == "__main__":
    main()
