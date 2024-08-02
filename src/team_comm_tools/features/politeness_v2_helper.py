import os
import pandas as pd
import spacy
import en_core_web_sm
import re
import numpy as np
import regex
import pickle
import errno

from .keywords import kw

nlp = en_core_web_sm.load()
nlp.enable_pipe("senter")
# kw = keywords.kw

import nltk
from nltk.corpus import stopwords
from nltk import tokenize

def sentence_split(doc):
    """
    Splits a spaCy Doc object into a list of sentences, each with simple preprocessing.

    Args:
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be split into sentences.

    Returns:
        list: A list of preprocessed sentences from the input Doc object.
    """

    sentences = [str(sent) for sent in doc.sents]
    sentences = [' ' + prep_simple(str(s)) + ' ' for s in sentences]

    return sentences


def sentence_pad(doc):
    """
    Pads the sentences of a spaCy Doc object by concatenating them with simple preprocessing.

    Args:
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be padded.

    Returns:
        str: A single string with all sentences concatenated and preprocessed.
    """

    sentences = sentence_split(doc)

    return ''.join(sentences)


def count_matches(keywords, doc):
    """
    Counts the occurrences of prespecified keywords in a text.

    Args:
        keywords (dict): A dictionary where keys are feature names and values are lists of phrases to search for.
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be analyzed.

    Returns:
        pd.DataFrame: A DataFrame with the counts of keyword matches for each feature.
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
    Extracts dependency pairs from a spaCy Doc object and handles negations.

    Args:
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be analyzed.

    Returns:
        tuple: A tuple containing a list of dependency pairs and a list of negations.
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
    Extracts dependency pairs from a spaCy Doc object without handling negations.

    Args:
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be analyzed.

    Returns:
        list: A list of dependency pairs from the input text.
    """
    return [[token.dep_, token.head.text, token.text] for token in doc]


