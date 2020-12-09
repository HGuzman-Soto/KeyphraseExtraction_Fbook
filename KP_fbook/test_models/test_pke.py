import pke
import string
import pandas as pd
from clean_text import clean

text_df = pd.read_csv("../Data/sample_data.csv", encoding="utf-8")
print("original: ", clean(text_df["threads"][629]), "\n")
text = clean(text_df["threads"][629])


# initialize keyphrase extraction model, here TopicRank
extractor_00 = pke.unsupervised.TextRank()
extractor_0 = pke.unsupervised.SingleRank()
extractor = pke.unsupervised.TopicRank()
extractor_2 = pke.unsupervised.TopicalPageRank()
extractor_3 = pke.unsupervised.PositionRank()
extractor_4 = pke.unsupervised.MultipartiteRank()


# load the content of the document, here document is expected to be in raw
# format (i.e. a simple text file) and preprocessing is carried out using spacy
extractor_00.load_document(input=text, language='en')
extractor_0.load_document(input=text, language='en')
extractor.load_document(input=text, language='en')
extractor_2.load_document(input=text, language='en')
extractor_3.load_document(input=text, language='en')
extractor_4.load_document(input=text, language='en')


# keyphrase candidate selection, in the case of TopicRank: sequences of nouns
# and adjectives (i.e. `(Noun|Adj)*`)
extractor_00.candidate_selection()
extractor_0.candidate_selection()
extractor.candidate_selection()
extractor_2.candidate_selection()
extractor_3.candidate_selection()
extractor_4.candidate_selection()


# candidate weighting, in the case of TopicRank: using a random walk algorithm
extractor_00.candidate_weighting()
extractor_0.candidate_weighting()
extractor.candidate_weighting()
extractor_2.candidate_weighting()
extractor_3.candidate_weighting()
extractor_4.candidate_weighting()

# N-best selection, keyphrases contains the 10 highest scored candidates as
# (keyphrase, score) tuples
keyphrases_00 = extractor_00.get_n_best(n=10)
keyphrases_0 = extractor_0.get_n_best(n=10)
keyphrases = extractor.get_n_best(n=10)
keyphrases_2 = extractor_2.get_n_best(n=10)
keyphrases_3 = extractor_3.get_n_best(n=10)
keyphrases_4 = extractor_4.get_n_best(n=10)

print("TextRank", keyphrases_00, "\n")
print("SingleRank", keyphrases_0, "\n")
print("TopicRank:", keyphrases, "\n")
print("TopicalPageRank:", keyphrases_2, "\n")
print("PositionRank:", keyphrases_3, "\n")
print("MultiPartiteRank:", keyphrases_4, "\n")
