import pandas as pd
import numpy as np

from .discursive_diversity import *

'''
This is a conversation level feature, which computes the variance in discursive diversity across all chunks for each conversation. 

'''
def get_variance_in_DD(chat_data, conversation_id_col, speaker_id_col):
    dd_results = chat_data.groupby([conversation_id_col, 'chunk_num']).apply(lambda x: get_DD(x, conversation_id_col, speaker_id_col))
    dd_results = dd_results.reset_index(drop=True)
    results = dd_results.groupby(conversation_id_col, as_index=False).var()[[conversation_id_col, 'discursive_diversity']]
    return results.rename(columns={'discursive_diversity': 'variance_in_DD'})
