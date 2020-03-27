import UpperLimits
import pandas as pd


def main(filename):
    df = pd.read_csv(filename)
    t = df['BJD'].to_numpy()
    y = df['RV_mlc_nzp'].to_numpy()
    err = df['e_RV_mlc_nzp'].to_numpy()

    upper_limits = UpperLimits.UpperLimit(t, y, err).upper_limits(start_per=0.05, end_per=1500, num_datapoints=50,
                                                                  fap_threshold=0.001, amprange=10000)
    upper_limits.to_csv(filename[0:len(filename) - 4] + 'UpperDetectionLimits.csv')


main('GJ136-1.csv')
# if __name__ == "__main__":
#     main('filename')
