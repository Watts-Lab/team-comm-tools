import os
import pandas as pd
import spacy
import en_core_web_sm
import re
import numpy as np
import features.keywords as keywords
import regex
import pickle
import errno

nlp = en_core_web_sm.load()
nlp.enable_pipe("senter")
kw = keywords.kw

import nltk
from nltk.corpus import stopwords
from nltk import tokenize

def sentence_split(doc):

    sentences = [str(sent) for sent in doc.sents]
    sentences = [' ' + prep_simple(str(s)) + ' ' for s in sentences]

    return sentences


def sentence_pad(doc):

    sentences = sentence_split(doc)

    return ''.join(sentences)


def count_matches(keywords, doc):
    """
    For a given piece of text, search for the number if keywords from a prespecified list

    Inputs:
            Prespecified list (keywords)
            text

    Outputs:
            Counts of keyword matches
    """

    text = sentence_pad(doc)

    key_res = []
    phrase2_count = []

    for key in keywords:

        key_res.append(key)
        counter = 0

        check = any(item in text for item in keywords[key])

        if check == True:

            for phrase in keywords[key]:

                phrase_count = text.count(phrase)

                if phrase_count > 0:

                    counter = counter + phrase_count

        phrase2_count.append(counter)

    res = pd.DataFrame([key_res, phrase2_count], index=['Features', 'Counts']).T

    return res


def get_dep_pairs(doc):
    """
    Uses spaCy to find list of dependency pairs from text.
    Performs negation handling where by any dependency pairs related to a negated term is removed

    Input:
            Text

    Outputs:
            Dependency pairs from text that do not have ROOT as the head token or is a negated term
    """

    dep_pairs = [[token.dep_, token.head.text, token.head.i, token.text, token.i] for token in doc]
    negations = [dep_pairs[i] for i in range(len(dep_pairs)) if dep_pairs[i][0] == 'neg']
    token_place = [dep_pairs[i][2] for i in range(len(dep_pairs)) if dep_pairs[i][0] == 'neg']

    dep_pairs2 = []

    if len(negations) > 0:

        for j in range(len(dep_pairs)):

            if dep_pairs[j][2] not in token_place and dep_pairs[j] not in dep_pairs2:
                dep_pairs2.append(dep_pairs[j])

    else:
        dep_pairs2 = dep_pairs.copy()

    dep_pairs2 = [[dep_pairs2[i][0], dep_pairs2[i][1], dep_pairs2[i][3]] for i in range(len(dep_pairs2))]

    return dep_pairs2, negations


def get_dep_pairs_noneg(doc):
    """
    No negation is done as we are only searching 'hits'
    """
    return [[token.dep_, token.head.text, token.text] for token in doc]


def count_spacy_matches(keywords, dep_pairs):
    """
    When searching for key words are not sufficient, we may search for dependency pairs.
    Finds any-prespecified dependency pairs from text string and outputs the counts

    Inputs:
            Dependency pairs from text
            Predefined tokens for search in dependency heads

    Output:
            Count of dependency pair matches
    """

    key_res = []
    phrase2_count = []

    for key in keywords:
        key_res.append(key)
        counter = 0

        check = any(item in dep_pairs for item in keywords[key])

        if check == True:

            for phrase in keywords[key]:

                if phrase in dep_pairs:

                    for dep in dep_pairs:

                        if phrase == dep:

                            counter = counter + 1

        phrase2_count.append(counter)

    res = pd.DataFrame([key_res, phrase2_count], index=['Features', 'Counts']).T

    return res


def token_count(doc):

    # Counts number of words in a text string
    return len([token for token in doc])


def bare_command(doc):
    """
    Check the first word of each sentence is a verb AND is contained in list of key words

    Output: Count of matches
    """

    keywords = set([' be ', ' do ', ' please ', ' have ', ' thank ', ' hang ', ' let '])

    first_words = [' ' + prep_simple(str(sent[0])) + ' ' for sent in doc.sents]

    POS_fw = [sent[0].tag_ for sent in doc.sents]

    # returns word if word is a verb and in list of keywords
    bc = [b for a, b in zip(POS_fw, first_words) if a == 'VB' and b not in keywords]

    return len(bc)


