import numpy as np
from astropy.timeseries import LombScargle


def _sinfunc(t, per, amp):
    """
    Returns the y-value for a sine function with a given time, period (in days), and amplitude (m/s).
    :param t: the time (timestamps, a numpy array)
    :param per: the period (a float, in days)
    :param amp: the amplitude (a float, m/s)
    :return: an array with the y-values of the sine function.
    """
    return amp * np.sin((2 * np.pi / per) * t)


def add_signal(old_signal, t, amplitude, period):
    """
    Add a sine function with a given period and amplitude to the old signal.
    :param old_signal: the original signal (a numpy array)
    :param t: timestamps (timestamps, a numpy array)
    :param amplitude: the amplitude (a float, m/s)
    :param period: the period (a float, in days)
    :return:
    """
    return old_signal + _sinfunc(t, period, amplitude)


class AddingTimeSeries(object):
    def __init__(self, time, signal_y, error):
        """
        Constructs a timeSeries object with given timestamps and given y-values. Models the addition of a set
        of signals with a given period and a range of amplitudes.
        :param time: the timestamps (numpy array)
        :param signal_y: the y-values (numpy array)
        :param error: the error in the y-values (numpy array)
        """

        self.t = time
        self.y = signal_y
        self.err = error

    def add_increment_signals(self, period, start_amp=0.001, end_amp=2000, fap_threshold=0.001):
        """
        Add sine signals to the time series object with a range of amplitudes.
        :param fap_threshold:
        :param period:
        :param start_amp:
        :param end_amp:
        :return:
        """
        time = self.t - self.t[0]
        start = start_amp
        end = end_amp

        amp = (start_amp + end_amp) / 2

        fap = 1
        upperLimits = []
        frequency = 1 / period
        # IF DEBUGGING, UNCOMMENT THE COMMENTED LINES OF CODE
        # counter = 0
        while fap_threshold > fap or fap > fap_threshold + fap_threshold / 2:
            # counter = counter + 1
            # print("Counter: ", counter, "Period: ", period, "Current amplitude being tested: ", amp, "FAP: ", fap)
            ls = LombScargle(self.t, add_signal(self.y, time, amp, period), self.err)
            fap = ls.false_alarm_probability(ls.power(frequency))

            if fap_threshold > fap:  # If FAP is too small, DECREASE the amplitude
                if round(start, 6) == end_amp or round(end, 6) == start_amp:

                    upperLimits.append(period)
                    upperLimits.append(amp)
                    upperLimits.append(fap)
                    break

                else:
                    end = amp
                    amp = abs(start + end) / 2

            elif fap_threshold + fap_threshold / 2 < fap:  # If FAP is too large, INCREASE the amplitude
                if round(start, 6) == end_amp or round(end, 6) == start_amp:
                    upperLimits.append(period)
                    upperLimits.append(amp)
                    upperLimits.append(fap)
                    break

                else:
                    start = amp
                    amp = abs(start + end) / 2

            else:
                upperLimits.append(period)
                upperLimits.append(amp)
                upperLimits.append(fap)
                break

        return upperLimits
