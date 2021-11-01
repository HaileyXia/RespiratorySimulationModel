"""
Call 6 types breathing pattern sequentially, generate 6 types of breathing pattern, sort them randomly,
save to a csv file
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pattern.biots_function import biots_function
from pattern.bradypnea_function import bradypnea_function
from pattern.central_apnea_function import central_apnea_function
from pattern.cheyne_stokes_function import cheyne_stokes_function
from pattern.eupnea_function import eupnea_function
from pattern.tachypnea_function import tachypnea_function
from sklearn import preprocessing


def print_list():
    """
    Print 6 types of breathing pattern randomly
    :return: a csv file contains 6 types of breathing pattern
    """
    scale = 10  # Specifies the number of times each breathing pattern occurs
    n_class = 6  # Number of respiratory categories
    breathing_time = 60  # breathing time
    sample_rate = 10  # sample rate
    mat = [[0 for i in range(2)] for j in range(6 * scale)]
    for i in range(0, scale):
        # 1:Eupnea
        mat[i][0] = eupnea_function(breathing_time, sample_rate)
        mat[i][1] = 1
        # 2:Bradypnea
        mat[i + scale][0] = bradypnea_function(breathing_time, sample_rate)
        mat[i + scale][1] = 2
        # 3 Tachypnea
        mat[i + scale * 2][0] = tachypnea_function(breathing_time, sample_rate)
        mat[i + scale * 2][1] = 3
        # 4 Biots
        mat[i + scale * 3][0] = biots_function(breathing_time, sample_rate)
        mat[i + scale * 3][1] = 4
        # 5 Cheyne_stokes
        mat[i + scale * 4][0] = cheyne_stokes_function(breathing_time, sample_rate)
        mat[i + scale * 4][1] = 5
        # 6 Central_Apnea
        mat[i + scale * 5][0] = central_apnea_function(breathing_time, sample_rate)
        mat[i + scale * 5][1] = 6
    signal = [[0 for i in range(breathing_time * 10 + 1)] for j in range(6 * scale)]
    for i in range(0, n_class * scale):
        signal[i][1:breathing_time * 10 + 1] = mat[i][0]

    signal = [[row[i] for row in signal] for i in range(len(signal[0]))]

    # normalized
    min_max_scale = preprocessing.MinMaxScaler(feature_range=(0, 1))
    signal = min_max_scale.fit_transform(signal)

    signal = [[row[i] for row in signal] for i in range(len(signal[0]))]

    for i in range(0, n_class * scale):
        signal[i][0] = mat[i][1]
    np.random.shuffle(signal)
    test = pd.DataFrame(signal, dtype=np.float32)
    test.to_csv('test.csv')

    for j in range(0, 10):
        if signal[j][0] == 1:
            x = np.arange(0, breathing_time * sample_rate)
            y = [signal[j][i] for i in range(1, breathing_time * sample_rate + 1)]
            plt.plot(x, y)
            plt.show()
            break


if __name__ == '__main__':
    print_list()
