import numpy as np


def awgn(signal):
    """
    Add white noise to the original signal.
    :param signal: original breathing point
    :return: breathing point with white noise
    """
    snr = 20
    sig_power = sum([np.math.pow(abs(signal[i]), 2) for i in range(len(signal))])
    sig_power = sig_power / len(signal)
    noise_power = sig_power / (np.math.pow(10, (snr/10)))
    noise = np.math.sqrt(noise_power) * (np.random.uniform(-1, 1, size=len(signal)))

    return noise
