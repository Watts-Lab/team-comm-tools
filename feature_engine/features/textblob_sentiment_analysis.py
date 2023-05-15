import pandas as pd
from textblob import TextBlob
import statistics as stat

'''
This is a *chat-level feature*.
Polarity: Ranges between -1 to 1,  -1 is most negative, 0 is neutral, 1 is positive
Subjectivity: Ranges between 0 to 1, 0 - purely factual, 1 - pure opinion
'''
def get_subjectivity_score(string):
    return TextBlob(string).sentiment.subjectivity
def get_polarity_score(string):
    return TextBlob(string).sentiment.polarity