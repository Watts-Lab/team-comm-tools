import numpy as np
import pandas as pd
from string import punctuation
import re
from .get_all_DD_features import *
from sklearn.metrics.pairwise import cosine_similarity

'''
    To compute word mimicry, we use the dataset that removed all the punctuations
    This is a *chat-level* feature in which order matters.
'''

####### Extract the function words & non-functions words from a message
## Get the function words in a given message
def get_function_words_in_message(text, function_word_reference):
   return [x for x in text.split() if x in function_word_reference]
# OUTPUT column: function_words

## Get the non-function words in a given message
def get_content_words_in_message(text, function_word_reference):
  return [x for x in text.split() if x not in function_word_reference]
# OUTPUT column: content_words


####### Return a list of words that are also used in other's previous turn
'''
@param df: the dataset that removed all punctuations
@param on_column: the column that we want to find mimicry on
                  For function words: input == `function_words`
                  For content words: input == `content_words`
@param conversation_id: A string representing the column name that should be selected as the conversation ID
'''
def mimic_words(df, on_column, conversation_id):
  word_mimic = [[]]
  for i in range(1, len(df)):
    if df.loc[i, conversation_id] == df.loc[i-1, conversation_id]: # only do this if they're in the same conversation
      word_mimic.append([x for x in df.loc[i, on_column] if x in df.loc[(i-1),on_column]])
    else:
      word_mimic.append([])
  return word_mimic
# OUTPUT: function_word_mimicry, content_word_mimicry

####### Compute the number of mimic words

## Function word mimicry: simply count the number of mimic words by using len()
'''
@param function_mimic_words: input is each entry under `function_word_mimicry` column.
'''
def function_mimicry_score(function_mimic_words):
  return len(function_mimic_words)
# OUTPUT column: function_word_accommodation 

## Content word mimicry: Compute the inverse frequency of each content word that also occurred in the other’s immediately preceding turn, then sum them up
# Step 1: compute the frequency of each content word across the whole dataset)
# --> ContWordFreq
'''
@param on_column: the column with which we calculate content word frequency. 
                  Input == 'content_words'
'''
def compute_frequency(df, on_column):
  return(dict(pd.Series(np.concatenate(df[on_column])).value_counts()))

# Step 2: compute the term frequency of each content mimic word, then sum them up
'''
This function happens on the individual level. 
@param column_mimic: the column that we want to compute term frequency on. 
                  Input is each entry under `content_word_mimicry` column
@param frequency_list: the dictionary of content word frequency across the dataset. 
                  Input is the result from step 1
'''
def computeTF(column_mimc, frequency_dict):
  tfdict = {}
  wf = pd.Series(column_mimc, dtype = 'str').value_counts()
  for i in wf.index:
    tfdict[i] = wf[i]/frequency_dict[i]
  return sum(tfdict.values())

# Step 3: Combine them
def Content_mimicry_score(df, column_count_frequency, column_count_mimic):
  # Compute the frequency of each content word across the whole dataset
  ContWordFreq = compute_frequency(df, column_count_frequency)
  # Compute the content_mimicry_score
  return df[column_count_mimic].apply(lambda x:computeTF(x, ContWordFreq))
# OUTPUT column: content_word_accommodation


# WITH BERT SENTENCE VECTORS 

"""
function: get_mimicry_bert

Uses SBERT vectors to get the cosine similarity between each message and the previous message.
"""
def get_mimicry_bert(chat_data, vect_data, conversation_id):
  
  chat_df = chat_data.copy()
  chat_df['message_embedding'] = conv_to_float_arr(vect_data['message_embedding'].to_frame())

  mimicry = []

  for num, conv in chat_df.groupby(conversation_id,  sort=False):

      # first chat has no zero mimicry score, nothing previous to compare it to 
      mimicry.append(0)
      prev_embedding = conv.iloc[0]['message_embedding']

      for index, row in conv[1:].iterrows():
          
        # last "pair" has only one element, safeguard against this
        cur_embedding = row['message_embedding']
        cos_sim_matrix = cosine_similarity([cur_embedding, prev_embedding])
        cosine_sim = cos_sim_matrix[0, 1]
        
        mimicry.append(cosine_sim)

        prev_embedding = row['message_embedding'] 

  return mimicry

"""
function: get_moving_mimicry

- prev_mimicry keeps track of the previous mimicry values. This is updated in each iteration.
- The mimicry value is the extent to which each previous chat "mimicked" (i.e., was similar to) the preceding chat,
as calculated by cosine similarity.
- The first mimicry value (0) is ignored in this calculation.
"""
def get_moving_mimicry(chat_data, vect_data, conversation_id):

  chat_df = chat_data.copy()
  chat_df['message_embedding'] = conv_to_float_arr(vect_data['message_embedding'].to_frame())

  moving_mimicry = []

  for num, conv in chat_df.groupby(conversation_id, sort = False):

      prev_embedding = conv.iloc[0]["message_embedding"]
      prev_mimicry = []
      moving_mimicry.append(0) # Start with 0; however, prev_mimicry is not stored so it is ignored from calculations
      
      for index, row in conv[1:].iterrows():
        # find cosine similarity between current pair
        cos_sim_matrix = cosine_similarity([row['message_embedding'], prev_embedding])
        cosine_sim = cos_sim_matrix[0, 1]

        # get the running average
        prev_mimicry.append(cosine_sim)
        moving_mimicry.append(np.average(prev_mimicry))

        # update the previous embedding
        prev_embedding = row['message_embedding'] 
      
  return moving_mimicry