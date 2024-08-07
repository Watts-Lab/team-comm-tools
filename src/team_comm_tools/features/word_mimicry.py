import numpy as np
import pandas as pd
from string import punctuation
import re
from sklearn.metrics.pairwise import cosine_similarity

from team_comm_tools.features.get_all_DD_features import *

# '''
#     To compute word mimicry, we use the dataset that removed all the punctuations
#     This is a *chat-level* feature in which order matters.
# '''
def get_function_words_in_message(text, function_word_reference):
  """
  Extract the function words & non-functions words from a message

  Args:
      text (str): The input text to be analyzed.
      function_word_reference (list): A list of function words to reference against.

  Returns:
      list: A list of function words found in the input text.
  """

  return [x for x in text.split() if x in function_word_reference]

def get_content_words_in_message(text, function_word_reference):

  """
  Extract the non-function words in a given message.

  Args:
      text (str): The input text to be analyzed.
      function_word_reference (list): A list of function words to reference against.

  Returns:
      list: A list of content words found in the input text.
  """
  return [x for x in text.split() if x not in function_word_reference]


def mimic_words(df, on_column, conversation_id):
  """
  Return a list of words that are also used in the other's previous turn.

  Args:
      df (DataFrame): The dataset that removed all punctuations.
      on_column (str): The column that we want to find mimicry on.
      conversation_id (str): The column name that should be selected as the conversation ID.

  Returns:
      list: A list of lists, where each sublist contains words mimicked from the previous turn.
  """
  word_mimic = [[]]
  for i in range(1, len(df)):
    if df.loc[i, conversation_id] == df.loc[i-1, conversation_id]: # only do this if they're in the same conversation
      word_mimic.append([x for x in df.loc[i, on_column] if x in df.loc[(i-1),on_column]])
    else:
      word_mimic.append([])
  return word_mimic

def function_mimicry_score(function_mimic_words):
  """
  Compute the number of mimic words for function words by simply counting the number of mimic words using len().

  Args:
      function_mimic_words (list): Each entry under the `function_word_mimicry` column.

  Returns:
      int: The number of function mimic words.
  """
  return len(function_mimic_words)

def compute_frequency(df, on_column):
  """
  Compute the frequency of each content word across the whole dataset.

  Args:
      df (DataFrame): The input dataframe.
      on_column (str): The column with which we calculate content word frequency.

  Returns:
      dict: A dictionary with content words as keys and their frequencies as values.
  """
  return(dict(pd.Series(np.concatenate(df[on_column])).value_counts()))


def computeTF(column_mimc, frequency_dict):
  """
  Compute the term frequency of each content mimic word, then sum them up.

  Args:
      column_mimc (list): Each entry under the `content_word_mimicry` column.
      frequency_dict (dict): A dictionary of content word frequency across the dataset.

  Returns:
      float: The sum of term frequencies for the content mimic words.
  """
  tfdict = {}
  wf = pd.Series(column_mimc, dtype = 'str').value_counts()
  for i in wf.index:
    tfdict[i] = wf[i]/frequency_dict[i]
  return sum(tfdict.values())


def Content_mimicry_score(df, column_count_frequency, column_count_mimic):
  """
  Combine the steps to compute the content word mimicry score.

  Args:
      df (DataFrame): The input dataframe.
      column_count_frequency (str): The column with content words to calculate frequency.
      column_count_mimic (str): The column with content word mimicry.

  Returns:
      Series: A series with content word accommodation scores.
  
  """
  # Compute the frequency of each content word across the whole dataset
  ContWordFreq = compute_frequency(df, column_count_frequency)
  # Compute the content_mimicry_score
  return df[column_count_mimic].apply(lambda x:computeTF(x, ContWordFreq))

def get_mimicry_bert(chat_data, vect_data, conversation_id):
  """ 
  Uses SBERT vectors to get the cosine similarity between each message and the previous message.

  Args:
    chat_data (DataFrame): The input chat dataframe.
    vect_data (DataFrame): The dataframe containing SBERT vectors.
    conversation_id (str): The column name that should be selected as the conversation ID.

  Returns:
    list: A list of cosine similarity scores between each message and the previous message.
  """
  
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


def get_moving_mimicry(chat_data, vect_data, conversation_id):
  """
  Calculate the moving average of mimicry scores using SBERT vectors.

  Args:
      chat_data (DataFrame): The input chat dataframe.
      vect_data (DataFrame): The dataframe containing SBERT vectors.
      conversation_id (str): The column name that should be selected as the conversation ID.

  Returns:
      list: A list of moving average mimicry scores for each message in the conversation.
  """

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