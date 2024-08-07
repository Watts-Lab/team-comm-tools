import pandas as pd
import numpy as np
from team_comm_tools.features.get_all_DD_features import *
# from sklearn.metrics.pairwise import cosine_similarity


def get_forward_flow(chat_data, vect_data, conversation_id_col):

    """
    Measures the extent to which each chat in the conversation 'builds on' the previous chats in the conversation.
    This is a chat level feature.

    Args:
        chat_data (pd.DataFrame): pd.DataFrame containing chat data with 'conversation_num' and 'message_embedding' columns.
        vect_data (pd.DataFrame): pd.DataFrame containing vectorized data.
        conversation_id_col (str): The name of the column representing conversation IDs.

    Returns:
        List: List of cosine similarities representing forward flow for each chat in the conversation.
    """
    
    chat_df = chat_data.copy()
    chat_df['message_embedding'] = conv_to_float_arr(vect_data['message_embedding'].to_frame())

    forward_flow = []

    for num, conv in chat_df.groupby(conversation_id_col,  sort=False):

        forward_flow.append(0)
        embedding_running_sum = conv.iloc[0]["message_embedding"]
        chat_count = 1
        avg_embedding = embedding_running_sum / chat_count

        for index, row in conv[1:].iterrows():
            
            # determine distance from that and average of all previous messages, append to the list
            cos_sim_matrix = cosine_similarity([row['message_embedding'], avg_embedding])
            cosine_sim = cos_sim_matrix[0, 1]

            forward_flow.append(1 - cosine_sim)

            # add to cache, increment count
            embedding_running_sum += row["message_embedding"]
            chat_count += 1
            
            # calculate new average
            avg_embedding = embedding_running_sum / chat_count
    
    return forward_flow