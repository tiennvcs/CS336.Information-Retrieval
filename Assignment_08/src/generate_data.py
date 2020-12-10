import numpy as np
import os


def generate(size):
    data = np.random.random_integers(low=int(-1e6), high=int(1e6), size=size)
    with open('../data/{}.txt'.format(size), 'w') as f:
        np.savetxt(f, data)


if __name__ == '__main__':

    # set random seed
    np.random.seed(seed=18521489)
    size = int(1e6)
    generate(size)