import numpy as np
import csv
import pandas as pd

"""
file: turn-taking_features.py
---
Calculates the turn-taking index for each speaker
"""

"""
Returns the total number of turns for each speaker

input_data (pd.DataFrame): a dataframe of conversations, in which each row is one chat
speaker_id_col (str): the name of the column containing the speaker's unique identifier
"""

def count_turns(input_data, speaker_id_col):
    """
    Returns the total number of turns for each speaker.

    Args:
        input_data (pd.DataFrame): A dataframe of conversations, in which each row is one chat.
        speaker_id_col (str): The name of the column containing the speaker's unique identifier.

    Returns:
        pd.DataFrame: A dataframe with columns for the speaker's unique identifier and their turn count.
    """

    temp_turn_count = 1
    consolidated_actions = []

    start_index = input_data.index[0] + 1
    end_index = len(input_data) + input_data.index[0]

    prev_row = input_data.iloc[0]
    for i, row in input_data.iloc[1:, :].iterrows():
        cur_row = row
        if cur_row[speaker_id_col] == prev_row[speaker_id_col]:
            temp_turn_count += 1
        else:
            consolidated_actions.append((prev_row[speaker_id_col], temp_turn_count))
            temp_turn_count = 1

        prev_row = cur_row

    consolidated_actions.append((cur_row[speaker_id_col], temp_turn_count))
    assert sum(x[1] for x in consolidated_actions) == len(input_data)

    df_consolidated_actions = pd.DataFrame(columns=[speaker_id_col, "turn_count"], data=consolidated_actions)
    return df_consolidated_actions

def count_turn_taking_index(input_data, speaker_id_col):
    """
    Returns the turn-taking index for each speaker.

    Args:
        input_data (pd.DataFrame): A dataframe of conversations, in which each row is one chat.
        speaker_id_col (str): The name of the column containing the speaker's unique identifier.

    Returns:
        float: The turn-taking index for the speaker.
    """

    if(len(input_data) == 1): # there is only 1 speaker for one row; catch a divide by zero error
        return 0
    else:
        return (len(count_turns(input_data, speaker_id_col)) - 1) / (len(input_data) - 1)

def get_turn(input_data, conversation_id_col, speaker_id_col):
    """
    Returns the turn-taking index for each conversation.

    Args:
        input_data (pd.DataFrame): A dataframe of conversations, in which each row is one chat.
        conversation_id_col (str): The name of the column containing the conversation's unique identifier.
        speaker_id_col (str): The name of the column containing the speaker's unique identifier.

    Returns:
        pd.DataFrame: A dataframe with columns for the conversation's unique identifier and the turn-taking index.
    """
    
    turn_calculated_2 = input_data.groupby(conversation_id_col).apply(lambda x : count_turn_taking_index(x, speaker_id_col)).reset_index().rename(columns={0: "turn_taking_index"})
    return turn_calculated_2