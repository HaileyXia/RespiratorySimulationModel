import numpy as np


def randa2b(a, b, n):
    """
    Get array of random numbers between a and b
    :param a: minimum number
    :param b: maximum number
    :param n: number of random numbers
    :return:
    """
    output = np.random.uniform(a, b, n)
    return output
