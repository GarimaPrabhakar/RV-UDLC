from AddSignals import AddingTimeSeries
import numpy as np
import pandas as pd


class UpperLimit:

    def __init__(self, time, y_vals, error):
        """
        Constructs an UpperLimits object given information about the inputted time series to calculate the
        upper detection limits on radial velocity data as described by Zechmeister et al. (2009)
        :param time: timestamps (numpy array)
        :param y_vals: radial velocities (numpy array)
        :param error: error on the radial velocities (numpy array)
        """
        self.t = time
        self.y = y_vals
        self.err = error

        # Some storage variables
        self.ul = pd.DataFrame()

    def get_amplitude_limits(self, period, amp_start=0.05, amp_end=10, num_signals=1000, fap_threshold=0.001):
        """
        Computes the upper detection limit at a given period by iteratively injecting sinusoidal signals
        at a range of amplitudes and recovering the signals at which the false alarm probability is at 0.001,
        as described by Zechmeister et al. (2009).
        :param fap_threshold: the false alarm probability threshold at which a signal is statistically significant
        enough to be an exoplanet. The default is 0.001, as determined by Zechmeister et al. (2009).
        :param period: the given period to compute the upper detection limit for.
        :param amp_start: the lower bound for tested amplitudes.
        :param amp_end: the upper bound for tested amplitudes.
        :param num_signals: the number of signals to be tested. Note that if more signals are tested, the
        results will be more accurate, but computation time will be longer.
        :return: the period and amplitude of the upper detection limit.
        """
        ts = AddingTimeSeries(self.t, self.y, self.err)
        ts.add_increment_signals(period, amp_start, amp_end, num_signals)

        signal = ts.check_FAP(fap_threshold=fap_threshold)

        return signal[0], signal[1]

    def upper_limits_array(self, periods, fap_threshold=0.01):
        """
        Computes the upper detection limits on period and amplitude for a numpy array of periods.
        :param fap_threshold: the false alarm probability threshold at which a signal is statistically significant
        enough to be an exoplanet. The default is 0.001, as determined by Zechmeister et al. (2009).
        :param periods: the numpy array of periods to calculate the amplitude
        :return: a pandas data frame with the Period and Amplitude upper detection limits
        """
        amplitude = []
        period = []
        for per in periods:
            p, a = UpperLimit(self.t, self.y, self.err).get_amplitude_limits(per, fap_threshold=fap_threshold)
            amplitude.append(a)
            period.append(p)

        self.ul = pd.DataFrame({"Period": period, "Amplitude": amplitude})
        return self.ul

    def upper_limits(self, start_per=0.05, end_per=1500, num_datapoints=1000, fap_threshold=0.01):
        """
        Computes the upper detection limits on period and amplitude for a numpy array of periods.
        :param fap_threshold: he false alarm probability threshold at which a signal is statistically significant
        enough to be an exoplanet. The default is 0.001, as determined by Zechmeister et al. (2009).
        :param start_per: The minimum period at which the upper detection limit will be computed.
        :param end_per:  The maximum period at which the upper detection limit will be computed.
        :param num_datapoints: The number of periods for which the upper detection limit will be computed.
        :return: a pandas data frame with the Period and Amplitude upper detection limits
        """
        per = np.linspace(start_per, end_per, num_datapoints)
        return UpperLimit(self.t, self.y, self.err).upper_limits_array(periods=per, fap_threshold=fap_threshold)
