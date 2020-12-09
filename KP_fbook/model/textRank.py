import itertools
import nltk
import networkx as nx
import pandas as pd
import string
import math
import spacy

from clean_text import clean
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from itertools import takewhile, tee, islice

pd.options.mode.chained_assignment = None  # default='warn'


stopwords = stopwords.words('english')


"""
3 phrases of textRank
1. Pre-process - clean text and extract noun phrases as candidates with minor filtering
2. Ranking via pageRank algorithm. Set up requires taking co-occurences of each candidate
within a 2-10 window
3. Post-Processing - output top 10 and remove redundancy/join similar phrases together

"""


"""
Given a list of candidates words, iterate through the entire text and see if any words are
adjacent to each other, define by a +1 or -1 range between index. If this is the case, then
append the two words together

"""


"""
Function joins together adjacent candidate keywords.
A minor bug - Will create duplicate keywords
"""


def textRank(text):
    # remove_entities(text)
    clean_text = clean(text)
    clean_text_list = clean_text.split()
    words = [word.lower() for sent in sent_tokenize(clean_text)
             for word in word_tokenize(sent)]

    # get candidates
    candidates = get_NP(clean_text)
    candidates = [word for word in candidates if word not in stopwords]

    labeled_text = [(i, word)
                    for i, word in enumerate(clean_text_list)]
    graph = nx.Graph()

    window = 2
    graph.add_nodes_from([word[-1]
                          for word in labeled_text if word[-1] in candidates])

    # # add edges to the graph
    for index, node1 in labeled_text:
        if node1 not in candidates:
            continue
        if index > window:
            left_side = index - window
        else:
            left_side = index
        for j in range(left_side, min(index + window, len(labeled_text))):
            (j, node2) = labeled_text[j]
            if node2 in candidates and j != node2:
                graph.add_edge(node1, node2)
    w = nx.pagerank_scipy(graph, alpha=0.85,
                          tol=0.0001, weight=None)

    top_words = sorted(w, key=w.get, reverse=True)
    top_words_dict = {k: v for k, v in sorted(
        w.items(), key=lambda items: items[1], reverse=True)}

    # computing optimal keywords
    nb_nodes = graph.number_of_nodes()
    TOP_PERCENT = .15
    optimal_keyphrases = min(math.floor(nb_nodes * TOP_PERCENT), nb_nodes)
    if optimal_keyphrases == 0:
        optimal_keyphrases = 1

    optimal_word_dict = dict(itertools.islice(
        top_words_dict.items(), optimal_keyphrases))

    # best words = longest_sequence
    best_words = longest_sequence_selection(
        top_words[: int(optimal_keyphrases)], labeled_text)

    # remove duplicates
    unique_best_words = list(set(best_words))

    return unique_best_words, optimal_word_dict


def longest_sequence_selection(candidates, sentence):
    dict_sent = dict(sentence)
    rev_dict_sent = {value: key for (key, value) in dict_sent.items()}

    cand_dict = {}
    for word in candidates:
        cand_dict[word] = rev_dict_sent[word]

    reversed_dictionary = {value: key for (key, value) in cand_dict.items()}

    final_cand = []

    for k, v in list(reversed_dictionary.items()):
        if k - 1 in reversed_dictionary.keys():
            final_cand.append(reversed_dictionary[k - 1] + " " + v)
            reversed_dictionary.pop(k-1)
        elif k + 1 in reversed_dictionary.keys():
            final_cand.append(v + " " + reversed_dictionary[k + 1])
            reversed_dictionary.pop(k+1)
        else:
            final_cand.append(v)
    return final_cand


"""
Methods extracts noun phrases as candidates and also filters
1. Punctuaction
2. Stopwords --> need to implement
"""


def get_NP(text):
    grammar = r"""
        NBAR:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

        NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}
    """
    punct = set(string.punctuation)
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

    noun_phrases = [
        nphrase for nphrase in noun_phrases if nphrase not in punct]
    noun_phrases = [n for n in noun_phrases if n]
    return noun_phrases


def get_VP(text):
    grammar = "VP:{<PRP>?<VB>*<RB|RBR>?}"

    punct = set(string.punctuation)
    chunker = nltk.RegexpParser(grammar)
    sentences = nltk.sent_tokenize(text.lower())
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    verb_phrases = []
    for sent in sentences:
        tree = chunker.parse(sent)
        for subtree in tree.subtrees():
            if subtree.label() == 'VP':
                verb_phrases.extend([w[0] for w in subtree.leaves()])

    verb_phrases = [
        vphrase for vphrase in verb_phrases if vphrase not in punct]
    verb_phrases = [n for n in verb_phrases if n]
    return verb_phrases


def remove_entities(text):
    text_no_entities = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    ents = [e.text for e in doc.ents]

    for item in doc:
        if item.text in ents:
            pass
        else:
            text_no_entities.append(item.text)
    print(" ".join(text_no_entities))


text_df = pd.read_csv("../Data/sample_data.csv", encoding="utf-8")

text_df['tr_outputs'] = ""
text_df['tr_scores'] = ""
for row in range(len(text_df)):
    best_words, tr_scores = textRank(text_df['threads'][row])
    text_df['tr_outputs'][row] = best_words
    text_df['tr_scores'][row] = tr_scores
    print(row)

text_df.to_csv('scores/tr_scores.csv', index=False)
