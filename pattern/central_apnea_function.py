"""
Example:Central Apnea
"""
import numpy as np
from tools.awgn import awgn
from tools.breathing import breathing
from tools.randa2b import randa2b


def central_apnea_function(times, n):
    """
    A simulator used to generate Central-Apnea Respiratory Pattern based on the breathing time and sample rate.
    Respiratory situation is normal breathing, then choking. Common symptom is primary hypoventilation syndrome.
    :param times: breathing time
    :param n: sample rate
    :return: array of breathing point
    """
    for t in range(0, 1):
        # Randomly generate N breakpoints within 0 to first 2/3 part of integer seconds, and sort
        n = n//2
        random_int = np.random.randint(t * times, (t + 1) * times - (times//3), size=n)
        random_int.sort()
        # delimit n+2 intervals
        list_splice = [np.arange(t * times, random_int[0] + 1/n, 1/n).tolist()]
        for i in range(0, n - 1):
            list_splice.append(np.arange(random_int[i], random_int[i + 1] + 1/n, 1/n).tolist())
        # A random breakpoint is generated between the last breakpoint and 5/6 part of seconds, resulting in suffocation
        rand_apnea = np.random.randint(random_int[n - 1], (t + 1) * times - (times//3), size=1)
        list_splice.append(np.arange(random_int[n - 1], rand_apnea + 1/n, 1/n).tolist())
        list_splice.append(np.arange(rand_apnea, (t + 1) * times + 1/n, 1/n).tolist())

        breath_list = []
        # Respiratory signals are generated in segments
        for i in range(0, n + 1):
            # Central Apnea a is between 0.3 to 0.6, b is between 1.37 to 1.77, c is between -0.05 to +0.05，d is
            # between -0.1 to 0.1
            breath_list.append(
                breathing(list_splice[i + t * (n + 2)], randa2b(0.3, 0.6, 1), randa2b(1.37, 1.77, 1),
                          randa2b(-0.05, 0.05, 1),
                          randa2b(-0.1, 0.1, 1)))
            # biots Asphyxia phase a is between -0.05 to 0.05, b is between 0.01 to 3.14, c is between -0.05 to
            # +0.05，d is between -0.01 to 0.01
        breath_list.append(breathing(list_splice[n + 1 + t * (n + 2)], randa2b(-0.05, 0.05, 1), randa2b(0.01, 3.14, 1),
                                     randa2b(-0.2, 0.2, 1),
                                     randa2b(-0.01, 0.01, 1)))

    # save together
    index = 0
    mat = [0] * (times*n*2)
    for i in range(0, (n + 2)*1):
        for j in range(0, len(breath_list[i]) - 1):
            mat[index] = (breath_list[i])[j]
            index = index + 1

    # Add Gaussian noise，SNR = 20
    noise = awgn(mat)
    noise.tolist()
    for i in range(0, len(noise)):
        mat[i] = mat[i] + noise[i]
        # mat[i] = mat[i].astype(np.float32)
    return mat
