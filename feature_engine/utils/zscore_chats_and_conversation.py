import numpy as np
import pandas as pd
import scipy.stats as stats

# Get the z-score of each message at the chat level: z-score compared across all chats in the whole dataset
'''
@param chats_data = a dataframe of the chat, in which each row is one message.
@param on_column = the name of the numeric column on which the z-score is to be calculated. For example, to z_score info exchange: info_exchange_wordcount
'''
def get_zscore_across_all_chats(chats_data, on_column):
  return(stats.zscore(chats_data[on_column]))

# Get the z-score within each conversation: z-score compared within the conversation (grouped by conversation_num)
'''
@param chats_data = a dataframe of the chat, in which each row is one message.
@param on_column = the name of the numeric column on which the z-score is to be calculated. For example, to z_score info exchange: info_exchange_wordcount
'''
def get_zscore_across_all_conversations(chats_data, on_column):
  return(chats_data[["conversation_num", on_column]].groupby(["conversation_num"])[on_column].transform(lambda x : stats.zscore(x)))