import argparse
import pandas as pd
import json
import re
import regex
import ast
from json_helpers import flatten_json_iterative_solution

######################################################################################################


def main():
    df = pd.read_csv("../Data/data.csv", encoding="utf-8",
                     sep=',')
    if args.remove == 1:
        df = remove_threads(df)
        df.to_csv('../Data/data.csv', index=False,
                  encoding='utf-8', sep=',', header=True)
    elif args.jsonify == 1:
        df = clean_json(df)
        df.to_csv('../Data/json_data.csv', index=False,
                  encoding='utf-8', sep=',', header=True)
    elif args.finalize:
        df_new = pd.read_csv("../Data/json_data.csv",
                             encoding="utf-8", sep=',')
        df_new = df_new.drop(labels=['json_obj'], axis=1)
        df_new = df_new[df_new['depth'] > 0]
        df_new.to_csv('../Data/sample_data.csv', index=False,
                      encoding="utf-8", sep=',', header=True)

######################################################################################################


"""
Function removes posts with no comments and duplicates
"""


def remove_threads(df):
    clean_df = df.dropna(subset=["json_obj"], axis=0)
    clean_df = clean_df.drop_duplicates(
        subset=['Post', 'json_obj'], keep="first")
    return clean_df


######################################################################################################
"""
Json objects - combines all the dictionaries into a giant string or list

"""


def clean_json(df):
    df["threads"] = ""
    df["depth"] = ""
    count = 0
    for row in range(len(df)):

        data = df["json_obj"][row]
        try:
            json_obj = ast.literal_eval(data)
            count += 1
        except:
            pass
        length = len(json_obj)
        unpacked_json = flatten_json_iterative_solution(json_obj)
        df["threads"][row] = ". ".join(unpacked_json.values())
        df["depth"][row] = length
    print(count)

    return df

######################################################################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean up Facebook data")
    optional_parser = parser.add_argument_group("optional arguments")
    optional_parser.add_argument(
        '-remove', '-r', help="Delete posts with no comments", type=int, default=0)
    optional_parser.add_argument(
        '-jsonify', '-j', help="Converts json objects into text", type=int, default=0)
    optional_parser.add_argument(
        '-finalize', '-f', help="set up training data", type=int, default=0)
    args = parser.parse_args()

    main()
