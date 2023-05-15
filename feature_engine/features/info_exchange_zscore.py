import numpy as np
import pandas as pd
import scipy.stats as stats
# source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.zscore.html
from features.basic_features import *

'''
function: get_info_exchange_wordcount
(Chat-level function)

Get the wordcount used to calculate z-scores: total word count minus first_singular pronouns
'''
def get_info_exchange_wordcount(df):
  # count_words() function was defined in basic_features.py
  return (df["num_words"] - df["first_person"])