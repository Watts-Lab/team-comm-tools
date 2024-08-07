import pandas as pd
import numpy as np

def remove_active_user(df, speaker_id_col):
    """
    Removes the active user from their own 'user_list' in each row of the DataFrame.

    Args:
        df (pd.DataFrame): Contains 'speaker_nickname' and 'user_list' columns.
        speaker_id_col (str): The name of the column containing the speaker's unique identifier.

    Returns:
        pd.DataFrame: Modified pd.DataFrame with 'user_list' updated to remove the active user.
    """

    counter = 0
    for index, row in df.iterrows():
        user = row[speaker_id_col]
        user_list = row['user_list']
        i = np.argwhere(user_list==user)
        df.at[index,'user_list'] = np.delete(row['user_list'],i)
        df.iloc
    return df

def get_user_network(user_df, conversation_id_col, speaker_id_col):
    """
    Takes in data at the user level, and generates a "user_list" per user per conversation. This "user_list" contains the other participating in this conversation. 
    This is a user level feature.
    
    Args:
        user_df (pd.DataFrame): The dataset for which we are generating a "user_list" per user per conversation.
        conversation_id_col (str): The name of the column containing conversation identifiers.
        speaker_id_col (str): The name of the column containing the speaker's unique identifier.

    Returns:
        pd.DataFrame: Updated user_df with a 'user_list' column
    """
    
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