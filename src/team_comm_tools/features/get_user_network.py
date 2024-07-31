import pandas as pd
import numpy as np

'''
User Level Feature.

This feature takes in data at the user level, and generates a "user_list" per user per conversation. This "user_list" contains the other participating in this conversation. 

'''

def remove_active_user(df, speaker_id_col):
    counter = 0
    for index, row in df.iterrows():
        user = row[speaker_id_col]
        user_list = row['user_list']
        i = np.argwhere(user_list==user)
        df.at[index,'user_list'] = np.delete(row['user_list'],i)
        df.iloc
    return df

def get_user_network(user_df, conversation_id_col, speaker_id_col):
    
    user_lists = user_df.groupby(conversation_id_col, group_keys=True).apply(lambda df : np.asarray(df[speaker_id_col]))

    user_list_df = pd.merge(
        left=user_df,
        right=user_lists.rename("user_list"),
        on=[conversation_id_col],
        how="inner"
    )
    
    user_list_df_final = user_list_df.groupby(conversation_id_col, group_keys=True).apply(
        lambda df : remove_active_user(df, speaker_id_col)).reset_index(drop=True)
    
    return user_list_df_final[[conversation_id_col, speaker_id_col, 'user_list']]