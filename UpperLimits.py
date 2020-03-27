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

    def get_amplitude_limits(self, period, amp_start=0.05, amp_end=10, fap_threshold=0.001):
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
        per, amp, fap = ts.add_increment_signals(period=period, start_amp=amp_start,
                                                 end_amp=amp_end, fap_threshold=fap_threshold)

        return per, amp, fap

    def upper_limits_array(self, periods, fap_threshold=0.01, amp_start=0.05, amp_end=10):
        """
        Computes the upper detection limits on period and amplitude for a numpy array of periods.
        :param fap_threshold: the false alarm probability threshold at which a signal is statistically significant
        enough to be an exoplanet. The default is 0.001, as determined by Zechmeister et al. (2009).
        :param periods: the numpy array of periods to calculate the amplitude
        :return: a pandas data frame with the Period and Amplitude upper detection limits
        """
        amplitude = []
        period = []
        fap_ = []
        for per in periods:
            upper_limits_ = UpperLimit(self.t, self.y, self.err).get_amplitude_limits(period=per, amp_start=amp_start,
                                                                                      amp_end=amp_end,
                                                                                      fap_threshold=fap_threshold)

            amplitude.append(upper_limits_[0])
            period.append(upper_limits_[1])
            fap_.append(upper_limits_[2])

            print("Finished calculation for upper detection limit at period: ", upper_limits_[0],
                  " with the FAP at ", upper_limits_[2])

        self.ul = pd.DataFrame({"Period": period, "Amplitude": amplitude, "FAP": fap_})
        return self.ul

    def upper_limits(self, start_per=0.05, num_datapoints=1000, end_per=1000, fap_threshold=0.01,
                     amp_start=0.05, amp_end=1000, amprange=10000):
        """
        Computes the upper detection limits on period and amplitude for a numpy array of periods.
        :param amprange: the number of amplitudes to test
        :param amp_end: the maximum amplitude to test
        :param amp_start: the minimum amplitude to test
        :param fap_threshold: he false alarm probability threshold at which a signal is statistically significant
        enough to be an exoplanet. The default is 0.001, as determined by Zechmeister et al. (2009).
        :param start_per: The minimum period at which the upper detection limit will be computed.
        :param end_per:  The maximum period at which the upper detection limit will be computed.
        :param num_datapoints: The number of periods for which the upper detection limit will be computed.
        :return: a pandas data frame with the Period and Amplitude upper detection limits
        """
        per = np.linspace(start_per, end_per, num_datapoints)
        return UpperLimit(self.t, self.y, self.err).upper_limits_array(periods=per,
                                                                       fap_threshold=fap_threshold, amp_start=amp_start,
                                                                       amp_end=amp_end, amprange=amprange)
