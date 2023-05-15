import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re

'''
    This function uses the dataset WITH all the punctuations.
'''

############ Method 1:
# Look for a question mark at the end of a sentence, or look for the first words that indicate a question
'''
This function takes each message as input, and return the number of questions in this message
@param text: each message
'''
def calculate_num_question_naive(text, question_words):
    # step 1: tokenize sentence
    sentences = sent_tokenize(text)
    num_q = 0
    for sentence in sentences:
        # Only proceed if the sentence contains letters or numbers
        if re.match("^[a-zA-Z0-9 ]+", sentence):
            # Is a question if the sentence ends with "?" or starts with a word that is in the question_words list
            if sentence.endswith("?") or word_tokenize(sentence)[0] in question_words:
                num_q += 1
    return num_q

############ Method 2:
# Use a pre-trained model to classify whether a sentence is a quesion or not.
# Source: https://datascience.stackexchange.com/questions/26427/how-to-extract-question-s-from-document-with-nltk
# Detailed explanation of the model training process: please refer to the relevant wiki page


### Note: 
# To apply this method, we need to use punkt, which is a nltk library tool for tokenizing text documents. 
# When we use an old or a degraded version of nltk module we generally need to download the remaining data.
# Run this if there's an error -
# nltk.download('punkt')



###### Modeling training process - 
# step 1: Get the posts from the NPS Chat Corpus with the XML annotation for each post:
posts = nltk.corpus.nps_chat.xml_posts()[:10000]

# step 2: Define a simple feature extractor that checks what words the post contains
def dialogue_act_features(post):
     features = {}
     for word in nltk.word_tokenize(post):
         features['contains({})'.format(word.lower())] = True
     return features

# step 3: Apply the feature extractor to each post (using post.get('class') to get a post's dialogue act type
featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]

# step 4: Build up a classifier using NaiveBayes
# Split the data into training and testing sets
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
# NaiveBayes classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

###### Making predictions using the pre-trained model
'''
This function takes each message as input, and return the number of questions in this message
@param text: each message
'''
def calculate_num_question_nltk(text):
    # step 1: tokenize sentence
    sentences = sent_tokenize(text)
    num_q = 0
    # step 2: classifier
    question_type = ['whQuestion', 'ynQuestion']
    for sentence in sentences:
        if re.match("^[a-zA-Z0-9 ]+", sentence):
            if classifier.classify(dialogue_act_features(sentence)) in question_type:
                num_q += 1
    return num_q


