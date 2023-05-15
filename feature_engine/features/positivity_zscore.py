import numpy as np
import pandas as pd
import scipy.stats as stats
import nltk
import csv
from nltk.corpus import stopwords

'''
function: get_positivity_wordcount
(Chat-level function)

This gets the net number of "positive" words in the message, minus
any words that are actually English stopwords.
'''
def get_positivity_wordcount(df):
    #Trying to group real positive words by each chat
    return(df['positive_words'] - df['nltk_english_stopwords'])