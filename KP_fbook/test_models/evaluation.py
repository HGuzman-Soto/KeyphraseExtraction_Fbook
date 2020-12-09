# imports and functions
import pke
import string
import pandas as pd
import random
from clean_text import clean
from nltk import word_tokenize
import re
import math

pd.options.mode.chained_assignment = None  # default='warn'


# Function returns keyphrases from tuple output
def get_keyphrases(keyphrases_tuples):
    output_list = []
    for entry in range(len(keyphrases_tuples)):
        output_list.append(keyphrases_tuples[entry][0])
    return output_list

# Function generates highlighted text for all graph methods


def generate_all_outputs(text_df, random_indexes):
    for number in random_indexes:
        text = clean(text_df['threads'][number])
        extractor_TR = pke.unsupervised.TopicRank()
        extractor_TR.load_document(input=text, language='en')
        extractor_TR.candidate_selection()
        extractor_TR.candidate_weighting()
        keyphrases_TR = extractor_TR.get_n_best(n=10)

        output = get_keyphrases(keyphrases_TR)

# Fixes issues with formatting


def Convert(string):
    try:
        li = list(string.split(", "))
    except:
        li = ""
    return li


"""Function returns individual scores"""

#recall = tp / tp + fn


def exact_get_scores(keyphrases, ngsl_output, tsl_output):
    # tokenize keyphrases to split up multi-words?
    keyphrases = word_tokenize(" ".join(keyphrases))

    if len(ngsl_output) > 0:
        ngsl_score = len(set(keyphrases).intersection(
            ngsl_output)) / len(ngsl_output)
    else:
        ngsl_score = math.nan

    if len(tsl_output) > 0:
        tsl_score = len(set(keyphrases).intersection(
            tsl_output)) / len(tsl_output)
    else:
        tsl_score = math.nan

    # Clean this up later, this is condition to deal with NaN values
    if math.isnan(ngsl_score):
        ngsl_accuracy = math.nan
    else:
        ngsl_accuracy = round(ngsl_score * 100, 2)

    if math.isnan(tsl_score):
        tsl_accuracy = math.nan

    else:
        tsl_accuracy = round(tsl_score * 100, 2)

    print('ngsl: {} out of {}'.format(len(set(keyphrases).intersection(
        ngsl_output)), len(ngsl_output)))
    print('tsl: {} out of {} '.format(len(set(keyphrases).intersection(
        tsl_output)), len(tsl_output)))
    print('ngsl accuracy: {}% \ntsl accuracy: {}%'.format(
        ngsl_accuracy, tsl_accuracy))

    return ngsl_accuracy, tsl_accuracy


def get_recall(keyphrases, ngsl_output, tsl_output):
    keyphrases = word_tokenize(" ".join(keyphrases))

    ngsl_tp = len(set(keyphrases).intersection(
        ngsl_output))

    ngsl_fn = len([word for word in ngsl_output if word not in keyphrases])
    try:
        ngsl_recall = round((ngsl_tp / (ngsl_fn + ngsl_tp))*100, 2)
    except:
        ngsl_recall = math.nan

    tsl_tp = len(set(keyphrases).intersection(
        tsl_output))

    tsl_fn = len([word for word in tsl_output if word not in keyphrases])

    try:
        tsl_recall = round((tsl_tp / (tsl_fn + tsl_tp))*100, 2)
    except:
        tsl_recall = math.nan

    print('ngsl recall: {}% \ntsl recall: {}%\n'.format(
        ngsl_recall, tsl_recall))

    return ngsl_recall, tsl_recall

# Given a graph method, evaluate the accuracy and write it into results


def score_method(method):
    method = 'tr'
    text_df = pd.read_csv("../Data/sample_data.csv", encoding="utf-8")
    text_df['selected'] = ""
    text_df['ngsl_recall'] = ""
    text_df['ngsl_accuracy'] = ""
    text_df['tsl_recall'] = ""
    text_df["tsl_accuracy"] = ""

    text_df['threads'].apply(str)  # clean up step

    for row in range(len(text_df['threads'])):
        print("row:", row)
        extractor = pke.unsupervised.TopicRank()
        text = clean(text_df['threads'][row])
        extractor.load_document(input=text, language='en')
        extractor.candidate_selection()
        try:
            extractor.candidate_weighting()
            optimal_keyphrases = int(round(len(text) / 100, 0))

            if optimal_keyphrases > 0:
                pass
            else:
                optimal_keyphrases = 1
            keyphrases = extractor.get_n_best(n=optimal_keyphrases)

            output = get_keyphrases(keyphrases)
        except:
            output = ""
        print("selected", output)

        output_ngsl = Convert(text_df['ngsl_labels'][row])
        output_ngsl_list = []
        for word in output_ngsl:
            output_ngsl_list.append(word)

        output_tsl = Convert(text_df['tsl_labels'][row])
        output_tsl_list = []
        for word in output_tsl:
            output_tsl_list.append(word)

        scores_list = exact_get_scores(
            output, output_ngsl_list, output_tsl_list)

        recall_list = get_recall(output, output_ngsl_list, output_tsl_list)

        text_df['selected'][row] = output
        text_df['ngsl_accuracy'][row] = scores_list[0]
        text_df['tsl_accuracy'][row] = scores_list[1]

        text_df['ngsl_recall'][row] = recall_list[0]
        text_df['tsl_recall'][row] = recall_list[1]

    # finished
    text_df.to_csv("./results/sample_results_toposRank.csv")


score_method('tr')

# # Read dataset and generate 5 random samples
# text_df = pd.read_csv("../Data/sample_data.csv", encoding="utf-8")
# random.seed(2)
# random_indexes = random.sample(range(0, len(text_df)), 5)

# # minor cleaning of text such as removing urls, emoji's and white spaces
# text = clean(text_df['threads'][random_indexes[2]])


# extractor = pke.unsupervised.TextRank()
# extractor.load_document(input=text, language='en')
# extractor.candidate_selection()
# extractor.candidate_weighting()
# keyphrases = extractor.get_n_best(n=7)


# output = get_keyphrases(keyphrases)


# output_ngsl = Convert(text_df['nsgl_labels'][random_indexes[2]])
# output_ngsl_list = []
# for word in output_ngsl:
#     output_ngsl_list.append(word)

# # print(output_ngsl_list)


# output_tsl = Convert(text_df['tsl_label'][random_indexes[2]])
# output_tsl_list = []
# for word in output_tsl:
#     output_tsl_list.append(word)

# if len(output_tsl_list) > 0:
#     print(output_tsl_list)
# else:
#     print("No TSL words")

# exact_get_scores(output, output_ngsl_list, output_tsl_list)
