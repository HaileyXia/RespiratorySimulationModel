"""
Cheyne_Stokes
"""
import numpy as np
from tools.awgn import awgn
from tools.breathing import breathing
from tools.randa2b import randa2b


def cheyne_stokes_function(times, sample_rate):
    """
    A simulator used to generate Cheyne-Stokes Respiratory Pattern based on the breathing time and sample rate. Respiratory situation is shallow-deep-shallow
    breathing, then choking. Common symptom is congestive heart failure.
    :param times: breathing time
    :param sample_rate: sample rate
    :return: array of breathing point

    """
    # randomly generates 5 breakpoints in first 5/6 part seconds and sorts them
    random_int = [0] * 5
    for t in range(0, 1):
        n = 5
        random_int[0] = np.random.randint(t * times, (times*4//60) + t * times, size=1)
        random_int[1] = np.random.randint((times*10//60) + t * times, (times*14//60) + t * times, size=1)
        random_int[2] = np.random.randint((times*16//60) + t * times, (times*20//60) + t * times, size=1)
        random_int[3] = np.random.randint((times*26//60) + t * times, (times*30//60) + t * times, size=1)
        random_int[4] = np.random.randint((times*38//60) + t * times, (times*40//60) + t * times, size=1)

        # delimit n+2 intervals
        list_splice = [np.arange(t * times, random_int[0] + 1/sample_rate, 1/sample_rate).tolist()]
        for i in range(0, n-1):
            list_splice.append(np.arange(random_int[i], random_int[i + 1] + 1/sample_rate, 1/sample_rate).tolist())
        # A random breakpoint is generated between the last breakpoint and 1/3 part seconds, resulting in suffocation
        rand_apnea = np.random.randint(random_int[n - 1], (t + 1) * times - (times//3), size=1)
        list_splice.append(np.arange(random_int[n - 1], rand_apnea + 1/sample_rate, 1/sample_rate).tolist())
        list_splice.append(np.arange(rand_apnea, (t + 1) * times + 1/sample_rate, 1/sample_rate).tolist())

        breath_list = [breathing(list_splice[0 + t * (n + 2)], randa2b(0.2, 0.4, 1), randa2b(1.37, 1.77, 1),
                                 randa2b(-0.05, 0.05, 1),
                                 randa2b(-0.1, 0.1, 1)),
                       breathing(list_splice[1 + t * (n + 2)], randa2b(0.2, 0.4, 1), randa2b(1.37, 1.77, 1),
                                 randa2b(-0.05, 0.05, 1),
                                 randa2b(-0.1, 0.1, 1)),
                       breathing(list_splice[2 + t * (n + 2)], randa2b(0.6, 0.9, 1), randa2b(1.37, 1.77, 1),
                                 randa2b(-0.05, 0.05, 1),
                                 randa2b(-0.1, 0.1, 1)),
                       breathing(list_splice[3 + t * (n + 2)], randa2b(0.6, 0.9, 1), randa2b(1.37, 1.77, 1),
                                 randa2b(-0.05, 0.05, 1),
                                 randa2b(-0.1, 0.1, 1)),
                       breathing(list_splice[4 + t * (n + 2)], randa2b(0.2, 0.4, 1), randa2b(1.37, 1.77, 1),
                                 randa2b(-0.05, 0.05, 1),
                                 randa2b(-0.1, 0.1, 1)),
                       breathing(list_splice[5 + t * (n + 2)], randa2b(0.2, 0.4, 1), randa2b(1.37, 1.77, 1),
                                 randa2b(-0.05, 0.05, 1),
                                 randa2b(-0.1, 0.1, 1)),
                       breathing(list_splice[6 + t * (n + 2)], randa2b(-0.05, 0.05, 1), randa2b(0.01, 3.14, 1),
                                 randa2b(-0.2, 0.2, 1),
                                 randa2b(-0.01, 0.01, 1))]
        # Respiratory signals are generated in segments
        # Cheyne_stokes shallow stage of breathing a is between 0.1 to
        # 0.3, b is between 1.37 to 1.77, c is between -0.05 to 0.05, d is between -0.1 to 0.1. Cheyne_stokes shallow
        # stage of breathing a is between 0.3 to 0.4, b is between 1.37 to 1.77, c is between -0.05 to 0.05,
        # d is between -0.1 to 0.1. Cheyne_stokes deep stage of breathing a is between 0.4 to 0.8, b is between 1.37
        # to 1.77, c is between -0.05 to 0.05, d is between -0.1 to 0.1
        # biots Asphyxia phase a is between -0.05 to 0.05, b is between 0.01 to 3.14, c is between -0.01 to
        # +0.01，d is between -0.01 to 0.01

    # save together
    index = 0
    mat = [0] * (times*sample_rate)
    for i in range(0, (n + 2) * 1):
        for j in range(0, len(breath_list[i])-2):
            mat[index] = (breath_list[i])[j]
            index = index + 1

    # Add Gaussian noise，SNR = 20
    noise = awgn(mat)
    noise.tolist()
    for i in range(0, len(noise)):
        mat[i] = mat[i] + noise[i]
    return mat
