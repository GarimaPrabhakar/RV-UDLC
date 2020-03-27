import UpperLimits
import AddSignals
import pandas as pd
import os


def main():
    files = os.listdir("NonDetections")

    for filename in files:
        print("Analyzing Upper Detection Limits for file " + filename + "...")
        path = "NonDetections/" + filename
        df = pd.read_csv(path)
        t = df['BJD'].to_numpy()
        y = df['RV_mlc_nzp'].to_numpy()
        err = df['e_RV_mlc_nzp'].to_numpy()

        upper_limits = UpperLimits.UpperLimit(t, y, err).upper_limits(start_per=0.05, end_per=1000, num_datapoints=1000,
                                                                      fap_threshold=0.001, amprange=5000)
        upper_limits.to_csv("UpperLimits/" + filename[0:len(filename) - 4] + 'UpperDetectionLimits.csv')

        print("Done! Your results are stored in a csv file at: " +
              "UpperLimits/" + filename[0:len(filename) - 4] + 'UpperDetectionLimits.csv')


main()
# if __name__ == "__main__":
#     main('filename')