def Question(doc):
    """
    Counts number of prespecified question words
    """

    keywords = set([' who ', ' what ', ' where ', ' when ', ' why ', ' how ', ' which '])
    tags = set(['WRB', 'WP', 'WDT'])

    # doc = nlp(text)
    sentences = [str(sent) for sent in doc.sents if '?' in str(sent)]
    all_qs = len(sentences)

    n = 0
    for i in range(len(sentences)):
        whq = [token.tag_ for token in nlp(sentences[i]) if token.tag_ in tags]

        if len(whq) > 0:
            n += 1

    return all_qs - n, n


def word_start(keywords, doc):
    """
    Find first words in text such as conjunctions and affirmations
    """

    key_res = []
    phrase2_count = []

    # doc = nlp(text)

    for key in keywords:

        first_words = [' ' + prep_simple(str(sent[0])) + ' ' for sent in doc.sents]
        cs = [w for w in first_words if w in keywords[key]]

        phrase2_count.append(len(cs))
        key_res.append(key)

    res = pd.DataFrame([key_res, phrase2_count], index=['Features', 'Counts']).T
    return res


def adverb_limiter(keywords, doc):
    """
    Search for tokens that are advmod and in the prespecifid list of words
    """

    tags = [token.dep_ for token in doc if token.dep_ == 'advmod' and
            str(' ' + str(token) + ' ') in keywords['Adverb_Limiter']]

    return len(tags)


def feat_counts(text, kw):
    """
    Main function for getting the features from text input.
    Calls other functions to load dataset, clean text, counts features,
    removes negation phrases.

    Input:
            Text string
            Saved data of keywords and dependency pairs from pickle files

    Output:
            Feature counts
    """

    # remove extraneous backslashes
    text = re.sub('\\\\', '', text)

    text = re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r' ', text)
    text = text.lstrip()
    clean_text = prep_simple(text)
    doc_text = nlp(text)

    doc_clean_text = nlp(clean_text)

    kw_matches = count_matches(kw['word_matches'], doc_text)

    dep_pairs, negations = get_dep_pairs(doc_clean_text)
    dep_pair_matches = count_spacy_matches(kw['spacy_pos'], dep_pairs)

    dep_pairs_noneg = get_dep_pairs_noneg(doc_clean_text)
    disagreement = count_spacy_matches(kw['spacy_noneg'], dep_pairs_noneg)

    neg_dp = set([' ' + i[1] + ' ' for i in negations])
    neg_only = count_spacy_matches(kw['spacy_neg_only'], neg_dp)

    # count start word matches like conjunctions and affirmations
    start_matches = word_start(kw['word_start'], doc_text)

    scores = pd.concat([kw_matches, dep_pair_matches, disagreement, start_matches, neg_only])
    scores = scores.groupby('Features').sum()
    scores = scores.reset_index()

    bc = bare_command(doc_text)
    scores.loc[len(scores)] = ['Bare_Command', bc]

    ynq, whq = Question(doc_text)

    scores.loc[len(scores)] = ['YesNo_Questions', ynq]
    scores.loc[len(scores)] = ['WH_Questions', whq]

    adl = adverb_limiter(kw['spacy_tokentag'], doc_text)
    scores.loc[len(scores)] = ['Adverb_Limiter', adl]

    tokens = token_count(doc_text)
    scores.loc[len(scores)] = ['Token_count', tokens]

    return scores

def load_to_lists(path, words):

    keywords = []

    all_files = os.listdir(path)

    all_files = [file for file in all_files if file.endswith(".txt")]
    all_filenames = [file.split('.', 1)[0] for file in all_files if file.endswith(".txt")]

    feature_names = []

    all_lines = []
    for i in range(len(all_files)):

        if all_files[i].endswith(".txt"):
            try:
                with open(os.path.join(path, all_files[i]), "r") as f:
                    for line in f:
                        splitLine = line.split()

                        if words == 'single':
                            splitLine = ' '.join(splitLine)
                            splitLine = [splitLine.center(len(splitLine) + 2)]
                            all_lines.extend(splitLine)

                        if words == 'multiple':
                            all_lines.append(splitLine)

                        feature_names.append(all_filenames[i])
            except IOError as exc:
                if exc.errno != errno.EISDIR:
                    raise

    return feature_names, all_lines

