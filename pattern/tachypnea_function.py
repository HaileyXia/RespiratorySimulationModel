"""
Example:Tachypnea
"""
import numpy as np
from tools.awgn import awgn
from tools.breathing import breathing
from tools.randa2b import randa2b


def tachypnea_function(times, n):
    """
    A simulator used to generate Tachypnea Respiratory Pattern based on breathing time and sample rate. Respiratory situation is rapid breathing.
    Common symptom is acute respiratory distress.
    :param times: breathing time
    :param n: sample rate
    :return: array of breathing point
    """
    random_int = np.random.randint(0, times, size=n)
    random_int.sort()

    # delimit n+1 intervals
    list_splice = [np.arange(0, random_int[0] + 1/n, 1/n).tolist()]
    for i in range(0, n - 1):
        list_splice.append(np.arange(random_int[i], random_int[i + 1] + 1/n, 1/n).tolist())
    list_splice.append(np.arange(random_int[n - 1], times + 1/n, 1/n).tolist())

    breath_list = []
    # Respiratory signals are generated in segments
    for i in range(0, n + 1):
        # Tachypnea a is between 0.2 to 0.8, b is between 02.09 to 3.14，c is between -0.05 to +0.05，d is between -0.1
        # to 0.1
        breath_list.append(breathing(list_splice[i], randa2b(0.2, 0.8, 1), randa2b(2.09, 3.14, 1), randa2b(-0.2, 0.2, 1), randa2b(-0.1, 0.1, 1)))

    for i in range(0, n):
        (breath_list[i])[len(breath_list[i]) - 1] = (breath_list[i + 1])[0]

    # save together
    index = 0
    mat = [0] * (times*n)
    for i in range(0, n + 1):
        for j in range(0, len(breath_list[i]) - 2):
            mat[index] = (breath_list[i])[j]
            index = index + 1

    # Add Gaussian noise，SNR = 20
    noise = awgn(mat)
    noise.tolist()
    for i in range(0, len(noise)):
        mat[i] = mat[i] + noise[i]

    return mat
