# imports and functions
import string
import pandas as pd
import random
import re
import math
import ast
import argparse

from clean_text import clean
from nltk import word_tokenize


pd.options.mode.chained_assignment = None  # default='warn'


def get_accuracy(keyphrases, list_of_labels):
    # tokenize keyphrases to split up multi-words?
    if args.method == 'tf_idf':
        keyphrases = word_tokenize(" ".join(keyphrases))
    accuracy_list = []
    label_list = ['ngsl', 'tsl', 'awl', 'nawl']
    count = 0
    for label in list_of_labels:
        if len(label) > 0:
            label_score = len(set(keyphrases).intersection(
                label)) / len(label)

        else:
            label_score = math.nan

        if math.isnan(label_score):
            label_accuracy = math.nan
        else:
            label_accuracy = round(label_score * 100, 2)

        accuracy_list.append(label_accuracy)
        count += 1

    return accuracy_list


def get_recall(keyphrases, list_of_labels):

    if args.method == 'tf_idf':
        keyphrases = word_tokenize(" ".join(keyphrases))

    recall_list = []
    label_list = ['ngsl', 'tsl', 'awl', 'nawl']
    count = 0

    for label in list_of_labels:

        tp = len(set(keyphrases).intersection(
            label))

        fn = len([word for word in label if word not in keyphrases])
        try:
            recall_score = round((tp / (fn + tp))*100, 2)
        except:
            recall_score = math.nan

        recall_list.append(recall_score)
        count += 1

    return recall_list


def score_method(method, file, file_output):
    if method == 'tr':
        text_df = pd.read_csv(
            "scores/" + file, encoding="utf-8")
        score_label = 'tr_outputs'  # change to variable

    elif method == 'tf_idf':
        text_df = pd.read_csv("scores/" + file, encoding="utf-8")
        score_label = 'tf_idf_scores'
        text_df['keyphrases'] = ""

    text_df['ngsl_recall'] = ""
    text_df['ngsl_accuracy'] = ""
    text_df['tsl_recall'] = ""
    text_df["tsl_accuracy"] = ""
    text_df['awl_recall'] = ""
    text_df['awl_accuracy'] = ""
    text_df['nawl_recall'] = ""
    text_df['nawl_accuracy'] = ""

    for row in range(len(text_df)):
        output = text_df[score_label][row]
        if method == 'tf_idf':
            tf_idf_scores = ast.literal_eval(output)
            tf_idf_terms = list(tf_idf_scores.keys())
            output = tf_idf_terms
        elif method == 'tr':
            output = ast.literal_eval(output)

        print("selected", output, "\n")

        all_label_list = []

        output_ngsl_list = ast.literal_eval(text_df['ngsl_labels'][row])
        all_label_list.append(output_ngsl_list)

        output_tsl_list = ast.literal_eval(text_df['tsl_labels'][row])
        all_label_list.append(output_tsl_list)

        output_awl_list = ast.literal_eval(text_df['awl_labels'][row])
        all_label_list.append(output_awl_list)

        output_nawl_list = ast.literal_eval(text_df['nawl_labels'][row])
        all_label_list.append(output_nawl_list)

        accuracy_list = get_accuracy(
            output, all_label_list)

        recall_list = get_recall(output, all_label_list)

        print(row)
        if method == 'tf_idf':
            text_df['keyphrases'][row] = output

        text_df['ngsl_accuracy'][row] = accuracy_list[0]
        text_df['ngsl_recall'][row] = recall_list[0]
        text_df['tsl_accuracy'][row] = accuracy_list[1]
        text_df['tsl_recall'][row] = recall_list[1]
        text_df['awl_accuracy'][row] = accuracy_list[2]
        text_df['awl_recall'][row] = recall_list[2]
        text_df['nawl_accuracy'][row] = accuracy_list[3]
        text_df['nawl_recall'][row] = recall_list[3]

    # finished
    if method == 'tr':
        text_df.to_csv("results/" + file_output, index=False)
    elif method == 'tf_idf':
        text_df.to_csv("results/" + file_output, index=False)


def calculate_recall(file):
    df = pd.read_csv("results/" + file)
    df = df.dropna(axis=0, subset=['nawl_recall'], inplace=True)
    print(df)
    nawl_total_scores = 0
    nawl_recall_score = 0
    for row in range(len(df)):
        nawl_score = df['nawl_recall'][row]/100
        nawl_recall_score = nawl_score * \
            len(ast.literal_eval(df['nawl_labels'][row]))
        nawl_total_scores += len(ast.literal_eval(df['nawl_labels'][row]))

    print(nawl_recall_score/nawl_total_scores)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate keyphrase outputs")
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        '-method', '-m', help="Which method to evaluate", type=str, default=""
    )
    required.add_argument(
        '-file', '-f', help="Which csv file to evaluate", type=str, default=""
    )
    required.add_argument(
        '-output', '-o', help="Name of file outputs", type=str, default=""
    )
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        '-recall', '-r', help="calculate recall score", type=int, default=0
    )

    args = parser.parse_args()

    if (args.recall == 1):
        calculate_recall(args.file)
    else:
        score_method(args.method, args.file, args.output)
