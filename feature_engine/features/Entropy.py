import pandas as pd
import scipy as sp
import nltk
from nltk import ngrams
from collections import Counter
import math
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# get tokens of length n
def get_ngrams(df,on_column,n):
   
   #tokenize the text into words
   df['ngrams'] = df[on_column].apply(lambda x: list(ngrams(x.split(), n)))

def ngram_dialog_act_entropy(df,on_column,n):

    cv = CountVectorizer(ngram_range=(n, n))
    cv.fit(df[on_column])

    # Transform the strings into vectors
    vectors = cv.transform(df[on_column])

    # Compute the probability of each trigram in the vectors
    prob = vectors.toarray().sum(axis=0) / vectors.toarray().sum()

    # Compute the entropy of the trigrams in the vectors
    entropy = 0
    counter = 0
    for p in prob:
        if p > 0:
            entropy += -p * math.log2(p)
            counter = counter+1

    return entropy/counter