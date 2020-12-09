import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from clean_text import clean
from nltk.corpus import stopwords

pd.options.mode.chained_assignment = None  # default='warn'


stopwords = stopwords.words('english')


all_threads = pd.read_csv('../Data/sample_data.csv')
all_threads['clean_thread'] = all_threads['threads'].apply(
    func=lambda x: clean(x))

vectorizer = TfidfVectorizer(
    max_df=.65, min_df=1, stop_words=stopwords, ngram_range=(1, 1), use_idf=True, norm=None)
transformed_documents = vectorizer.fit_transform(
    all_threads['clean_thread'].apply(str))


transformed_documents_as_array = transformed_documents.toarray()
print(len(transformed_documents_as_array))


all_threads['tf_idf_scores'] = ""
for counter, doc in enumerate(transformed_documents_as_array):
    tf_idf_tuples = list(zip(vectorizer.get_feature_names(), doc))
    one_doc_as_df = pd.DataFrame.from_records(tf_idf_tuples, columns=[
                                              'term', 'score']).sort_values(by='score', ascending=False).reset_index(drop=True)

    print("row:", counter, "\n")
    print("len of doc", len(all_threads['threads'][counter]), "\n")

    optimal_keyphrases = int(
        round(len(all_threads['threads'][counter]) / 150, 0))
    if optimal_keyphrases > 0:
        pass
    else:
        optimal_keyphrases = 1

    print("optimal kp", optimal_keyphrases)

    top_kp = one_doc_as_df[:optimal_keyphrases].set_index(
        'term').to_dict(orient='index')
    all_threads["tf_idf_scores"][counter] = top_kp

    print("list form", one_doc_as_df[:optimal_keyphrases], "\n")


all_threads.to_csv('scores/tf_idf_scores_1.csv', index=False)
