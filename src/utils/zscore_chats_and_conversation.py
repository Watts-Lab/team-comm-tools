import numpy as np
import pandas as pd
import scipy.stats as stats

def get_zscore_across_all_chats(chats_data, on_column):
  """Calculate the z-score of a specified column for each chat message across the entire dataset.

  This function computes the z-score for the values in the specified numeric column, comparing 
  each value to the mean and standard deviation of that column across all chat messages in the dataset.

  :param chats_data: The DataFrame containing chat data, where each row represents one message.
  :type chats_data: pandas.DataFrame
  :param on_column: The name of the numeric column on which the z-score is to be calculated.
  :type on_column: str
  :return: A Series containing the z-scores for each message in the specified column.
  :rtype: pandas.Series
  """
  return(stats.zscore(chats_data[on_column]))

def get_zscore_across_all_conversations(chats_data, on_column, conversation_id_col):
  """Calculate the z-score of a specified column for each chat message within each conversation.

  This function computes the z-score for the values in the specified numeric column, 
  comparing each value to the mean and standard deviation of that column within each conversation.

  :param chats_data: The DataFrame containing chat data, where each row represents one message.
  :type chats_data: pandas.DataFrame
  :param on_column: The name of the numeric column on which the z-score is to be calculated.
  :type on_column: str
  :param conversation_id_col: A string representing the column name that should be selected as the conversation ID. Defaults to "conversation_num".
  :type conversation_id_col: str
  :return: A Series containing the z-scores for each message in the specified column within each conversation.
  :rtype: pandas.Series
  """
  return(chats_data[[conversation_id_col, on_column]].groupby([conversation_id_col])[on_column].transform(lambda x : stats.zscore(x)))