import numpy as np
import string
import spacy
from spacy.training import Example
from spacy.scorer import Scorer
import random
import pandas as pd
from collections import defaultdict
from utils.preprocess import *

"""
file: named_entity_recognition_features.py
---
Detects whether a user is talking about (or to) someone else in a conversation.
"""

nlp = spacy.load("en_core_web_sm")
named_entities_list=[]

"""
function: num_named_entity

Returns the number of named-entities in a message
"""
def num_named_entity(text, cutoff):
    if (len(named_entities_list) > 0):
        named_entities_list.clear()

    calculate_named_entities(text, cutoff)

    # number of named entities
    return (len(named_entities_list))

"""
function: named_entities

Returns a tuple of all (named-entities, confidence score) in a message
""" 
def named_entities(text, cutoff):
    if (len(named_entities_list) > 0):
        named_entities_list.clear()

    calculate_named_entities(text, cutoff)

    # number of named entities
    return(tuple(named_entities_list))

"""
function: calculate_named_entities

Appends (named-entities, confidence score) to a list of all named entities in a message

Inspired by https://support.prodi.gy/t/accessing-probabilities-in-ner/94
"""    
def calculate_named_entities(text, cutoff):
    docs = list(nlp.pipe([text], disable=['ner']))

    # beam search parsing for ner
    beams = nlp.get_pipe('ner').beam_parse(docs, beam_width=16, beam_density=0.0001)
    entity_scores = defaultdict(float)
    
    # calculating confidence in each named entity prediction
    for doc, beam in zip(docs, beams):
        for score, ents in nlp.get_pipe('ner').moves.get_beam_parses(beam):
            for start, end, label in ents:
                # sum scores for each named entity
                entity_scores[(start, end, label)] += score

    for key in entity_scores:
        start, end, label = key
        score = entity_scores[key]

        # checks if confidence is above the cutoff and if named entity is a PERSON
        if score > cutoff and label == "PERSON":
            named_entities_list.append((doc[start:end], score))

"""
function: built_spacy_ner

Returns a tuple of sentences, the named entity and its position in the sentence, and its label for training

Inspired by https://dataknowsall.com/blog/ner.html
"""     
def built_spacy_ner(text, target, type):
    start = str.find(text, target)
    end = start + len(target)

    return (text, {"entities": [(start, end, type)]})

"""
function: train_spacy_ner

Trains model based on user inputted file that provides example sentences and the named entity that appears

Inspired by https://dataknowsall.com/blog/ner.html
"""   
def train_spacy_ner(training):

    # takes training data from user inputted file
    training["sentence_to_train"] = training["sentence_to_train"].astype(str).apply(preprocess_text)
    training["name_to_train"] = training["name_to_train"].astype(str).apply(preprocess_text)

    TRAIN_DATA = []

    for i in range(0, len(training["sentence_to_train"])):
        TRAIN_DATA.append(
            built_spacy_ner(training["sentence_to_train"][i], training["name_to_train"][i], "PERSON")
        )

    # add a named entity label
    ner = nlp.get_pipe('ner')

    # iterate through training data and add new entity labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # creating an optimizer and selecting a list of pipes NOT to train
    optimizer = nlp.create_optimizer()
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    with nlp.disable_pipes(*other_pipes):
        for itn in range(10):
            random.shuffle(TRAIN_DATA)
            losses = {}

            # batch the examples and iterate over them
            for batch in spacy.util.minibatch(TRAIN_DATA, size=2):
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    nlp.update([example], drop=0.35, sgd=optimizer, losses=losses)