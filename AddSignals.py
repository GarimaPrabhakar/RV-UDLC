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


class AddingTimeSeries:
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

        # Some storage variables
        self._y_added_signals = signal_y  # the modified signal
        self._signal_box = np.zeros((1, 3))  # Contains period, amplitude, and FAP for each signal

    def add_increment_signals(self, period, start_amp, end_amp, num_signals=1000):
        """
        Add sine signals to the time series object with a range of amplitudes.
        :param period:
        :param start_amp:
        :param end_amp:
        :param num_signals: The number of signals to add.
        :return:
        """
        time = self.t - self.t[0]
        increment = (end_amp - start_amp) / num_signals
        amp = start_amp
        self._signal_box = np.zeros((num_signals, 3))
        for signal in range(num_signals):
            self._y_added_signals = add_signal(self._y_added_signals, time, amp, period)

            frequency = 1 / period
            ls = LombScargle(self.t, add_signal(self.y, self.t, amp, period), self.err)
            fap = ls.false_alarm_probability(ls.power(frequency))
            print('TEST')
            print(frequency, fap)

            self._signal_box[signal] = np.array([period, amp, fap]).reshape(1, 3)
            amp = amp + increment

        return self._y_added_signals

    def get_signal_box(self):
        """
        Returns a numpy array with information on all signals added to the original time series.
        Each row contains the period, amplitude, and false alarm probability of the signal in that order.
        If no signals have been added to the time series, this method will return an empty
        array of length 0 with 3 columns.
        :return: the numpy array containing the period and amplitude of each signal.
        """
        return self._signal_box

    def get_modified_time_series(self):
        """
        Returns a numpy array with the sum of all signals added to the original time series. If no signals have been
        added to the time series, this method will return an empty array with the length of the time series and
        1 column.
        :return: the numpy array containing the sum of all signals added to the original time series.
        """
        return self._y_added_signals

    def check_FAP(self, signal_box=None, fap_threshold=0.001):
        """
        Returns the signal period and amplitude with the false alarm probability closest to the given threshold.
        :param signal_box: a numpy array of the signals to be checked (format is [period, amplitude, fap]
        for each row in the array).
        :param fap_threshold: the FAP threshold that every signal will be compared to.
        :return: the period and amplitude at which the signal has a FAP closest to 0.001
        """
        if signal_box is None:
            index = np.abs(self._signal_box[:, 2] - fap_threshold).argmin()
            return self._signal_box[index]
        else:
            return signal_box[(np.abs(signal_box[:, 2] - fap_threshold).argmin())]
