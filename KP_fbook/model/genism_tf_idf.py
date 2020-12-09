import numpy as np
from gensim import models
import gensim
import pandas as pd
from gensim.utils import simple_preprocess

from gensim import corpora
from pprint import pprint
from clean_text import clean
from nltk.tokenize import word_tokenize

df = pd.read_csv("../Data/sample_data.csv", encoding='utf-8')
df_strings = df['threads'].apply(
    func=lambda x: clean(x)
)
# df_strings = df_strings[3]
# print("original_text", df_strings, "\n")

# text = [word_tokenize(df_strings)]
# print(text)


# Create the Dictionary and Corpus
mydict = corpora.Dictionary([word_tokenize(thread) for thread in df_strings])
print(len(mydict))
corpus = [mydict.doc2bow(word_tokenize(thread)) for thread in df_strings]
print(len(corpus))
# Show the Word Weights in Corpus
for doc in corpus:
    pass
    #print([[mydict[id], freq] for id, freq in doc])

    # [['first', 1], ['is', 1], ['line', 1], ['the', 1], ['this', 1]]
    # [['is', 1], ['the', 1], ['this', 1], ['second', 1], ['sentence', 1]]
    # [['this', 1], ['document', 1], ['third', 1]]

    # Create the TF-IDF model
tfidf = models.TfidfModel(corpus, smartirs='ntc')

# Show the TF-IDF weights
counter = 0
for doc in tfidf[corpus]:
    counter += 1
    print(counter)

    #print([[mydict[id], np.around(freq, decimals=2)] for id, freq in doc])
    # [['first', 0.66], ['is', 0.24], ['line', 0.66], ['the', 0.24]]
    # [['is', 0.24], ['the', 0.24], ['second', 0.66], ['sentence', 0.66]]
    # [['document', 0.71], ['third', 0.71]]
