"""
Main script
script extracts features

1) Nounphrases
2) TF-IDF scores
3) First position

"""
import numpy as np
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
import re


def remove_punctuation(text):
    """
    Returns text free of punctuation marks
    """
    exclude = set(string.punctuation)
    return ''.join([ch for ch in text if ch not in exclude])


def get_NP(text):
    grammar = r"""
        NBAR:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

        NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}
    """
    chunker = nltk.RegexpParser(grammar)
    sentences = nltk.sent_tokenize(text.lower())
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    noun_phrases = []
    for sent in sentences:
        tree = chunker.parse(sent)
        for subtree in tree.subtrees():
            if subtree.label() == 'NP':
                noun_phrases.extend([w[0] for w in subtree.leaves()])

    noun_phrases = [remove_punctuation(nphrase) for nphrase in noun_phrases]
    noun_phrases = [n for n in noun_phrases if n]
    return noun_phrases


def get_TF(text, candidate_words):
    words = [remove_punctuation(w) for w in text.lower().split()]
    words_str = ' '.join(words)
    return [len(re.findall(re.escape(c), words_str))/float(len(words)) for c in candidate_words]


def get_position(text, candidate_words):
    """
    Returns first occurence of each keyword in text
    """
    words = [remove_punctuation(w) for w in text.lower().split()]
    position = []
    for candidate in candidate_words:
        occurences = [pos for pos, w in enumerate(words) if w == candidate]
        if len(occurences) > 0:
            position.append(occurences[0])
        else:
            position.append(0)

    return position


def extract_features(text):
    num_features = 2

    candidate_words = get_NP(text)
    tf_feature = np.array(get_TF(text, candidate_words))
    position_feature = np.array(get_position(text, candidate_words))

    features = np.zeros((len(candidate_words), num_features))

    features[:, 0] = tf_feature
    features[:, 1] = position_feature

    feature_names = ['Term frequency', 'First Occurence']

    print({'features': features, 'names': feature_names})


def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    import itertools
    import nltk
    import string

    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(
        sent) for sent in nltk.sent_tokenize(text))
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                    for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase
    candidates = [' '.join(word for word, pos, chunk in group).lower()
                  for key, group in itertools.groupby(all_chunks, lambda word__pos__chunk: word__pos__chunk[2] != 'O'
                                                      ) if key]

    return [cand for cand in candidates
            if cand not in stop_words and not all(char in punct for char in cand)]


def extract_candidate_words(text, good_tags=set(['JJ', 'JJR', 'JJS', 'NN', 'NNP', 'NNS', 'NNPS'])):
    import itertools
    import nltk
    import string

    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize and POS-tag words
    tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent)
                                                                    for sent in nltk.sent_tokenize(text)))
    # filter on certain POS tags and lowercase all words
    candidates = [word.lower() for word, tag in tagged_words
                  if tag in good_tags and word.lower() not in stop_words
                  and not all(char in punct for char in word)]

    return candidates
