from math import sin


def breathing(x, death, frequency, longitudinal, oblique):
    """
    Get breathing point
    :param x: the signal-to-noise ratio
    :param death: amplitude, which is the depth of breath.
    :param frequency: frequency, which is the respiration rate.
    :param longitudinal: amplitude offset between each breakpoint.
    :param oblique: amplitude offset of each waveform with time
    :return: breathing point
    """
    breathing_signal = []
    for i in range(0, len(x)):
        breathing_signal.append(death * sin(frequency * x[i]) + longitudinal + oblique * (x[i] - x[0]))
    return breathing_signal
