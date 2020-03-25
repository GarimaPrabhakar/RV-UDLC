from AddSignals import AddingTimeSeries
import numpy as np
import pandas as pd


class UpperLimit:

    def __init__(self, time, y_vals, error):
        self.t = time
        self.y = y_vals
        self.err = error

        # Some storage variables
        self.ul = pd.DataFrame()

    def get_amplitude_limits(self, period, amp_start=0.05, amp_end=10, num_signals=1000):
        ts = AddingTimeSeries(self.t, self.y, self.err)
        ts.add_increment_signals(period, amp_start, amp_end, num_signals)

        signal = ts.check_FAP()

        return signal[0], signal[1]

    def get_upper_limits(self, periods):
        amplitude = []
        period = []
        for per in periods:
            p, a = UpperLimit(self.t, self.y, self.err).get_amplitude_limits(per)
            amplitude.append(a)
            period.append(p)

        self.ul = pd.DataFrame({"Period": period, "Amplitude": amplitude})
        return self.ul

    def upper_limits(self, start_per=0.05, end_per=1500, num_datapoints=1000):
        per = np.linspace(start_per, end_per, num_datapoints)
        return UpperLimit(self.t, self.y, self.err).get_upper_limits(per)
