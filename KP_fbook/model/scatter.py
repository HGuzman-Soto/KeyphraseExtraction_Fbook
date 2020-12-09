import pandas as pd
import matplotlib.pyplot as plt

import argparse


def main():
    df = pd.read_csv("results/" + args.file)
    df = df.drop(columns=['ngsl_accuracy',
                          'tsl_accuracy', 'awl_accuracy', 'nawl_accuracy'])
    df = df.dropna(axis=0, subset=['nawl_recall',
                                   'awl_recall', 'tsl_recall', 'ngsl_recall'])

    ax1 = df.plot(kind='hist', bins=5, y='nawl_recall',
                  color='#FFA3A3', title=args.title)
    ax2 = df.plot(kind='hist', bins=5, color='#FFA321',
                  y='awl_recall', title=args.title)
    ax3 = df.plot(kind='hist', bins=5, y='tsl_recall',
                  color='#33cccc', title=args.title)
    ax4 = df.plot(kind='hist', bins=5, y='ngsl_recall',
                  color='red', title=args.title)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot keyphrase outputs")
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        '-file', '-f', help="Which csv file to evaluate", type=str, default="")
    required.add_argument(
        '-title', '-t', help="title for plots", type=str, default=""
    )

    args = parser.parse_args()
    main()