def count_spacy_matches(keywords, dep_pairs):
    """
    Counts occurrences of prespecified dependency pairs in a list of dependency pairs.

    Args:
        keywords (dict): A dictionary where keys are feature names and values are lists of dependency pairs to search for.
        dep_pairs (list): A list of dependency pairs extracted from the text.

    Returns:
        pd.DataFrame: A DataFrame with the counts of dependency pair matches for each feature.
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
    """
    Counts the number of tokens (words) in a spaCy Doc object.

    Args:
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be analyzed.

    Returns:
        int: The number of tokens in the input text.
    """

    # Counts number of words in a text string
    return len([token for token in doc])


def bare_command(doc):
    """
    Checks if the first word of each sentence is a verb and not in a list of keywords.

    Args:
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be analyzed.

    Returns:
        int: The count of sentences that start with a verb not in the keyword list.
    """

    keywords = set([' be ', ' do ', ' please ', ' have ', ' thank ', ' hang ', ' let '])

    first_words = [' ' + prep_simple(str(sent[0])) + ' ' for sent in doc.sents]

    POS_fw = [sent[0].tag_ for sent in doc.sents]

    # returns word if word is a verb and in list of keywords
    bc = [b for a, b in zip(POS_fw, first_words) if a == 'VB' and b not in keywords]

    return len(bc)


def Question(doc):
    """
    Counts the number of sentences containing question words and question marks.

    Args:
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be analyzed.

    Returns:
        tuple: A tuple containing the counts of Yes/No questions and WH-questions.
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
    Finds the first words in text that match a list of keywords.

    Args:
        keywords (dict): A dictionary where keys are feature names and values are lists of first words to search for.
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be analyzed.

    Returns:
        pd.DataFrame: A DataFrame with the counts of first word matches for each feature.
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
    Searches for adverb modifiers in the text that match a list of keywords.

    Args:
        keywords (dict): A dictionary where the key 'Adverb_Limiter' contains a list of adverb modifiers to search for.
        doc (spacy.tokens.Doc): The spaCy Doc object containing the text to be analyzed.

    Returns:
        int: The count of adverb modifier matches in the text.
    """

    tags = [token.dep_ for token in doc if token.dep_ == 'advmod' and
            str(' ' + str(token) + ' ') in keywords['Adverb_Limiter']]

    return len(tags)


def feat_counts(text, kw):
    """
    Extracts various linguistic features from a text using predefined keywords and dependency pairs.

    Args:
        text (str): The text to be analyzed.
        kw (dict): A dictionary containing predefined keywords and dependency pairs.

    Returns:
        pd.DataFrame: A DataFrame with counts of various linguistic features.
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
    """
    Loads keywords from text files in a specified directory into lists.

    Args:
        path (str): The directory path containing the text files.
        words (str): Specifies whether to load 'single' or 'multiple' words per line.

    Returns:
        tuple: A tuple containing a list of feature names and a list of keywords.
    """

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
    Loads keywords from text files in a specified directory into a dictionary.

    Args:
        path (str): The directory path containing the text files.
        words (str): Specifies whether to load 'single' or 'multiple' words per line.

    Returns:
        dict: A dictionary where keys are filenames and values are lists of keywords.
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

    Args:
        path (str): The base directory path containing the folders with text files.
        path_in (str): The directory path to save the pickle files.
        folders (list): A list of folder names containing the text files.
        words_in_line (list): A list specifying whether each folder contains 'single' or 'multiple' words per line.

    Returns:
        None
    """

    for i in range(len(folders)):
        x = load_to_dict(path + folders[i], words_in_line[i])

        file = open(path_in + folders[i] + ".pkl", "wb")
        pickle.dump(x, file)
        file.close()


def load_saved_data(path_in, folders):
    """
    Loads predefined keywords and dependency pairs

    Args:
        path_in (str): The directory path containing the pickle files.
        folders (list): A list of folder names to load the pickle files from.

    Returns:
        dict: A dictionary where keys are folder names and values are dictionaries of keywords and dependency pairs.
    """

    dicts = {}

    for i in range(len(folders)):

        file = open(path_in + folders[i] + ".pkl", "rb")
        x = pickle.load(file)
        dicts[folders[i]] = x
        file.close()

    return dicts


def clean_text(text):
    """
    Cleans and normalizes text by replacing certain patterns and characters.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned and normalized text.
    """

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
    """
    Preprocesses text by cleaning and removing certain characters.

    Args:
        text (str): The input text to be preprocessed.

    Returns:
        str: The preprocessed text.
    """

    # text cleaning

    t = text.lower()
    t = clean_text(t)
    t = re.sub(r"[.?!]+\ *", "", t) 
    t = re.sub('[^A-Za-z,]', ' ', t)  

    return t

def prep_whole(text):
    """
    Preprocesses text by cleaning, removing certain characters, and filtering out stopwords.

    Args:
        text (str): The input text to be preprocessed.

    Returns:
        str: The preprocessed text with stopwords removed.
    """

    t = text.lower()
    t = clean_text(t)
    t = re.sub('[^A-Za-z]', ' ', t)

    words = nltk.word_tokenize(t)

    stopword = set(stopwords.words('english'))
    words = [w for w in words if not w in stopword]
    text = ' '.join(words)

    return text


def sentenciser(text):
    """
    Splits text into sentences using spaCy.

    Args:
        text (str): The input text to be split into sentences.

    Returns:
        list: A list of sentences from the input text.
    """

    nlp.enable_pipe("senter")

    doc = nlp(text)

    split_t = [sent.text for sent in doc.sents]

    return split_t


def punctuation_seperator(text):
    """
    Separates text into segments based on punctuation.

    Args:
        text (str): The input text to be separated by punctuation.

    Returns:
        list: A list of text segments with punctuation removed.
    """

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
    """
    Separates text into segments based on conjunctions.

    Args:
        text (str): The input text to be separated by conjunctions.

    Returns:
        list: A list of text segments separated by conjunctions.
    """

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
    """
    Splits text into phrases based on punctuation and conjunctions.

    Args:
        text (str): The input text to be split into phrases.

    Returns:
        list: A list of phrases from the input text.
    """

    text = punctuation_seperator(text)
    phrases = []
    for t in text:
        t = conjection_seperator(t)

        phrases.extend(t)

    return phrases