def load_to_dict(path, words):
    """
    Main function for taking raw .txt files and generates a python dictionary
    Used in conjunction with committ_data function
    """

    keywords = {}

    all_files = os.listdir(path)

    all_files = [file for file in all_files if file.endswith(".txt")]
    all_filenames = [file.split('.', 1)[0] for file in all_files if file.endswith(".txt")]

    for i in range(len(all_files)):
        all_lines = []
        if all_files[i].endswith(".txt"):
            try:
                with open(os.path.join(path, all_files[i]), "r") as f:
                    for line in f:
                        splitLine = line.split()

                        if words == 'single':
                            splitLine = [' '.join(splitLine)]
                            all_lines.extend(splitLine)

                        if words == 'multiple':
                            #splitLine = multi_strings(line)
                            all_lines.append(splitLine)

                if words == 'single':
                    all_lines = [l.center(len(l) + 2) for l in all_lines]

                keywords[all_filenames[i]] = all_lines
            except IOError as exc:
                if exc.errno != errno.EISDIR:
                    raise

    return keywords


def commit_data(path, path_in, folders, words_in_line):
    """
    Loads data from .txt files, creates one dictionary per folder
    and outputs each folder as a dictionary in a pickle file
    """

    for i in range(len(folders)):
        x = load_to_dict(path + folders[i], words_in_line[i])

        file = open(path_in + folders[i] + ".pkl", "wb")
        pickle.dump(x, file)
        file.close()


def load_saved_data(path_in, folders):
    """
    Loads predefined keywords and dependency pairs

    Input:
            Pickle files of dictionaries saved in directory

    Output:
            Python dictionaries
    """

    dicts = {}

    for i in range(len(folders)):

        file = open(path_in + folders[i] + ".pkl", "rb")
        x = pickle.load(file)
        dicts[folders[i]] = x
        file.close()

    return dicts


def clean_text(text):

    orig = ["let's", "i'm", "won't", "can't", "shan't", "'d",
            "'ve", "'s", "'ll", "'re", "n't", "u.s.a.", "u.s.", "e.g.", "i.e.",
            "‘", "’", "“", "”", "100%", "  ", "mr.", "mrs.", "dont", "wont"]

    new = ["let us", "i am", "will not", "cannot", "shall not", " would",
           " have", " is", " will", " are", " not", "usa", "usa", "eg", "ie",
           "'", "'", '"', '"', "definitely", " ", "mr", "mrs", "do not", "would not"]

    for i in range(len(orig)):
        text = text.replace(orig[i], new[i])

    return text


def prep_simple(text):

    # text cleaning

    t = text.lower()
    t = clean_text(t)
    t = re.sub(r"[.?!]+\ *", "", t) 
    t = re.sub('[^A-Za-z,]', ' ', t)  

    return t

def prep_whole(text):

    t = text.lower()
    t = clean_text(t)
    t = re.sub('[^A-Za-z]', ' ', t)

    words = nltk.word_tokenize(t)

    stopword = set(stopwords.words('english'))
    words = [w for w in words if not w in stopword]
    text = ' '.join(words)

    return text


def sentenciser(text):

    nlp.enable_pipe("senter")

    doc = nlp(text)

    split_t = [sent.text for sent in doc.sents]

    return split_t


def punctuation_seperator(text):

    PUNCT_RE = regex.compile(r'(\p{Punctuation})')
    split_punct = PUNCT_RE.split(text)

    # Removing punctuation from the list
    no_punct = []
    for s in split_punct:
        s = re.sub(r'[^\w\s]', '', s)
        if s != '':
            no_punct.append(s)

    return no_punct


def conjection_seperator(text):

    tags = nltk.pos_tag(nltk.word_tokenize(text))
    first_elements = [e[0] for e in tags]
    second_elements = [e[1] for e in tags]

    if 'CC' in second_elements:
        index = [i for i, e in enumerate(second_elements) if e == 'CC']
        index.insert(0, 0)
        parts = [first_elements[i:j] for i, j in zip(index, index[1:] + [None])]

        return [' '.join(p) for p in parts]
    else:
        return [' '.join(first_elements)]


def phrase_split(text):

    text = punctuation_seperator(text)
    phrases = []
    for t in text:
        t = conjection_seperator(t)

        phrases.extend(t)

    return phrases
