import pandas as pd
import re

#returns the total number of hedge words present in the data set (We can add more hedge words)
def is_hedged_sentence_1(num_hedge_words):
    return 1 if num_hedge_words > 0 else 0