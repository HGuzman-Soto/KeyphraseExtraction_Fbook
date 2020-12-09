import pandas as pd
import json
import argparse
import re

from nltk.corpus import stopwords
from ast import literal_eval
from collections import defaultdict


""" 
Function to transfer information from txt to csv - for gsl.txt 
"""


def transfer_info():
    df = pd.read_csv('original_wordlists/gsl.txt', sep=" ", header=0)
    df = df.drop('index', axis=1)
    df.to_csv('gsl.csv', index=False)
    # manually get rid of empty column in excel sheet-> bug


""" Function removes stopwords from a csv file"""


def remove_stopwords(df, label):
    df = pd.read_csv(df, sep=",")
    stop = stopwords.words('english')
    df = df[~df['Words'].isin(stop)]
    df.to_csv(label, index=False)


"""
Define a new csv file

For each related word form in headword, append these to the 'words' column
in the new csv_file

1) Append the headword
2) Append each related word form, if they exist
3) Remove awkward spacing from original csv
4) Finally convert to csv

FIX: In general, the arguement parsing
This function can work for awl and nawl

"""


def unpack_awl(file):
    df = pd.read_csv('original_wordlists/'+file, sep=",")
    awl_arr = []
    for row in range(len(df)):
        awl_arr.append(df['Headword'][row])
        try:
            list_of_words = df['Related word forms'][row].split(",")
        except:  # when there is no list of words
            pass
        for word in list_of_words:
            awl_arr.append(word)
    awl_df = pd.DataFrame(data=awl_arr, columns=['Words'])
    awl_df.Words = awl_df.Words.str.strip()

    awl_df.to_csv("clean_"+file, index=False)


"""
unpacks acl - 

1) Don't need headword
2) Get the list of collocatins
3) unpack determiners

TO-DO: Unpack the optional determiners

Edge case of tuples with more than one word
"""


def unpack_acl():
    df = pd.read_csv(
        'original_wordlists/acl_unofficial.csv', sep=",")
    acl_arr = []
    for row in range(len(df)):
        if '(' in df['Collocations'][row]:
            list_of_words = df['Collocations'][row].split(",")
            for word in list_of_words:
                words = re.sub('[()]', '', str(list_of_words))

        else:
            list_of_words = df['Collocations'][row].split(",")
            for word in list_of_words:
                acl_arr.append(word)
    awl_df = pd.DataFrame(data=acl_arr, columns=['Words'])
    awl_df.Words = awl_df.Words.str.strip()

    awl_df.to_csv("clean_nacl.csv", index=False)


"""
To do: Unpack labels better - weird issue with lists

Function checks to see if a row of text intersects with any labels from a
word list. The intersection of words are attached to that row as labels


TODO
1) Fix unpacking labels a bit better
2) Fix the weird 'words' difference in each word lsit
3) Fix the pandas issue it gives with copying?
"""


def label_data(file, df_label):
    vocab_df = pd.read_csv(file)
    sample_df = pd.read_csv('../Data/sample_data.csv')
    sample_df[df_label] = ""
    list_of_gsl = vocab_df['Words'].to_list()

    row = 0
    for entry in sample_df['threads']:
        label = set(list_of_gsl).intersection(
            str(entry).split())
        sample_df[df_label][row] = list(label)  # check to see if this works
        row += 1

    sample_df.to_csv('../Data/sample_data.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transfer word lists to dataset")
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        '-remove', '-r', help="Remove stopwords from a word list", type=str, default=""
    )
    required.add_argument(
        '-transfer', '-t', help="Transfer word list to dataset", type=str, default="")
    required.add_argument(
        '-label', '-l', help="Label the column name", type=str
    )
    optional = parser.add_argument_group("optional arguements")
    optional.add_argument(
        '-awl', '-a', help="Unpack the awl csv list", type=str, default=""
    )
    optional.add_argument(
        '-collocation', '-c', help="Unpack acl list", type=int, default=0
    )
    args = parser.parse_args()

    if len(args.remove) > 0:
        remove_stopwords(df=args.remove, label=args.label)
    if len(args.transfer) > 0:
        label_data(file=args.transfer, df_label=args.label)
    if len(args.awl) > 0:
        unpack_awl(file=args.awl)
    if args.collocation == 1:
        unpack_acl()


"""
Gsl labels - stopwords and 'I' are removed
"""
# transfer_info() - transfer gsl.txt to gsl.csv
